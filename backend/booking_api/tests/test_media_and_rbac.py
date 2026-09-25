import io
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from booking_api.models import Service, TimeSlot

User = get_user_model()


def generate_test_image(filename="test.png", format="PNG", size=(100, 100)):
    """Helper to generate a valid in-memory image for upload testing."""
    file = io.BytesIO()
    image = Image.new("RGB", size, color=(120, 180, 140))
    image.save(file, format=format)
    file.seek(0)
    return SimpleUploadedFile(filename, file.read(), content_type=f"image/{format.lower()}")


class MediaAndRBACTestCase(TestCase):
    """
    Automated verification for MEDIA-001 and RBAC permissions:
    Asserts profile avatar upload/deletion, service image update, and role security.
    """

    def setUp(self):
        # 1. Regular Client
        self.client_user = User.objects.create_user(
            username='client_bob',
            email='bob@example.com',
            password='Password123!'
        )
        self.client_user.profile.role = 'client'
        self.client_user.profile.save()
        client_refresh = RefreshToken.for_user(self.client_user)
        self.client_token = str(client_refresh.access_token)
        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.client_token)

        # 2. Studio Admin
        self.admin_user = User.objects.create_user(
            username='admin_elena',
            email='elena@sanctuary.ke',
            password='AdminPassword123!',
            is_staff=True
        )
        self.admin_user.profile.role = 'studio_admin'
        self.admin_user.profile.save()
        admin_refresh = RefreshToken.for_user(self.admin_user)
        self.admin_token = str(admin_refresh.access_token)
        self.admin_api = APIClient()
        self.admin_api.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)

        # 3. Baseline service
        self.service = Service.objects.create(
            slug='sound-bath-test',
            title='Sound Bath Test',
            category='Sound',
            price_kes=4500,
            price_eur=50,
            description='Test service'
        )

    def test_client_avatar_upload_and_removal(self):
        """Authenticated client can upload profile picture and cleanly remove it."""
        test_file = generate_test_image("avatar.png", "PNG")
        response = self.api_client.post('/api/auth/profile/avatar/', {'avatar': test_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('avatar_url', response.data)
        self.assertIsNotNone(response.data['avatar_url'])

        self.client_user.refresh_from_db()
        self.assertTrue(bool(self.client_user.profile.avatar))

        # Delete avatar
        del_response = self.api_client.delete('/api/auth/profile/avatar/')
        self.assertEqual(del_response.status_code, status.HTTP_200_OK)
        self.client_user.refresh_from_db()
        self.assertFalse(bool(self.client_user.profile.avatar))

    def test_client_cannot_upload_service_image(self):
        """Regular client is forbidden from uploading service images (admin only)."""
        test_file = generate_test_image("service.png", "PNG")
        response = self.api_client.post(f'/api/admin/services/{self.service.id}/image/', {'image': test_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_upload_service_image(self):
        """Studio admin can successfully upload service photography."""
        test_file = generate_test_image("service_photo.jpg", "JPEG")
        response = self.admin_api.post(f'/api/admin/services/{self.service.id}/image/', {'image': test_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image_url', response.data)
        self.service.refresh_from_db()
        self.assertTrue(bool(self.service.image))
