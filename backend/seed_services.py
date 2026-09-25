import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karina_backend.settings')
django.setup()

from booking_api.supabase_client import get_supabase
from datetime import date, timedelta

sb = get_supabase()

new_services = [
    {
        'slug': 'sound-bath',
        'title': 'Restorative Sound Bath & Vibrational Therapy',
        'category': 'sound',
        'duration_minutes': 60,
        'location_type': 'all nairobi',
        'location_display': 'Karen Studio Sanctuary, Nairobi',
        'price_kes': 3500,
        'price_eur': 40,
        'image_url': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=800&q=80',
        'description': 'Immerse in Tibetan singing bowls, quartz crystal frequencies, and shamanic chimes designed to calm your central nervous system, lower cortisol, and restore deep delta-wave sleep.',
        'badge': 'Deep Rest',
        'capacity': 'Group (8–12)'
    },
    {
        'slug': 'holistic-vinyasa',
        'title': 'Holistic Vinyasa & Breathwork Flow',
        'category': 'yoga',
        'duration_minutes': 75,
        'location_type': 'all nairobi salzburg',
        'location_display': 'Solarium & Garden Deck, Karen',
        'price_kes': 3000,
        'price_eur': 32,
        'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80',
        'description': 'Dynamic alignment-focused vinyasa coupled with pranayama breath control to energize meridian channels, release fascia tension, and cultivate deep inner stillness.',
        'badge': 'Energizing',
        'capacity': 'Small Group (4–8)'
    },
    {
        'slug': 'deep-tissue-therapy',
        'title': 'Deep Tissue & Lymphatic Drainage Therapy',
        'category': 'therapy',
        'duration_minutes': 90,
        'location_type': 'all nairobi',
        'location_display': 'Private Healing Suite, Karen',
        'price_kes': 8500,
        'price_eur': 95,
        'image_url': 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80',
        'description': 'Therapeutic myofascial release targeting chronic muscular adhesions, paired with gentle lymphatic drainage and pure botanical essential oils tailored to your body.',
        'badge': 'Therapeutic',
        'capacity': 'Private 1:1'
    },
    {
        'slug': 'guided-meditation',
        'title': 'Guided Mindfulness & Somatic Meditation',
        'category': 'mindfulness',
        'duration_minutes': 45,
        'location_type': 'all online nairobi',
        'location_display': 'Sanctuary & Zoom Live',
        'price_kes': 2200,
        'price_eur': 25,
        'image_url': 'https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?auto=format&fit=crop&w=800&q=80',
        'description': 'Centering somatic grounding, vagus nerve regulation, and quiet mindful awareness designed to alleviate burnout, soothe tension, and cultivate emotional equilibrium.',
        'badge': 'Mindfulness',
        'capacity': 'Small Group or 1:1'
    }
]

existing = sb.table('services').select('slug, id').execute().data or []
existing_slug_map = {s['slug']: s['id'] for s in existing}

created_service_ids = {}

for s in new_services:
    slug = s['slug']
    if slug not in existing_slug_map:
        res = sb.table('services').insert(s).execute()
        if res.data:
            created_service_ids[slug] = res.data[0]['id']
            print(f"Added service: {s['title']} ({res.data[0]['id']})")
    else:
        created_service_ids[slug] = existing_slug_map[slug]
        print(f"Service already exists: {s['title']} ({existing_slug_map[slug]})")

# Also seed time slots for upcoming days for the new services
slots_to_insert = []
today = date.today()

sample_times = [
    ('08:00 AM', 'morning', 4),
    ('10:30 AM', 'morning', 6),
    ('02:00 PM', 'afternoon', 4),
    ('05:30 PM', 'evening', 8),
]

for i in range(1, 14): # next 14 days
    slot_date = str(today + timedelta(days=i))
    for slug, s_id in created_service_ids.items():
        for start_time, period, spots in sample_times[:2]: # 2 slots per day per service
            slots_to_insert.append({
                'service_id': s_id,
                'slot_date': slot_date,
                'start_time': start_time,
                'period': period,
                'location_name': 'Karen Studio, Nairobi',
                'spots_left': spots,
                'is_full': False,
                'waitlist_available': False
            })

if slots_to_insert:
    # Check if slots already exist for this date and service
    existing_slots = sb.table('time_slots').select('id, service_id, slot_date').eq('slot_date', str(today + timedelta(days=1))).execute().data or []
    existing_pair = {(es.get('service_id'), es.get('slot_date')) for es in existing_slots}
    
    fresh_slots = [sl for sl in slots_to_insert if (sl['service_id'], sl['slot_date']) not in existing_pair]
    if fresh_slots:
        # Batch insert in chunks of 50
        for chunk_start in range(0, len(fresh_slots), 50):
            chunk = fresh_slots[chunk_start:chunk_start+50]
            sb.table('time_slots').insert(chunk).execute()
        print(f"Inserted {len(fresh_slots)} initial scheduling slots for new services.")

print("Seed process complete.")
