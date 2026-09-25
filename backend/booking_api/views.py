import random
import string
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .supabase_client import SupabaseService, get_supabase
from django.contrib.auth.models import User
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
    UserProfileSerializer
)
from datetime import datetime, timedelta, date
from .tasks import process_mpesa_payment_task, send_booking_confirmation_task

logger = logging.getLogger(__name__)

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

class ApiRootView(APIView):
    """Karina Wellness Booking Platform API Directory."""
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            'message': 'Welcome to Karina Wellness Booking API (Connected to Supabase)',
            'endpoints': {
                'services': request.build_absolute_uri('services/'),
                'slots': request.build_absolute_uri('slots/'),
                'bookings': request.build_absolute_uri('bookings/'),
                'mpesa_stk_push': request.build_absolute_uri('payments/mpesa-stk/'),
                'user_packages': request.build_absolute_uri('user-packages/'),
                'auth_signup': request.build_absolute_uri('auth/signup/'),
                'auth_login': request.build_absolute_uri('auth/login/'),
                'auth_logout': request.build_absolute_uri('auth/logout/'),
                'auth_me': request.build_absolute_uri('auth/me/'),
            },
            'database': 'Remote Supabase (Booking-Karina)',
            'frontend_url': 'http://localhost:5173/'
        })

class ServiceListView(APIView):
    """List services with optional category and location filtering."""
    def get(self, request):
        category = request.query_params.get('category', 'all')
        location = request.query_params.get('location', 'all')
        services = SupabaseService.get_services(category=category, location=location)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

class ServiceDetailView(APIView):
    """Retrieve details for a single service."""
    def get(self, request, pk):
        service = SupabaseService.get_service_by_id(pk)
        if not service:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

class TimeSlotListView(APIView):
    """Retrieve time slots by date and service."""
    def get(self, request):
        service_id = request.query_params.get('service_id')
        date = request.query_params.get('date', '2024-10-26')
        slots = SupabaseService.get_time_slots(service_id=service_id, date=date)
        serializer = TimeSlotSerializer(slots, many=True)
        return Response(serializer.data)

