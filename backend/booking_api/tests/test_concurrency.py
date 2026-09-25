import datetime
from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from booking_api.models import Service, TimeSlot, Booking

User = get_user_model()


class PessimisticConcurrencyBookingTestCase(TransactionTestCase):
    """
    Automated verification for CONC-001:
    Asserts pessimistic row locking guarantees ZERO overbooking under concurrent traffic.
    """

    def setUp(self):
        # 1. Create studio service
        self.service = Service.objects.create(
            slug='reformer-concurrency-test',
            title='Reformer Pilates Concurrency Test',
            category='Reformer',
            duration_minutes=60,
            price_kes=3500,
            price_eur=40,
            description='Test service for concurrent locking'
        )

        # 2. Create slot with exactly 1 remaining spot
        self.slot = TimeSlot.objects.create(
            service=self.service,
            slot_date=datetime.date.today() + datetime.timedelta(days=1),
            start_time='09:00 AM',
            period='Morning',
            location_name='Karen Sanctuary',
            total_capacity=1,
            spots_left=1,
            is_full=False
        )

        # 3. Create 10 distinct authenticated clients
        self.clients = []
        for i in range(10):
            user = User.objects.create_user(
                username=f'client_concurrency_{i}',
                email=f'client_{i}@test.com',
                password='Password123!'
            )
            refresh = RefreshToken.for_user(user)
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
            self.clients.append((user, client))

    def test_concurrent_bookings_for_single_spot_guarantees_exactly_one_winner(self):
        """10 simultaneous threads booking 1 remaining spot must yield exactly 1 success (201) and 9 conflicts (409)."""
        payload = {
            'service_id': str(self.service.id),
            'slot_id': str(self.slot.id),
            'payment_method': 'mpesa',
            'currency': 'KES',
            'notes': 'Concurrent stress test'
        }

        from django.db import close_old_connections

        def attempt_booking(client_tuple):
            close_old_connections()
            try:
                _, client = client_tuple
                return client.post('/api/bookings/', payload, format='json')
            finally:
                close_old_connections()

        # Execute 10 simultaneous requests in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            responses = list(executor.map(attempt_booking, self.clients))

        status_codes = [r.status_code for r in responses]
        success_count = status_codes.count(status.HTTP_201_CREATED)
        conflict_count = status_codes.count(status.HTTP_409_CONFLICT)

        # Assertions
        self.assertEqual(success_count, 1, f"Expected exactly 1 booking to succeed, but got {success_count}.")
        self.assertEqual(conflict_count, 9, f"Expected 9 conflicts (409), but got {conflict_count}.")

        # Database state assertions
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.spots_left, 0, "Slot spots_left must be 0.")
        self.assertTrue(self.slot.is_full, "Slot must be marked is_full = True.")

        # Ensure exactly 1 booking was created in the database
        db_bookings_count = Booking.objects.filter(slot=self.slot).count()
        self.assertEqual(db_bookings_count, 1, "Database must contain exactly 1 booking record for this slot.")
