import uuid
import os
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


def user_avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    user_id = instance.user_id if hasattr(instance, 'user_id') else instance.id
    return f"avatars/user_{user_id}/{uuid.uuid4().hex[:12]}.{ext}"


def service_image_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    slug_id = instance.slug or str(instance.id)[:8]
    return f"services/{slug_id}/{uuid.uuid4().hex[:12]}.{ext}"


def session_banner_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    return f"sessions/{instance.id}/{uuid.uuid4().hex[:12]}.{ext}"


class UserProfile(models.Model):
    """
    User Profile extending Django's standard User model to support
    granular Role-Based Access Control (RBAC), wellness bio, contact, and somatic notes.
    """
    class Role(models.TextChoices):
        CLIENT = 'client', 'Client / Member'
        COACH = 'coach', 'Coach / Practitioner'
        STUDIO_ADMIN = 'studio_admin', 'Studio Administrator'
        SUPERADMIN = 'superadmin', 'Platform Superadmin'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
        db_index=True,
        help_text="Role-Based Access Control principal"
    )
    phone = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=user_avatar_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text="User profile picture (JPG, PNG, WebP up to 5MB)"
    )
    avatar_shape = models.CharField(
        max_length=20,
        default='circle',
        choices=[
            ('circle', 'Circle'),
            ('squircle', 'Squircle / Rounded'),
            ('square', 'Classic Square')
        ],
        help_text="Display shape preference for profile photo"
    )
    avatar_position = models.CharField(
        max_length=50,
        default='center',
        choices=[
            ('center', 'Center'),
            ('top', 'Top Focus'),
            ('bottom', 'Bottom Focus'),
            ('left', 'Left Alignment'),
            ('right', 'Right Alignment')
        ],
        help_text="Object position focal alignment for avatar image"
    )
    bio = models.TextField(blank=True, help_text="Short bio or personal wellness focus")
    emergency_contact = models.CharField(max_length=255, blank=True)
    somatic_notes = models.TextField(blank=True, help_text="Client pelvic, injury, or somatic disclosures")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT

    @property
    def is_coach(self):
        return self.role == self.Role.COACH

    @property
    def is_studio_admin(self):
        return self.role in [self.Role.STUDIO_ADMIN, self.Role.SUPERADMIN] or self.user.is_staff or self.user.is_superuser

    def remove_avatar(self):
        """Cleanly remove the avatar file from S3 or local storage."""
        if self.avatar:
            try:
                self.avatar.delete(save=False)
            except Exception:
                pass
            self.avatar = None
            self.save(update_fields=['avatar', 'updated_at'])

    def update_avatar(self, new_file):
        """Replace avatar file, deleting previous image to prevent storage leak."""
        if self.avatar:
            try:
                self.avatar.delete(save=False)
            except Exception:
                pass
        self.avatar = new_file
        self.save(update_fields=['avatar', 'updated_at'])

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """Ensure every Django User automatically has a UserProfile attached."""
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


# Attach dynamic helper accessors to standard User model
def _get_user_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


if not hasattr(User, 'role'):
    User.role = property(lambda self: _get_user_profile(self).role)
if not hasattr(User, 'phone'):
    User.phone = property(lambda self: _get_user_profile(self).phone)
if not hasattr(User, 'avatar'):
    User.avatar = property(lambda self: _get_user_profile(self).avatar)
if not hasattr(User, 'avatar_shape'):
    User.avatar_shape = property(lambda self: _get_user_profile(self).avatar_shape)
if not hasattr(User, 'avatar_position'):
    User.avatar_position = property(lambda self: _get_user_profile(self).avatar_position)
if not hasattr(User, 'bio'):
    User.bio = property(lambda self: _get_user_profile(self).bio)
if not hasattr(User, 'emergency_contact'):
    User.emergency_contact = property(lambda self: _get_user_profile(self).emergency_contact)
if not hasattr(User, 'somatic_notes'):
    User.somatic_notes = property(lambda self: _get_user_profile(self).somatic_notes)
if not hasattr(User, 'is_client'):
    User.is_client = property(lambda self: _get_user_profile(self).is_client)
if not hasattr(User, 'is_coach'):
    User.is_coach = property(lambda self: _get_user_profile(self).is_coach)
if not hasattr(User, 'is_studio_admin'):
    User.is_studio_admin = property(lambda self: _get_user_profile(self).is_studio_admin)
if not hasattr(User, 'update_avatar'):
    User.update_avatar = lambda self, new_file: _get_user_profile(self).update_avatar(new_file)
if not hasattr(User, 'remove_avatar'):
    User.remove_avatar = lambda self: _get_user_profile(self).remove_avatar()

