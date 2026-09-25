import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karina_backend.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Ensure an admin superuser exists
admin_user, created = User.objects.get_or_create(username='admin', defaults={
    'email': 'admin@karinawellness.com',
    'first_name': 'Karina',
    'last_name': 'Admin',
    'is_staff': True,
    'is_superuser': True
})

admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.set_password('admin123')
admin_user.save()

token, _ = Token.objects.get_or_create(user=admin_user)

# Also grant staff to elena_karina if present
try:
    elena = User.objects.get(username='elena_karina')
    elena.is_staff = True
    elena.is_superuser = True
    elena.save()
    Token.objects.get_or_create(user=elena)
    print("Granted admin access to elena_karina.")
except User.DoesNotExist:
    pass

print(f"Admin user verified: username='admin', password='admin123', Token='{token.key}'")
