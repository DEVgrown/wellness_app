import random
import string
import logging
from datetime import datetime, date
from django.db import transaction, OperationalError, DatabaseError
from django.db.models import Sum, Count, Q
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, Service, TimeSlot, Booking, UserPackage, PaymentTransaction, AuditLog
from .permissions import IsVerifiedStudioAdmin, IsStudioAdminUser, IsOwnerOrAdmin
from .serializers import (
    ServiceSerializer,
    ServiceCreateUpdateSerializer,
    TimeSlotSerializer,
    TimeSlotCreateUpdateSerializer,
    BulkSlotGenerateSerializer,
    BookingSerializer,
    BookingCreateSerializer,
    RescheduleBookingSerializer,
    AdminBookingUpdateSerializer,
    CustomerUpdateSerializer,
    CustomerCreateSerializer,
    IssuePackagePassSerializer,
    MpesaPaymentSerializer,
    UserPackageSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer
)
from .tasks import process_mpesa_payment_task, send_booking_confirmation_task

User = get_user_model()
logger = logging.getLogger(__name__)


class ApiRootView(APIView):
    """Karina Wellness Booking Platform API Directory."""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'message': 'Welcome to Karina Wellness Booking API (Unified PostgreSQL Engine)',
            'endpoints': {
                'services': request.build_absolute_uri('services/'),
                'slots': request.build_absolute_uri('slots/'),
                'bookings': request.build_absolute_uri('bookings/'),
                'mpesa_stk_push': request.build_absolute_uri('payments/mpesa-stk/'),
                'user_packages': request.build_absolute_uri('user-packages/'),
                'auth_profile': request.build_absolute_uri('auth/profile/'),
                'auth_profile_avatar': request.build_absolute_uri('auth/profile/avatar/'),
                'auth_signup': request.build_absolute_uri('auth/signup/'),
                'auth_login': request.build_absolute_uri('auth/login/'),
                'auth_logout': request.build_absolute_uri('auth/logout/'),
                'auth_me': request.build_absolute_uri('auth/me/'),
            },
            'database': 'Unified PostgreSQL (Django ORM)',
            'frontend_url': 'http://localhost:5173/'
        })


# ==========================================
# SERVICE CATALOG VIEWS
# ==========================================

class ServiceListView(APIView):
    """List services with optional category and location filtering."""
    permission_classes = [AllowAny]

    def get(self, request):
        category = request.query_params.get('category', 'all')
        location = request.query_params.get('location', 'all')
        queryset = Service.objects.all().order_by('created_at')

        if category and category.lower() != 'all':
            queryset = queryset.filter(category__iexact=category)
        if location and location.lower() != 'all':
            queryset = queryset.filter(location_type__icontains=location)

        serializer = ServiceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ServiceDetailView(APIView):
    """Retrieve details for a single service."""
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceSerializer(service, context={'request': request})
        return Response(serializer.data)


# ==========================================
# SCHEDULE & TIME SLOT VIEWS
# ==========================================

class TimeSlotListView(APIView):
    """Retrieve live schedule time slots by date and service."""
    permission_classes = [AllowAny]

    def get(self, request):
        service_id = request.query_params.get('service_id')
        date_str = request.query_params.get('date')

        queryset = TimeSlot.objects.select_related('service').all().order_by('slot_date', 'start_time')

        if service_id:
            queryset = queryset.filter(service_id=service_id)
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(slot_date=target_date)
            except ValueError:
                pass

        serializer = TimeSlotSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


# ==========================================
# BOOKING & PESSIMISTIC CONCURRENCY ENGINE
# ==========================================