User.Role = UserProfile.Role


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    duration_minutes = models.PositiveIntegerField(default=60)
    location_type = models.CharField(max_length=50, default='all nairobi')
    location_display = models.CharField(max_length=200, default='Karen Studio Sanctuary, Nairobi')
    price_kes = models.PositiveIntegerField(default=3500)
    price_eur = models.PositiveIntegerField(default=40)

    # Dual Image Support: S3 Cloud / Database ImageField + Optional Web URL Fallback
    image = models.ImageField(
        upload_to=service_image_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Uploaded service photo saved in media storage (JPG, PNG, WebP up to 10MB)"
    )
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Optional external image fallback URL")

    description = models.TextField()
    badge = models.CharField(max_length=100, blank=True)
    capacity = models.CharField(max_length=100, default='Small Group (4–8)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_image(self, new_file):
        """Replace service photo, purging previous physical file."""
        if self.image:
            try:
                self.image.delete(save=False)
            except Exception:
                pass
        self.image = new_file
        self.save(update_fields=['image', 'updated_at'])

    def remove_image(self):
        """Delete service photo from storage and database."""
        if self.image:
            try:
                self.image.delete(save=False)
            except Exception:
                pass
            self.image = None
            self.save(update_fields=['image', 'updated_at'])

    def __str__(self):
        return self.title


class TimeSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='slots')
    slot_date = models.DateField(db_index=True)
    start_time = models.CharField(max_length=20)
    period = models.CharField(max_length=20, default='Morning')
    location_name = models.CharField(max_length=200, default='Karen Sanctuary')
    total_capacity = models.PositiveIntegerField(default=4)
    spots_left = models.PositiveIntegerField(default=4)
    is_full = models.BooleanField(default=False)

    # Custom Session / Workshop Banner Image Support
    banner_image = models.ImageField(
        upload_to=session_banner_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Custom session/masterclass promotional banner (JPG, PNG, WebP up to 10MB)"
    )
    banner_url = models.URLField(max_length=500, blank=True, null=True, help_text="Optional external banner fallback URL")
    session_theme = models.CharField(max_length=200, blank=True, help_text="e.g. Full Moon Sound Immersion or Pelvic Floor Masterclass")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['service', 'slot_date']),
        ]

    def update_banner(self, new_file):
        """Replace session banner, purging previous file."""
        if self.banner_image:
            try:
                self.banner_image.delete(save=False)
            except Exception:
                pass
        self.banner_image = new_file
        self.save(update_fields=['banner_image', 'updated_at'])

    def remove_banner(self):
        """Delete session banner file from storage and database."""
        if self.banner_image:
            try:
                self.banner_image.delete(save=False)
            except Exception:
                pass
            self.banner_image = None
            self.save(update_fields=['banner_image', 'updated_at'])

    def __str__(self):
        return f"{self.service.title} - {self.slot_date} {self.start_time} ({self.spots_left}/{self.total_capacity} spots)"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='bookings')
    slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name='bookings')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_payment')
    payment_method = models.CharField(max_length=50, default='mpesa')
    payment_reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
    currency = models.CharField(max_length=10, default='KES')
    total_amount = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    coach_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {str(self.id)[:8]} - {self.user.username} - {self.service.title} ({self.status})"


class UserPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packages')
    package_name = models.CharField(max_length=255, default='5-Session Studio Pass')
    total_sessions = models.PositiveIntegerField(default=5)
    remaining_sessions = models.PositiveIntegerField(default=5)
    valid_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.package_name} ({self.remaining_sessions}/{self.total_sessions} left)"


class PaymentTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    provider = models.CharField(max_length=50, default='daraja_mpesa')
    merchant_request_id = models.CharField(max_length=100, blank=True)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default='KES')
    phone_number = models.CharField(max_length=50)
    status = models.CharField(max_length=30, default='initiated')
    raw_callback_payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx {self.checkout_request_id} - {self.amount} {self.currency} ({self.status})"


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_actions')
    action = models.CharField(max_length=100)  # e.g. "CUSTOMER_EXPORT", "SLOT_OVERBOOK_OVERRIDE", "PASS_ISSUED"
    target_entity = models.CharField(max_length=100)
    target_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        actor_name = self.actor.username if self.actor else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {actor_name} -> {self.action} on {self.target_entity}:{self.target_id}"


# Automated File Cleanup Signals
@receiver(post_delete, sender=Service)
def cleanup_service_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        try:
            instance.image.delete(save=False)
        except Exception:
            pass


@receiver(post_delete, sender=TimeSlot)
def cleanup_timeslot_banner_on_delete(sender, instance, **kwargs):
    if instance.banner_image:
        try:
            instance.banner_image.delete(save=False)
        except Exception:
            pass


@receiver(post_delete, sender=UserProfile)
def cleanup_user_avatar_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        try:
            instance.avatar.delete(save=False)
        except Exception:
            pass
