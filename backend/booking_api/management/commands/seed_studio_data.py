import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from booking_api.models import User, Service, TimeSlot, UserPackage


class Command(BaseCommand):
    help = 'Seeds initial studio services, upcoming time slots, and default studio admin account'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting studio data seeding...'))

        # 1. Seed or update studio admin account
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@karinawellness.com',
                'first_name': 'Karina',
                'last_name': 'Director',
                'role': User.Role.STUDIO_ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'phone': '+254 700 000 000',
                'bio': 'Founder & Master Movement Practitioner at Karina Wellness Sanctuary.'
            }
        )
        if created:
            admin_user.set_password('AdminSecure2026!')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created studio administrator: admin / AdminSecure2026!'))
        else:
            self.stdout.write(self.style.SUCCESS('Studio administrator account already exists.'))

        # 2. Seed baseline services
        services_data = [
            {
                'slug': 'reformer-pilates',
                'title': 'Reformer Pilates',
                'category': 'Reformer',
                'duration_minutes': 60,
                'location_type': 'all nairobi',
                'location_display': 'Karen Studio Sanctuary, Nairobi',
                'price_kes': 3500,
                'price_eur': 40,
                'image_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80',
                'description': 'Dynamic athletic conditioning, core recruitment, and somatic alignment utilizing state-of-the-art reformer carriages.',
                'badge': 'Signature Practice',
                'capacity': 'Intimate Group (4–6)'
            },
            {
                'slug': 'somatic-movement',
                'title': 'Somatic Movement & Breathwork',
                'category': 'Somatic',
                'duration_minutes': 75,
                'location_type': 'all nairobi',
                'location_display': 'Karen Studio Sanctuary, Nairobi',
                'price_kes': 4000,
                'price_eur': 45,
                'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80',
                'description': 'Nervous system down-regulation, polyvagal reset, fascial unwinding, and guided therapeutic breathwork.',
                'badge': 'Nervous System Reset',
                'capacity': 'Small Group (6–8)'
            },
            {
                'slug': 'sound-sanctuary',
                'title': 'Sound Sanctuary & Restorative Yin',
                'category': 'Sound',
                'duration_minutes': 90,
                'location_type': 'all nairobi',
                'location_display': 'Karen Studio Sanctuary, Nairobi',
                'price_kes': 4500,
                'price_eur': 50,
                'image_url': 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?auto=format&fit=crop&w=800&q=80',
                'description': 'Multi-tonal acoustic sound immersion featuring planetary gongs and alchemy crystal bowls paired with long-held passive yin postures.',
                'badge': 'Deep Restoration',
                'capacity': 'Sanctuary Group (8–10)'
            },
            {
                'slug': 'pelvic-floor-health',
                'title': 'Clinical Pelvic Floor & Postpartum',
                'category': 'Clinical',
                'duration_minutes': 60,
                'location_type': 'all nairobi',
                'location_display': 'Karen Studio Sanctuary, Nairobi',
                'price_kes': 5000,
                'price_eur': 55,
                'image_url': 'https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?auto=format&fit=crop&w=800&q=80',
                'description': 'Specialized physiological restoration tailored to female endocrine transitions, prenatal readiness, and postpartum recovery.',
                'badge': 'Clinical Specialist',
                'capacity': 'Semi-Private (4 Max)'
            }
        ]

        created_services = []
        for s_data in services_data:
            service, s_created = Service.objects.update_or_create(
                slug=s_data['slug'],
                defaults=s_data
            )
            created_services.append(service)
            status_text = 'Created' if s_created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f"{status_text} service: {service.title}"))

        # 3. Seed upcoming slots for the next 7 days
        today = timezone.localdate()
        daily_schedule = [
            ('08:00 AM', 'Morning', 4),
            ('09:30 AM', 'Morning', 6),
            ('11:00 AM', 'Morning', 6),
            ('02:00 PM', 'Afternoon', 4),
            ('04:30 PM', 'Afternoon', 6),
            ('06:00 PM', 'Evening', 8)
        ]

        slots_created_count = 0
        for day_offset in range(1, 8):
            slot_date = today + datetime.timedelta(days=day_offset)
            for service in created_services:
                for time_str, period, cap in daily_schedule:
                    slot, sl_created = TimeSlot.objects.get_or_create(
                        service=service,
                        slot_date=slot_date,
                        start_time=time_str,
                        defaults={
                            'period': period,
                            'location_name': 'Karen Sanctuary, Nairobi',
                            'total_capacity': cap,
                            'spots_left': cap,
                            'is_full': False,
                            'session_theme': f"{service.title} - Sanctuary Flow"
                        }
                    )
                    if sl_created:
                        slots_created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {slots_created_count} schedule slots across next 7 days."))
        self.stdout.write(self.style.SUCCESS("Studio data seeding completed successfully!"))
