import os
import secrets
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karina_backend.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@karinawellness.com')
admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not admin_password:
    admin_password = secrets.token_urlsafe(16)
    generated_pw = True
else:
    generated_pw = False

admin_user, created = User.objects.get_or_create(username=admin_username, defaults={
    'email': admin_email,
    'first_name': 'Karina',
    'last_name': 'Admin',
    'is_staff': True,
    'is_superuser': True
})

admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.email = admin_email
admin_user.set_password(admin_password)
admin_user.save()

token, _ = Token.objects.get_or_create(user=admin_user)

print(f"Superuser '{admin_username}' provisioned with staff & superuser privileges.")
if generated_pw:
    print(f"NOTICE: Temporary password generated: {admin_password}")
    print("Please change this password immediately in production.")
