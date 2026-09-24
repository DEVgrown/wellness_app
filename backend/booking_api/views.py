import random
import string
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .supabase_client import SupabaseService
from .serializers import (
    ServiceSerializer,
    TimeSlotSerializer,
    BookingSerializer,
    BookingCreateSerializer,
    RescheduleBookingSerializer,
    MpesaPaymentSerializer,
    UserPackageSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)
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

