import uuid
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class AdminPermissionSecurityTestCase(APITestCase):
    """
    Automated security verification for SEC-001:
    Asserts all administrative endpoints strictly enforce IsAuthenticated and IsVerifiedStudioAdmin.
    """

    def setUp(self):
        # Create regular non-staff member
        self.client_user = User.objects.create_user(
            username='client_sarah',
            email='sarah@example.com',
            password='TestPassword123!',
            is_staff=False,
            is_superuser=False
        )
        self.client_token = Token.objects.create(user=self.client_user)

        # Create verified studio admin
        self.admin_user = User.objects.create_user(
            username='admin_karina',
            email='karina@sanctuary.ke',
            password='AdminPassword123!',
            is_staff=True,
            is_superuser=False
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

        self.dummy_uuid = str(uuid.uuid4())
        self.dummy_int = self.client_user.id

        # List of all 11 admin endpoints to test
        self.admin_endpoints = [
            ('GET', '/api/admin/overview/'),
            ('GET', '/api/admin/services/'),
            ('GET', f'/api/admin/services/{self.dummy_uuid}/'),
            ('GET', '/api/admin/slots/'),
            ('POST', '/api/admin/slots/bulk-generate/'),
            ('PATCH', f'/api/admin/slots/{self.dummy_uuid}/'),
            ('GET', '/api/admin/bookings/'),
            ('PATCH', f'/api/admin/bookings/{self.dummy_uuid}/'),
            ('GET', '/api/admin/customers/'),
            ('GET', f'/api/admin/customers/{self.dummy_int}/'),
            ('POST', f'/api/admin/customers/{self.dummy_int}/passes/'),
        ]

    def test_unauthenticated_requests_receive_401(self):
        """Unauthenticated requests must be rejected with 401 Unauthorized across all admin endpoints."""
        self.client.credentials()  # Clear credentials
        for method, endpoint in self.admin_endpoints:
            if method == 'GET':
                response = self.client.get(endpoint)
            elif method == 'POST':
                response = self.client.post(endpoint, {})
            elif method == 'PATCH':
                response = self.client.patch(endpoint, {})
            
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {endpoint} should require authentication (returned {response.status_code})"
            )

    def test_non_staff_authenticated_client_receives_403(self):
        """Regular authenticated users without staff flag must receive 403 Forbidden."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.client_token.key)
        for method, endpoint in self.admin_endpoints:
            if method == 'GET':
                response = self.client.get(endpoint)
            elif method == 'POST':
                response = self.client.post(endpoint, {})
            elif method == 'PATCH':
                response = self.client.patch(endpoint, {})
            
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
                f"Endpoint {endpoint} should forbid non-staff access (returned {response.status_code})"
            )

    def test_staff_admin_can_access_permission_check(self):
        """Staff administrators must bypass permission denial (must not receive 401 or 403)."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        # Check endpoint permissions are granted for overview
        response = self.client.get('/api/admin/overview/')
        self.assertNotIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
            f"Staff administrator should have permission to access /api/admin/overview/"
        )
