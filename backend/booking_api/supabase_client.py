import os
import logging
from django.conf import settings
from .models import Service, TimeSlot, Booking, UserPackage

logger = logging.getLogger(__name__)


def get_supabase():
    """
    Deprecated Supabase Client Stub.
    All data operations are now handled exclusively by PostgreSQL via Django ORM.
    """
    url = getattr(settings, 'SUPABASE_URL', os.getenv('SUPABASE_URL', ''))
    key = getattr(settings, 'SUPABASE_KEY', os.getenv('SUPABASE_KEY', ''))
    if not url or not key:
        logger.debug("Remote Supabase client disabled; using PostgreSQL engine.")
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception as e:
        logger.warning(f"Could not initialize legacy Supabase client: {e}")
        return None


class SupabaseService:
    """
    Backward-compatible PostgreSQL adapter for legacy calls.
    Directly interfaces with PostgreSQL via Django ORM.
    """
    @staticmethod
    def get_services(category=None, location=None):
        queryset = Service.objects.all().order_by('created_at')
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        if location and location != 'all':
            queryset = queryset.filter(location_type__icontains=location)
        return list(queryset.values())

    @staticmethod
    def get_service_by_id(service_id):
        s = Service.objects.filter(id=service_id).first()
        return s.__dict__ if s else None

    @staticmethod
    def update_booking(booking_id, update_fields):
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking:
            return None
        for key, val in update_fields.items():
            if hasattr(booking, key):
                setattr(booking, key, val)
        booking.save()
        return booking

    @staticmethod
    def get_user_packages(user_name='Sarah'):
        return list(UserPackage.objects.filter(user__username__iexact=user_name).values())
