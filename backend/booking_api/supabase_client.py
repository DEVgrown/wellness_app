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
    def create_service(service_data):
        supabase = get_supabase()
        response = supabase.table('services').insert(service_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    def update_service(service_id, update_fields):
        supabase = get_supabase()
        response = supabase.table('services').update(update_fields).eq('id', str(service_id)).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    def delete_service(service_id):
        supabase = get_supabase()
        # Clean up related slots first if any
        try:
            supabase.table('time_slots').delete().eq('service_id', str(service_id)).execute()
        except Exception as e:
            logger.warning(f"Error cascading slots deletion for service {service_id}: {e}")
        response = supabase.table('services').delete().eq('id', str(service_id)).execute()
        return response.data

    @staticmethod
    def get_time_slots(service_id=None, date=None, date_from=None, date_to=None):
        supabase = get_supabase()
        query = supabase.table('time_slots').select('*').order('slot_date').order('start_time')
        if service_id:
            query = query.eq('service_id', str(service_id))
        if date:
            query = query.eq('slot_date', str(date))
        if date_from:
            query = query.gte('slot_date', str(date_from))
        if date_to:
            query = query.lte('slot_date', str(date_to))
        response = query.execute()
        return response.data or []

    @staticmethod
    def create_time_slot(slot_data):
        supabase = get_supabase()
        response = supabase.table('time_slots').insert(slot_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    def bulk_create_time_slots(slots_list):
        supabase = get_supabase()
        if not slots_list:
            return []
        created_all = []
        # Chunk into batches of 50
        for i in range(0, len(slots_list), 50):
            chunk = slots_list[i:i+50]
            response = supabase.table('time_slots').insert(chunk).execute()
            if response.data:
                created_all.extend(response.data)
        return created_all

    @staticmethod
    def update_time_slot(slot_id, update_fields):
        supabase = get_supabase()
        response = supabase.table('time_slots').update(update_fields).eq('id', str(slot_id)).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    def delete_time_slot(slot_id):
        supabase = get_supabase()
        response = supabase.table('time_slots').delete().eq('id', str(slot_id)).execute()
        return response.data

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
    def get_all_bookings(status=None, date=None, service_id=None, search=None):
        supabase = get_supabase()
        query = supabase.table('bookings').select('*').order('created_at', desc=True)
        if status and status != 'all':
            query = query.eq('status', status)
        if date:
            query = query.eq('booking_date', str(date))
        if service_id:
            query = query.eq('service_id', str(service_id))
        response = query.execute()
        data = response.data or []
        if search:
            s_lower = search.lower().strip()
            data = [
                b for b in data
                if s_lower in (b.get('user_name') or '').lower()
                or s_lower in (b.get('user_email') or '').lower()
                or s_lower in (b.get('payment_reference') or '').lower()
                or s_lower in (b.get('service_title') or '').lower()
                or s_lower in (b.get('user_phone') or '').lower()
            ]
        return data

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
    def delete_booking(booking_id):
        supabase = get_supabase()
        response = supabase.table('bookings').delete().eq('id', str(booking_id)).execute()
        return response.data

    @staticmethod
    def get_user_packages(user_name='Sarah'):
        supabase = get_supabase()
        response = supabase.table('user_packages').select('*').eq('user_name', user_name).execute()
        return response.data or []

    @staticmethod
    def create_user_package(package_data):
        supabase = get_supabase()
        response = supabase.table('user_packages').insert(package_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    def delete_user_package(package_id):
        supabase = get_supabase()
        response = supabase.table('user_packages').delete().eq('id', str(package_id)).execute()
        return response.data

    @staticmethod
    def get_admin_metrics():
        supabase = get_supabase()
        services = supabase.table('services').select('id, category, price_kes, price_eur').execute().data or []
        slots = supabase.table('time_slots').select('id, slot_date, is_full, spots_left').execute().data or []
        bookings = supabase.table('bookings').select('*').execute().data or []

        revenue_kes = sum(b.get('total_amount', 0) for b in bookings if b.get('currency') == 'KES' and b.get('status') != 'cancelled')
        revenue_eur = sum(b.get('total_amount', 0) for b in bookings if b.get('currency') == 'EUR' and b.get('status') != 'cancelled')
        confirmed_count = sum(1 for b in bookings if b.get('status') == 'confirmed')
        completed_count = sum(1 for b in bookings if b.get('status') == 'completed')
        cancelled_count = sum(1 for b in bookings if b.get('status') == 'cancelled')
        
        return {
            'total_services': len(services),
            'total_slots': len(slots),
            'total_bookings': len(bookings),
            'confirmed_bookings': confirmed_count,
            'completed_bookings': completed_count,
            'cancelled_bookings': cancelled_count,
            'revenue_kes': revenue_kes,
            'revenue_eur': revenue_eur,
        }