class BookingListCreateView(APIView):
    """
    GET: List user bookings (or all if admin requested).
    POST: Atomic slot reservation with pessimistic row lock (guarantee zero overbooking).
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        if request.user and request.user.is_authenticated:
            is_personal = request.query_params.get('personal') in ['1', 'true', 'True']
            user_id = request.query_params.get('user_id')
            if (request.user.is_staff or getattr(request.user, 'is_studio_admin', False)) and not is_personal and not user_id:
                queryset = Booking.objects.select_related('service', 'slot', 'user').all()
            elif user_id and user_id != 'me' and (request.user.is_staff or getattr(request.user, 'is_studio_admin', False)):
                queryset = Booking.objects.select_related('service', 'slot', 'user').filter(user_id=user_id)
            else:
                queryset = Booking.objects.select_related('service', 'slot', 'user').filter(user=request.user)
        else:
            user_name = request.query_params.get('user_name')
            if user_name:
                queryset = Booking.objects.select_related('service', 'slot', 'user').filter(
                    Q(user__username__iexact=user_name) | Q(user__first_name__iexact=user_name)
                )
            else:
                queryset = Booking.objects.none()

        booking_status = request.query_params.get('status')
        if booking_status and booking_status.lower() != 'all':
            queryset = queryset.filter(status=booking_status)

        serializer = BookingSerializer(queryset.order_by('-created_at'), many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        slot_id = request.data.get('slot_id')
        service_id = request.data.get('service_id')
        payment_method = request.data.get('payment_method', 'mpesa')
        currency = request.data.get('currency', 'KES')
        notes = request.data.get('notes', '')

        if not slot_id or not service_id:
            return Response({'error': 'Both slot_id and service_id are required to reserve a session.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Pessimistic row-level lock on slot
                slot = TimeSlot.objects.select_for_update().filter(id=slot_id, service_id=service_id).first()
                if not slot:
                    return Response({'error': 'Specified schedule slot does not exist.'}, status=status.HTTP_404_NOT_FOUND)

                if slot.spots_left <= 0 or slot.is_full:
                    return Response({'error': 'Time slot is fully booked. Please select another slot.'}, status=status.HTTP_409_CONFLICT)

                # 2. Server-side authoritative price determination (eliminates SEC-006 client tampering)
                service = Service.objects.get(id=service_id)
                authoritative_price = service.price_kes if currency == 'KES' else service.price_eur

                # 3. Handle pass deduction if payment_method is pass
                if payment_method == 'pass':
                    user_pass = UserPackage.objects.select_for_update().filter(
                        user=request.user,
                        remaining_sessions__gt=0
                    ).order_by('valid_until', 'created_at').first()
                    if not user_pass:
                        return Response(
                            {'error': 'You do not have an active studio pass with available sessions. Please top up or choose a different payment method.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    user_pass.remaining_sessions -= 1
                    user_pass.save(update_fields=['remaining_sessions'])
                    booking_status = 'confirmed'
                elif payment_method in ['studio', 'card']:
                    booking_status = 'confirmed'
                else:
                    booking_status = 'pending_payment'

                # 4. Decrement slot capacity atomically
                slot.spots_left -= 1
                if slot.spots_left == 0:
                    slot.is_full = True
                slot.save(update_fields=['spots_left', 'is_full', 'updated_at'])

                # 5. Generate unique payment reference
                ref = 'QK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

                # 6. Create booking record
                booking = Booking.objects.create(
                    user=request.user,
                    service=service,
                    slot=slot,
                    status=booking_status,
                    payment_method=payment_method,
                    payment_reference=ref,
                    currency=currency,
                    total_amount=authoritative_price,
                    notes=notes
                )
        except OperationalError:
            return Response(
                {'error': 'Time slot is currently being locked/reserved by another concurrent client. Please retry or choose another slot.'},
                status=status.HTTP_409_CONFLICT
            )

        # 7. Async notification task
        try:
            user_display = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            send_booking_confirmation_task.delay(
                booking_id=str(booking.id),
                user_email=request.user.email,
                service_title=service.title,
                booking_date=str(slot.slot_date),
                time_slot=slot.start_time
            )
        except Exception as e:
            logger.warning(f"Async confirmation task dispatch offline: {e}")

        out_serializer = BookingSerializer(booking, context={'request': request})
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)


class BookingCancelView(APIView):
    """Cancel an active booking and restore slot capacity."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        with transaction.atomic():
            try:
                booking = Booking.objects.select_for_update().get(pk=pk)
            except Booking.DoesNotExist:
                return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Permission check: owner or studio admin
            if not request.user.is_staff and not getattr(request.user, 'is_studio_admin', False) and booking.user != request.user:
                return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

            if booking.status == 'cancelled':
                return Response({'message': 'Booking is already cancelled.'}, status=status.HTTP_200_OK)

            booking.status = 'cancelled'
            booking.notes = f"{booking.notes} [Cancelled by {request.user.username}]".strip()
            booking.save(update_fields=['status', 'notes'])

            # Restore pass session if booking was paid with pass
            if booking.payment_method == 'pass':
                user_pass = UserPackage.objects.filter(user=booking.user).order_by('-created_at').first()
                if user_pass:
                    user_pass.remaining_sessions = min(user_pass.total_sessions, user_pass.remaining_sessions + 1)
                    user_pass.save(update_fields=['remaining_sessions'])

            # Restore slot capacity atomically
            slot = TimeSlot.objects.select_for_update().filter(id=booking.slot_id).first()
            if slot:
                slot.spots_left = min(slot.total_capacity, slot.spots_left + 1)
                if slot.spots_left > 0:
                    slot.is_full = False
                slot.save(update_fields=['spots_left', 'is_full', 'updated_at'])

        serializer = BookingSerializer(booking, context={'request': request})
        return Response(serializer.data)


