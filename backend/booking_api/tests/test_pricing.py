import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from booking_api.models import Service, TimeSlot, Booking

User = get_user_model()


class AuthoritativePricingTestCase(TestCase):
    """
    Automated verification for SEC-006:
    Asserts client price tampering payloads (e.g. total_amount=1) are ignored and
    authoritative catalog prices are enforced by the server.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='client_alice',
            email='alice@example.com',
            password='Password123!'
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.service = Service.objects.create(
            slug='authoritative-reformer',
            title='Authoritative Reformer Class',
            category='Reformer',
            duration_minutes=60,
            price_kes=3500,
            price_eur=40,
            description='Test authoritative pricing'
        )

        self.slot = TimeSlot.objects.create(
            service=self.service,
            slot_date=datetime.date.today() + datetime.timedelta(days=2),
            start_time='10:00 AM',
            period='Morning',
            location_name='Karen Sanctuary',
            total_capacity=5,
            spots_left=5,
            is_full=False
        )

    def test_client_price_tampering_payload_is_overridden_by_server_price(self):
        """Even if the client sends total_amount: 1 KES, the server must charge 3,500 KES."""
        tampered_payload = {
            'service_id': str(self.service.id),
            'slot_id': str(self.slot.id),
            'payment_method': 'mpesa',
            'currency': 'KES',
            'total_amount': 1,  # Malicious price tampering attempt
            'notes': 'Attempting to book 3,500 KES session for 1 KES'
        }

        response = self.client.post('/api/bookings/', tampered_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_amount'], 3500, "Server must charge authoritative 3,500 KES.")

        # Verify database record
        booking_id = response.data['id']
        booking = Booking.objects.get(id=booking_id)
        self.assertEqual(booking.total_amount, 3500, "Database record must store 3,500 KES, not tampered 1 KES.")

    def test_eur_currency_authoritative_price_is_enforced(self):
        """When currency is EUR, server must authoritatively charge 40 EUR."""
        payload = {
            'service_id': str(self.service.id),
            'slot_id': str(self.slot.id),
            'payment_method': 'card',
            'currency': 'EUR',
            'total_amount': 5  # Malicious price tampering attempt
        }

        response = self.client.post('/api/bookings/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_amount'], 40, "Server must charge authoritative 40 EUR.")
