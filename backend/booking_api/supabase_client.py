from django.conf import settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

_supabase_client: Client = None

def get_supabase() -> Client:
    """Returns singleton Supabase client."""
    global _supabase_client
    if _supabase_client is None:
        url = settings.SUPABASE_URL
        key = settings.SUPABASE_KEY
        _supabase_client = create_client(url, key)
    return _supabase_client

class SupabaseService:
    @staticmethod
    def get_services(category=None, location=None):
        supabase = get_supabase()
        query = supabase.table('services').select('*').order('created_at')
        if category and category != 'all':
            query = query.eq('category', category)
        response = query.execute()
        data = response.data or []
        if location and location != 'all':
            data = [s for s in data if location in s.get('location_type', '')]
        return data

    @staticmethod
    def get_service_by_id(service_id):
        supabase = get_supabase()
        response = supabase.table('services').select('*').eq('id', str(service_id)).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    def get_time_slots(service_id=None, date=None):
        supabase = get_supabase()
        query = supabase.table('time_slots').select('*').order('start_time')
        if service_id:
            query = query.eq('service_id', str(service_id))
        if date:
            query = query.eq('slot_date', str(date))
        response = query.execute()
        return response.data or []

    @staticmethod
    def get_bookings(user_name=None, status=None):
        supabase = get_supabase()
        query = supabase.table('bookings').select('*').order('booking_date', desc=False)
        if user_name:
            query = query.eq('user_name', user_name)
        if status and status != 'all':
            query = query.eq('status', status)
        response = query.execute()
        return response.data or []

    @staticmethod
    def create_booking(booking_data):
        supabase = get_supabase()
        response = supabase.table('bookings').insert(booking_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    def update_booking(booking_id, update_fields):
        supabase = get_supabase()
        response = supabase.table('bookings').update(update_fields).eq('id', str(booking_id)).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    def get_user_packages(user_name='Sarah'):
        supabase = get_supabase()
        response = supabase.table('user_packages').select('*').eq('user_name', user_name).execute()
        return response.data or []