class BookingListCreateView(APIView):
    """List user bookings or create a new booking."""
    def get(self, request):
        user_name = request.query_params.get('user_name', 'Sarah')
        booking_status = request.query_params.get('status', 'all')
        bookings = SupabaseService.get_bookings(user_name=user_name, status=booking_status)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Generate reference
            payment_method = data.get('payment_method', 'mpesa')
            ref = 'QK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            booking_payload = {
                'service_id': str(data['service_id']) if data.get('service_id') else None,
                'service_title': data['service_title'],
                'user_name': data.get('user_name', 'Sarah'),
                'user_email': data.get('user_email', 'sarah@example.com'),
                'user_phone': data.get('user_phone', '+254 712 345 678'),
                'booking_date': str(data['booking_date']),
                'time_slot': data['time_slot'],
                'location_name': data.get('location_name', 'Karen Studio, Nairobi'),
                'status': 'confirmed',
                'payment_method': payment_method,
                'payment_reference': ref,
                'currency': data.get('currency', 'KES'),
                'total_amount': data['total_amount'],
                'notes': data.get('notes', ''),
            }
            
            created = SupabaseService.create_booking(booking_payload)
            if not created:
                return Response({'error': 'Failed to save booking to Supabase'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Trigger Celery confirmation task asynchronously (with graceful local fallback)
            try:
                send_booking_confirmation_task.delay(
                    booking_id=created['id'],
                    user_email=created['user_email'],
                    service_title=created['service_title'],
                    booking_date=created['booking_date'],
                    time_slot=created['time_slot']
                )
            except Exception as e:
                logger.warning(f"Celery dispatch failed (running synchronously/offline): {e}")

            out_serializer = BookingSerializer(created)
            return Response(out_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingCancelView(APIView):
    """Cancel an active booking."""
    def post(self, request, pk):
        updated = SupabaseService.update_booking(pk, {
            'status': 'cancelled',
            'notes': 'Cancelled by client. M-Pesa refund scheduled.'
        })
        if not updated:
            return Response({'error': 'Booking not found or cannot be cancelled'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookingSerializer(updated)
        return Response(serializer.data)

class BookingRescheduleView(APIView):
    """Reschedule an active booking."""
    def post(self, request, pk):
        serializer = RescheduleBookingSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            updated = SupabaseService.update_booking(pk, {
                'booking_date': str(data['booking_date']),
                'time_slot': data['time_slot']
            })
            if not updated:
                return Response({'error': 'Booking not found or cannot be rescheduled'}, status=status.HTTP_404_NOT_FOUND)
            out_serializer = BookingSerializer(updated)
            return Response(out_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MpesaSTKPushView(APIView):
    """Trigger Safaricom M-Pesa STK Push simulation."""
    def post(self, request):
        serializer = MpesaPaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            booking_id = data.get('booking_id')
            phone = data['phone_number']
            amount = data['amount']
            
            ref = 'QK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            # Attempt to queue task in Celery
            task_id = None
            try:
                async_res = process_mpesa_payment_task.delay(booking_id, phone, amount)
                task_id = async_res.id
            except Exception as e:
                logger.warning(f"Celery queue unavailable, falling back to direct acknowledgment: {e}")
            
            return Response({
                'success': True,
                'status': 'INITIATED',
                'message': f'STK Push prompt sent to {phone}. Please check your phone and enter M-Pesa PIN.',
                'checkout_request_id': f'ws_CO_{ref}',
                'receipt_reference': ref,
                'task_id': task_id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPackageView(APIView):
    """Retrieve active passes and packages."""
    def get(self, request):
        user_name = request.query_params.get('user_name', 'Sarah')
        packages = SupabaseService.get_user_packages(user_name=user_name)
        serializer = UserPackageSerializer(packages, many=True)
        return Response(serializer.data)

class SignUpView(APIView):
    """Register a new user, create auth token, and initialize user session."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            
            # Seed a complimentary starter pass in Supabase if desired
            try:
                display_name = f"{user.first_name} {user.last_name}".strip() or user.username
                # Check if package exists, or seed one
                SupabaseService.get_client().table('user_packages').insert({
                    'user_name': display_name,
                    'package_name': 'Welcome Complimentary Pass',
                    'total_sessions': 1,
                    'remaining_sessions': 1,
                    'valid_until': '30 Nov 2026'
                }).execute()
            except Exception as e:
                logger.warning(f"Could not seed starter package for {user.username}: {e}")

            return Response({
                'token': token.key,
                'user': UserProfileSerializer(user).data,
                'message': 'Account created successfully! Welcome to Karina Wellness.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """Authenticate user with username/email and password."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserProfileSerializer(user).data,
                'message': f'Welcome back, {user.first_name or user.username}!'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """Log out user by invalidating the active auth token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """Get current authenticated user profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'user': UserProfileSerializer(request.user).data
        })


# ==========================================
# ADMIN FUNCTIONALITIES & DASHBOARD VIEWS
# ==========================================

class AdminOverviewView(APIView):
    """KPI Metrics and live analytics for Admin Dashboard."""
    permission_classes = [AllowAny]

    def get(self, request):
        metrics = SupabaseService.get_admin_metrics()
        recent_bookings = SupabaseService.get_all_bookings()[:6]
        return Response({
            'metrics': metrics,
            'recent_bookings': BookingSerializer(recent_bookings, many=True).data
        })


class AdminServiceListCreateView(APIView):
    """Admin endpoint to list all services and create new offerings."""
    permission_classes = [AllowAny]

    def get(self, request):
        services = SupabaseService.get_services(category='all', location='all')
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            slug = data.get('slug')
            if not slug:
                # Generate clean slug from title
                import re
                slug = re.sub(r'[^a-zA-Z0-9]+', '-', data['title'].strip().lower()).strip('-')
            
            payload = {
                'title': data['title'],
                'slug': slug,
                'category': data['category'],
                'duration_minutes': data.get('duration_minutes', 60),
                'location_type': data.get('location_type', 'all nairobi'),
                'location_display': data.get('location_display', 'Karen Studio Sanctuary, Nairobi'),
                'price_kes': data.get('price_kes', 3500),
                'price_eur': data.get('price_eur', 40),
                'image_url': data.get('image_url') or 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80',
                'description': data['description'],
                'badge': data.get('badge', ''),
                'capacity': data.get('capacity', 'Small Group (4–8)')
            }
            created = SupabaseService.create_service(payload)
            if not created:
                return Response({'error': 'Failed to create service in database'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(ServiceSerializer(created).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminServiceDetailView(APIView):
    """Admin endpoint to retrieve, update, or remove a service."""
    permission_classes = [AllowAny]

    def get(self, request, pk):
        service = SupabaseService.get_service_by_id(pk)
        if not service:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ServiceSerializer(service).data)

    def put(self, request, pk):
        return self.patch(request, pk)

    def patch(self, request, pk):
        serializer = ServiceCreateUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated = SupabaseService.update_service(pk, serializer.validated_data)
            if not updated:
                return Response({'error': 'Service could not be updated or not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(ServiceSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deleted = SupabaseService.delete_service(pk)
        return Response({'message': 'Service and corresponding slots deleted successfully', 'data': deleted}, status=status.HTTP_200_OK)


class AdminTimeSlotListCreateView(APIView):
    """Admin endpoint to query time slots across services and dates or create a slot."""
    permission_classes = [AllowAny]

    def get(self, request):
        service_id = request.query_params.get('service_id')
        date_param = request.query_params.get('date')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        slots = SupabaseService.get_time_slots(
            service_id=service_id if service_id and service_id != 'all' else None,
            date=date_param,
            date_from=date_from,
            date_to=date_to
        )
        return Response(TimeSlotSerializer(slots, many=True).data)

    def post(self, request):
        serializer = TimeSlotCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            payload = {
                'service_id': data.get('service_id') or None,
                'slot_date': str(data['slot_date']),
                'start_time': data['start_time'],
                'period': data.get('period', 'morning'),
                'location_name': data.get('location_name', 'Karen Studio, Nairobi'),
                'spots_left': data.get('spots_left', 4),
                'is_full': data.get('is_full', False),
                'waitlist_available': data.get('waitlist_available', False)
            }
            created = SupabaseService.create_time_slot(payload)
            if not created:
                return Response({'error': 'Failed to create time slot'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(TimeSlotSerializer(created).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminTimeSlotBulkCreateView(APIView):
    """Admin endpoint to bulk-generate recurring weekly slots across a date range."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BulkSlotGenerateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            start_date = data['start_date']
            end_date = data['end_date']
            days_of_week = set(data['days_of_week'])  # 0=Monday, 6=Sunday
            times_list = data['times']  # list of dicts: [{'start_time': '08:00 AM', 'period': 'morning'}, ...]
            service_id = data.get('service_id') or None
            location_name = data.get('location_name', 'Karen Studio, Nairobi')
            spots_left = data.get('spots_left', 4)

            if end_date < start_date:
                return Response({'error': 'end_date must be after start_date'}, status=status.HTTP_400_BAD_REQUEST)

            slots_to_create = []
            curr = start_date
            while curr <= end_date:
                if curr.weekday() in days_of_week:
                    for t in times_list:
                        start_time = t.get('start_time', '09:00 AM')
                        period = t.get('period', 'morning')
                        slots_to_create.append({
                            'service_id': str(service_id) if service_id else None,
                            'slot_date': str(curr),
                            'start_time': start_time,
                            'period': period,
                            'location_name': location_name,
                            'spots_left': spots_left,
                            'is_full': False,
                            'waitlist_available': False
                        })
                curr += timedelta(days=1)

            created_slots = SupabaseService.bulk_create_time_slots(slots_to_create)
            return Response({
                'message': f'Successfully generated {len(created_slots)} session slots across selected dates.',
                'count': len(created_slots),
                'slots': TimeSlotSerializer(created_slots[:20], many=True).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminTimeSlotDetailView(APIView):
    """Admin endpoint to edit or delete a time slot."""
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        serializer = TimeSlotCreateUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            clean_data = {}
            for k, v in serializer.validated_data.items():
                if k == 'slot_date':
                    clean_data[k] = str(v)
                elif k == 'service_id':
                    clean_data[k] = str(v) if v else None
                else:
                    clean_data[k] = v
            updated = SupabaseService.update_time_slot(pk, clean_data)
            if not updated:
                return Response({'error': 'Time slot not found or update failed'}, status=status.HTTP_404_NOT_FOUND)
            return Response(TimeSlotSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deleted = SupabaseService.delete_time_slot(pk)
        return Response({'message': 'Time slot deleted successfully', 'data': deleted}, status=status.HTTP_200_OK)


class AdminBookingListView(APIView):
    """Admin endpoint to view and filter all attendee bookings."""
    permission_classes = [AllowAny]

    def get(self, request):
        status_filter = request.query_params.get('status', 'all')
        date_filter = request.query_params.get('date')
        service_id = request.query_params.get('service_id')
        search_query = request.query_params.get('search')

        bookings = SupabaseService.get_all_bookings(
            status=status_filter,
            date=date_filter,
            service_id=service_id,
            search=search_query
        )
        return Response(BookingSerializer(bookings, many=True).data)


class AdminBookingDetailView(APIView):
    """Admin endpoint to modify booking status, reschedule, add coach notes, or delete."""
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        serializer = AdminBookingUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            clean_data = {}
            for k, v in serializer.validated_data.items():
                if k == 'booking_date':
                    clean_data[k] = str(v)
                else:
                    clean_data[k] = v
            updated = SupabaseService.update_booking(pk, clean_data)
            if not updated:
                return Response({'error': 'Booking not found or update failed'}, status=status.HTTP_404_NOT_FOUND)
            return Response(BookingSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deleted = SupabaseService.delete_booking(pk)
        return Response({'message': 'Booking deleted successfully', 'data': deleted}, status=status.HTTP_200_OK)


# ==========================================
# ADMIN CUSTOMER & USER MANAGEMENT VIEWS
# ==========================================

class AdminCustomerListView(APIView):
    """Admin endpoint to retrieve all registered customers with aggregate stats or manually onboard new clients."""
    permission_classes = [AllowAny]

    def get(self, request):
        search_query = request.query_params.get('search', '').lower().strip()
        status_filter = request.query_params.get('status', 'all')

        users = User.objects.all().order_by('-date_joined')
        all_bookings = SupabaseService.get_all_bookings()
        all_packages = get_supabase().table('user_packages').select('*').execute().data or []

        # Index bookings by email and username
        bookings_by_email = {}
        bookings_by_name = {}
        for b in all_bookings:
            em = (b.get('user_email') or '').lower().strip()
            nm = (b.get('user_name') or '').lower().strip()
            if em:
                bookings_by_email.setdefault(em, []).append(b)
            if nm:
                bookings_by_name.setdefault(nm, []).append(b)

        # Index packages by username
        packages_by_name = {}
        for p in all_packages:
            nm = (p.get('user_name') or '').lower().strip()
            if nm:
                packages_by_name.setdefault(nm, []).append(p)

        customers_data = []
        for u in users:
            u_name = f"{u.first_name} {u.last_name}".strip() or u.username
            u_email = (u.email or '').lower().strip()
            u_username = u.username.lower().strip()

            # Find matching bookings
            matched_bookings = bookings_by_email.get(u_email, [])
            if not matched_bookings:
                matched_bookings = bookings_by_name.get(u_name.lower(), [])
            if not matched_bookings:
                matched_bookings = bookings_by_name.get(u_username, [])

            # Find matching packages
            matched_packages = packages_by_name.get(u_name.lower(), [])
            if not matched_packages:
                matched_packages = packages_by_name.get(u_username, [])

            total_spend_kes = sum(b.get('total_amount', 0) for b in matched_bookings if b.get('currency') == 'KES' and b.get('status') != 'cancelled')
            total_spend_eur = sum(b.get('total_amount', 0) for b in matched_bookings if b.get('currency') == 'EUR' and b.get('status') != 'cancelled')
            completed_count = sum(1 for b in matched_bookings if b.get('status') == 'completed')
            confirmed_count = sum(1 for b in matched_bookings if b.get('status') == 'confirmed')
            active_passes = sum(p.get('remaining_sessions', 0) for p in matched_packages)

            phone = matched_bookings[0].get('user_phone') if matched_bookings else ''

            customer_obj = {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'name': u_name,
                'phone': phone,
                'is_staff': u.is_staff,
                'is_superuser': u.is_superuser,
                'is_active': u.is_active,
                'date_joined': u.date_joined.strftime('%Y-%m-%d %H:%M') if u.date_joined else '',
                'total_bookings': len(matched_bookings),
                'completed_bookings': completed_count,
                'confirmed_bookings': confirmed_count,
                'total_spend_kes': total_spend_kes,
                'total_spend_eur': total_spend_eur,
                'active_passes': active_passes,
                'packages_count': len(matched_packages)
            }

            # Search filter
            if search_query:
                haystack = f"{u.username} {u_name} {u.email} {phone}".lower()
                if search_query not in haystack:
                    continue

            # Status filter
            if status_filter == 'staff' and not u.is_staff:
                continue
            elif status_filter == 'active_bookers' and len(matched_bookings) == 0:
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
            Token.objects.get_or_create(user=user)

            # Seed a complimentary starter pass
            try:
                display_name = f"{user.first_name} {user.last_name}".strip() or user.username
                SupabaseService.create_user_package({
                    'user_name': display_name,
                    'package_name': 'Welcome Complimentary Pass',
                    'total_sessions': 1,
                    'remaining_sessions': 1,
                    'valid_until': '31 Dec 2026'
                })
            except Exception as e:
                logger.warning(f"Could not seed initial pass for customer {user.username}: {e}")

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
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        u_name = f"{u.first_name} {u.last_name}".strip() or u.username
        u_email = (u.email or '').lower().strip()
        all_bookings = SupabaseService.get_all_bookings()
        
        # Match bookings by email or name
        customer_bookings = [
            b for b in all_bookings
            if (b.get('user_email') or '').lower().strip() == u_email
            or (b.get('user_name') or '').lower().strip() == u_name.lower()
            or (b.get('user_name') or '').lower().strip() == u.username.lower()
        ]

        packages = SupabaseService.get_user_packages(user_name=u_name)
        if not packages:
            packages = SupabaseService.get_user_packages(user_name=u.username)

        return Response({
            'user': UserProfileSerializer(u).data,
            'bookings': BookingSerializer(customer_bookings, many=True).data,
            'packages': UserPackageSerializer(packages, many=True).data
        })

    def patch(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data
            if 'first_name' in data:
                u.first_name = data['first_name']
            if 'last_name' in data:
                u.last_name = data['last_name']
            if 'email' in data:
                u.email = data['email']
            if 'is_active' in data:
                u.is_active = data['is_active']
            if 'is_staff' in data:
                u.is_staff = data['is_staff']
            u.save()
            return Response(UserProfileSerializer(u).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCustomerPassView(APIView):
    """Admin endpoint to issue or credit passes to a customer."""
    permission_classes = [AllowAny]

    def post(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = IssuePackagePassSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            u_name = f"{u.first_name} {u.last_name}".strip() or u.username
            payload = {
                'user_name': u_name,
                'package_name': data['package_name'],
                'total_sessions': data['total_sessions'],
                'remaining_sessions': data['total_sessions'],
                'valid_until': data['valid_until']
            }
            created = SupabaseService.create_user_package(payload)
            return Response({
                'message': f"Issued {data['total_sessions']} sessions ({data['package_name']}) to {u_name}.",
                'package': created
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