class BookingRescheduleView(APIView):
    """Reschedule an active booking to a new time slot atomically."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = RescheduleBookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_slot_id = serializer.validated_data['new_slot_id']

        with transaction.atomic():
            try:
                booking = Booking.objects.select_for_update().get(pk=pk)
            except Booking.DoesNotExist:
                return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

            if not request.user.is_staff and not getattr(request.user, 'is_studio_admin', False) and booking.user != request.user:
                return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

            if booking.status == 'cancelled':
                return Response({'error': 'Cannot reschedule a cancelled booking.'}, status=status.HTTP_400_BAD_REQUEST)

            # Lock new slot
            new_slot = TimeSlot.objects.select_for_update().filter(id=new_slot_id, service_id=booking.service_id).first()
            if not new_slot:
                return Response({'error': 'Target slot not found or belongs to a different service.'}, status=status.HTTP_404_NOT_FOUND)

            if new_slot.spots_left <= 0 or new_slot.is_full:
                return Response({'error': 'Target slot is fully booked.'}, status=status.HTTP_409_CONFLICT)

            # Restore old slot
            old_slot = TimeSlot.objects.select_for_update().filter(id=booking.slot_id).first()
            if old_slot:
                old_slot.spots_left = min(old_slot.total_capacity, old_slot.spots_left + 1)
                if old_slot.spots_left > 0:
                    old_slot.is_full = False
                old_slot.save(update_fields=['spots_left', 'is_full', 'updated_at'])

            # Decrement new slot
            new_slot.spots_left -= 1
            if new_slot.spots_left == 0:
                new_slot.is_full = True
            new_slot.save(update_fields=['spots_left', 'is_full', 'updated_at'])

            # Update booking
            booking.slot = new_slot
            booking.save(update_fields=['slot'])

        out_serializer = BookingSerializer(booking, context={'request': request})
        return Response(out_serializer.data)


# ==========================================
# PAYMENTS & PACKAGES
# ==========================================

class MpesaSTKPushView(APIView):
    """Trigger Safaricom M-Pesa STK Push."""
    def post(self, request):
        serializer = MpesaPaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            booking_id = data.get('booking_id')
            phone = data['phone_number']
            amount = data.get('amount', 3500)

            ref = 'QK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            checkout_id = f'ws_CO_{ref}'

            if booking_id:
                try:
                    booking = Booking.objects.get(pk=booking_id)
                    PaymentTransaction.objects.create(
                        booking=booking,
                        provider='daraja_mpesa',
                        checkout_request_id=checkout_id,
                        amount=amount,
                        currency=data.get('currency', 'KES'),
                        phone_number=phone,
                        status='initiated'
                    )
                except Booking.DoesNotExist:
                    pass

            task_id = None
            try:
                async_res = process_mpesa_payment_task.delay(str(booking_id) if booking_id else '', phone, amount)
                task_id = async_res.id
            except Exception as e:
                logger.warning(f"Celery queue unavailable, falling back to direct acknowledgment: {e}")

            return Response({
                'success': True,
                'status': 'INITIATED',
                'message': f'STK Push prompt sent to {phone}. Please check your handset and enter M-Pesa PIN.',
                'checkout_request_id': checkout_id,
                'receipt_reference': ref,
                'task_id': task_id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPackageView(APIView):
    """Retrieve active passes and packages for authenticated user."""
    def get(self, request):
        if request.user and request.user.is_authenticated:
            packages = UserPackage.objects.filter(user=request.user).order_by('-created_at')
        else:
            user_name = request.query_params.get('user_name', 'Sarah')
            packages = UserPackage.objects.filter(user__username__iexact=user_name).order_by('-created_at')

        serializer = UserPackageSerializer(packages, many=True)
        return Response(serializer.data)


# ==========================================
# AUTHENTICATION & PROFILE VIEWS
# ==========================================

class SignUpView(APIView):
    """Register a new member account and issue Simple JWT authentication tokens."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            # Issue complimentary welcome studio pass
            UserPackage.objects.create(
                user=user,
                package_name='Welcome Complimentary Pass',
                total_sessions=1,
                remaining_sessions=1,
                valid_until=date(2026, 12, 31)
            )

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'token': str(refresh.access_token),  # Backward compatibility alias
                'user': UserProfileSerializer(user, context={'request': request}).data,
                'message': 'Account created successfully! Welcome to Karina Wellness.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Authenticate user with username or email and return Simple JWT session tokens."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'token': str(refresh.access_token),  # Backward compatibility alias
                'user': UserProfileSerializer(user, context={'request': request}).data,
                'message': f'Welcome back, {user.first_name or user.username}!'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Invalidate current active session / blacklist refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """Current authenticated user profile view."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'user': UserProfileSerializer(request.user, context={'request': request}).data
        })


class UserProfileDetailView(APIView):
    """
    GET: Retrieve current authenticated user profile including avatar URL and role.
    PATCH: Update profile details (first_name, last_name, phone, bio, emergency_contact).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            full_profile = UserProfileSerializer(request.user, context={'request': request})
            return Response(full_profile.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAvatarManageView(APIView):
    """
    POST: Upload or replace profile picture (multipart/form-data).
    DELETE: Remove existing profile picture and clean up storage.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'avatar' not in request.FILES:
            return Response({'error': 'No avatar image file was provided in upload.'}, status=status.HTTP_400_BAD_REQUEST)

        avatar_file = request.FILES['avatar']

        # 1. Validate file extension
        allowed_extensions = {'jpg', 'jpeg', 'png', 'webp'}
        ext = avatar_file.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            return Response({'error': f'Invalid image format .{ext}. Allowed: JPG, PNG, WebP.'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Validate file size (max 5 MB)
        if avatar_file.size > 5 * 1024 * 1024:
            return Response({'error': 'Avatar file exceeds the 5 MB maximum size limit.'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Cleanly update avatar
        request.user.update_avatar(avatar_file)
        avatar_url = request.build_absolute_uri(request.user.avatar.url)

        return Response({
            'message': 'Profile picture updated successfully! 🌿',
            'avatar_url': avatar_url
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        if not request.user.avatar:
            return Response({'message': 'No profile picture currently set.'}, status=status.HTTP_200_OK)

        request.user.remove_avatar()
        return Response({
            'message': 'Profile picture removed successfully.',
            'avatar_url': None
        }, status=status.HTTP_200_OK)


# ==========================================
# ADMIN MEDIA UPLOAD VIEWS
# ==========================================

class AdminServiceImageManageView(APIView):
    """
    POST: Upload or replace service photo (multipart/form-data with key 'image').
    DELETE: Remove service photo from database and storage.
    """
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided in upload.'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']
        allowed_extensions = {'jpg', 'jpeg', 'png', 'webp'}
        ext = image_file.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            return Response({'error': f'Invalid format .{ext}. Allowed: JPG, PNG, WebP.'}, status=status.HTTP_400_BAD_REQUEST)

        if image_file.size > 10 * 1024 * 1024:
            return Response({'error': 'Image exceeds the 10 MB maximum size limit.'}, status=status.HTTP_400_BAD_REQUEST)

        service.update_image(image_file)
        full_url = request.build_absolute_uri(service.image.url)

        return Response({
            'message': 'Service photo uploaded and saved successfully! 🌿',
            'image_url': full_url
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

        service.remove_image()
        return Response({'message': 'Service photo removed successfully.', 'image_url': None}, status=status.HTTP_200_OK)


class AdminSessionBannerManageView(APIView):
    """
    POST: Upload or replace custom session/workshop banner (multipart/form-data with key 'banner_image').
    DELETE: Remove session banner.
    """
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            slot = TimeSlot.objects.get(pk=pk)
        except TimeSlot.DoesNotExist:
            return Response({'error': 'Session slot not found'}, status=status.HTTP_404_NOT_FOUND)

        if 'banner_image' not in request.FILES:
            return Response({'error': 'No banner image file provided in upload.'}, status=status.HTTP_400_BAD_REQUEST)

        banner_file = request.FILES['banner_image']
        allowed_extensions = {'jpg', 'jpeg', 'png', 'webp'}
        ext = banner_file.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            return Response({'error': f'Invalid format .{ext}. Allowed: JPG, PNG, WebP.'}, status=status.HTTP_400_BAD_REQUEST)

        if banner_file.size > 10 * 1024 * 1024:
            return Response({'error': 'Banner image exceeds the 10 MB maximum size limit.'}, status=status.HTTP_400_BAD_REQUEST)

        slot.update_banner(banner_file)
        full_url = request.build_absolute_uri(slot.banner_image.url)

        return Response({
            'message': 'Session promotional banner uploaded successfully!',
            'banner_image_url': full_url
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            slot = TimeSlot.objects.get(pk=pk)
        except TimeSlot.DoesNotExist:
            return Response({'error': 'Session slot not found'}, status=status.HTTP_404_NOT_FOUND)

        slot.remove_banner()
        return Response({'message': 'Session banner removed successfully.', 'banner_image_url': None}, status=status.HTTP_200_OK)


# ==========================================
# ADMIN MANAGEMENT & CRM VIEWS
# ==========================================

class AdminOverviewView(APIView):
    """KPI Metrics and live analytics for Admin Dashboard."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request):
        now = datetime.now()
        total_bookings = Booking.objects.count()
        confirmed_bookings = Booking.objects.filter(status='confirmed').count()
        total_revenue_kes = Booking.objects.filter(status__in=['confirmed', 'completed'], currency='KES').aggregate(total=Sum('total_amount'))['total'] or 0
        total_revenue_eur = Booking.objects.filter(status__in=['confirmed', 'completed'], currency='EUR').aggregate(total=Sum('total_amount'))['total'] or 0
        active_customers = User.objects.filter(profile__role=UserProfile.Role.CLIENT, is_active=True).count()
        total_slots = TimeSlot.objects.count()
        full_slots = TimeSlot.objects.filter(is_full=True).count()

        recent_bookings = Booking.objects.select_related('service', 'slot', 'user').order_by('-created_at')[:6]

        return Response({
            'metrics': {
                'total_bookings': total_bookings,
                'confirmed_bookings': confirmed_bookings,
                'total_revenue_kes': total_revenue_kes,
                'total_revenue_eur': total_revenue_eur,
                'active_customers': active_customers,
                'occupancy_rate': round((full_slots / total_slots * 100), 1) if total_slots > 0 else 0,
                'total_slots': total_slots
            },
            'recent_bookings': BookingSerializer(recent_bookings, many=True, context={'request': request}).data
        })


class AdminServiceListCreateView(APIView):
    """Admin endpoint to list all services and create new offerings."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request):
        services = Service.objects.all().order_by('-created_at')
        serializer = ServiceSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            return Response(ServiceSerializer(service, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminServiceDetailView(APIView):
    """Admin endpoint to retrieve, update, or remove a service."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ServiceSerializer(service, context={'request': request}).data)

    def patch(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceCreateUpdateSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            service = serializer.save()
            return Response(ServiceSerializer(service, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        service.delete()
        return Response({'message': 'Service removed successfully.'}, status=status.HTTP_200_OK)


class AdminTimeSlotListCreateView(APIView):
    """Admin endpoint to query schedule or create single session slots."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request):
        slots = TimeSlot.objects.select_related('service').all().order_by('slot_date', 'start_time')
        serializer = TimeSlotSerializer(slots, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TimeSlotCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            slot = serializer.save()
            return Response(TimeSlotSerializer(slot, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminTimeSlotBulkCreateView(APIView):
    """Bulk generate recurring slots across specified days of week."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def post(self, request):
        serializer = BulkSlotGenerateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        service_id = data['service_id']
        start_date = data['start_date']
        end_date = data['end_date']
        days_of_week = set(data['days_of_week'])
        times = data['times']
        location_name = data.get('location_name', 'Karen Sanctuary, Nairobi')
        total_capacity = data.get('total_capacity', 6)

        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            return Response({'error': 'Target service not found'}, status=status.HTTP_404_NOT_FOUND)

        created_count = 0
        current_date = start_date
        one_day = datetime.timedelta(days=1) if hasattr(datetime, 'timedelta') else None
        from datetime import timedelta
        one_day = timedelta(days=1)

        while current_date <= end_date:
            if current_date.weekday() in days_of_week:
                for t in times:
                    start_time = t.get('start_time', '09:00 AM')
                    period = t.get('period', 'Morning')
                    _, created = TimeSlot.objects.get_or_create(
                        service=service,
                        slot_date=current_date,
                        start_time=start_time,
                        defaults={
                            'period': period,
                            'location_name': location_name,
                            'total_capacity': total_capacity,
                            'spots_left': total_capacity,
                            'is_full': False
                        }
                    )
                    if created:
                        created_count += 1
            current_date += one_day

        return Response({
            'message': f'Successfully generated {created_count} schedule slots.',
            'created_count': created_count
        }, status=status.HTTP_201_CREATED)


class AdminTimeSlotDetailView(APIView):
    """Admin endpoint to retrieve, edit, or delete a single time slot."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request, pk):
        try:
            slot = TimeSlot.objects.select_related('service').get(pk=pk)
        except TimeSlot.DoesNotExist:
            return Response({'error': 'Time slot not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(TimeSlotSerializer(slot, context={'request': request}).data)

    def patch(self, request, pk):
        try:
            slot = TimeSlot.objects.get(pk=pk)
        except TimeSlot.DoesNotExist:
            return Response({'error': 'Time slot not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TimeSlotCreateUpdateSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            slot = serializer.save()
            return Response(TimeSlotSerializer(slot, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            slot = TimeSlot.objects.get(pk=pk)
        except TimeSlot.DoesNotExist:
            return Response({'error': 'Time slot not found'}, status=status.HTTP_404_NOT_FOUND)
        slot.delete()
        return Response({'message': 'Time slot deleted successfully.'}, status=status.HTTP_200_OK)


class AdminBookingListView(APIView):
    """Admin endpoint to retrieve all bookings with multi-filter search."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request):
        queryset = Booking.objects.select_related('service', 'slot', 'user').all().order_by('-created_at')
        status_filter = request.query_params.get('status')
        if status_filter and status_filter.lower() != 'all':
            queryset = queryset.filter(status=status_filter)

        serializer = BookingSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class AdminBookingDetailView(APIView):
    """Admin endpoint to update booking status, coach notes, or cancel."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request, pk):
        try:
            booking = Booking.objects.select_related('service', 'slot', 'user').get(pk=pk)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BookingSerializer(booking, context={'request': request}).data)

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminBookingUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            booking = serializer.save()
            return Response(BookingSerializer(booking, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        booking.delete()
        return Response({'message': 'Booking deleted successfully.'}, status=status.HTTP_200_OK)


class AdminCustomerListView(APIView):
    """Admin CRM endpoint to list all customers with computed spend, pass balances, and bookings."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request):
        search_query = request.query_params.get('search', '').lower().strip()
        status_filter = request.query_params.get('status', 'all')

        users = User.objects.prefetch_related('bookings', 'packages', 'profile').all().order_by('-date_joined')

        customers_data = []
        for u in users:
            u_bookings = list(u.bookings.all())
            u_packages = list(u.packages.all())

            total_spend_kes = sum(b.total_amount for b in u_bookings if b.currency == 'KES' and b.status != 'cancelled')
            total_spend_eur = sum(b.total_amount for b in u_bookings if b.currency == 'EUR' and b.status != 'cancelled')
            completed_count = sum(1 for b in u_bookings if b.status == 'completed')
            confirmed_count = sum(1 for b in u_bookings if b.status == 'confirmed')
            active_passes = sum(p.remaining_sessions for p in u_packages)

            customer_obj = {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'name': f"{u.first_name} {u.last_name}".strip() or u.username,
                'phone': u.phone or '',
                'role': u.role,
                'is_staff': u.is_staff,
                'is_superuser': u.is_superuser,
                'is_active': u.is_active,
                'date_joined': u.date_joined.strftime('%Y-%m-%d %H:%M') if u.date_joined else '',
                'total_bookings': len(u_bookings),
                'completed_bookings': completed_count,
                'confirmed_bookings': confirmed_count,
                'total_spend_kes': total_spend_kes,
                'total_spend_eur': total_spend_eur,
                'active_passes': active_passes,
                'packages_count': len(u_packages)
            }

            if search_query:
                haystack = f"{u.username} {customer_obj['name']} {u.email} {customer_obj['phone']}".lower()
                if search_query not in haystack:
                    continue

            if status_filter == 'staff' and not u.is_staff:
                continue
            elif status_filter == 'active_bookers' and len(u_bookings) == 0:
                continue
            elif status_filter == 'pass_holders' and active_passes == 0:
                continue
            elif status_filter == 'inactive' and u.is_active:
                continue

            customers_data.append(customer_obj)

        return Response(customers_data)

    def post(self, request):
        serializer = CustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            name = data.get('name', '').strip()
            first_name = ''
            last_name = ''
            if name:
                parts = name.split(' ', 1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ''

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=first_name,
                last_name=last_name,
                is_staff=data.get('is_staff', False)
            )
            if hasattr(user, 'profile'):
                user.profile.phone = data.get('phone', '')
                user.profile.role = data.get('role', UserProfile.Role.CLIENT)
                user.profile.save()

            UserPackage.objects.create(
                user=user,
                package_name='Welcome Complimentary Pass',
                total_sessions=1,
                remaining_sessions=1,
                valid_until=date(2026, 12, 31)
            )

            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip() or user.username,
                'is_staff': user.is_staff,
                'message': f"Customer '{user.username}' created successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCustomerDetailView(APIView):
    """Admin endpoint to view deep details, all bookings, packages, or update customer account."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def get(self, request, pk):
        try:
            u = User.objects.prefetch_related('bookings__service', 'bookings__slot', 'packages').get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'user': UserProfileSerializer(u, context={'request': request}).data,
            'bookings': BookingSerializer(u.bookings.all().order_by('-created_at'), many=True, context={'request': request}).data,
            'packages': UserPackageSerializer(u.packages.all().order_by('-created_at'), many=True).data
        })

    def patch(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerUpdateSerializer(u, data=request.data, partial=True)
        if serializer.is_valid():
            u = serializer.save()
            return Response(UserProfileSerializer(u, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCustomerPassView(APIView):
    """Admin endpoint to issue or credit passes to a customer."""
    permission_classes = [IsAuthenticated, IsVerifiedStudioAdmin]

    def post(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = IssuePackagePassSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            package = UserPackage.objects.create(
                user=u,
                package_name=data['package_name'],
                total_sessions=data['total_sessions'],
                remaining_sessions=data['total_sessions'],
                valid_until=data['valid_until']
            )
            u_name = f"{u.first_name} {u.last_name}".strip() or u.username
            return Response({
                'message': f"Issued {data['total_sessions']} sessions ({data['package_name']}) to {u_name}.",
                'package': UserPackageSerializer(package).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
