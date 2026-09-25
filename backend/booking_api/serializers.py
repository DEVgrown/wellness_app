from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import UserProfile, Service, TimeSlot, Booking, UserPackage, PaymentTransaction, AuditLog

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    emergency_contact = serializers.SerializerMethodField()
    somatic_notes = serializers.SerializerMethodField()
    avatar_shape = serializers.SerializerMethodField()
    avatar_position = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'name',
            'role', 'phone', 'avatar_url', 'avatar_shape', 'avatar_position',
            'bio', 'emergency_contact', 'somatic_notes',
            'is_staff', 'is_superuser', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'username', 'email', 'role', 'is_staff', 'is_superuser', 'is_active', 'date_joined']

    def get_name(self, obj):
        full = f"{obj.first_name} {obj.last_name}".strip()
        return full if full else obj.username

    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else 'client'

    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, 'profile') else ''

    def get_bio(self, obj):
        return obj.profile.bio if hasattr(obj, 'profile') else ''

    def get_emergency_contact(self, obj):
        return obj.profile.emergency_contact if hasattr(obj, 'profile') else ''

    def get_somatic_notes(self, obj):
        return obj.profile.somatic_notes if hasattr(obj, 'profile') else ''

    def get_avatar_shape(self, obj):
        return getattr(obj.profile, 'avatar_shape', 'circle') if hasattr(obj, 'profile') else 'circle'

    def get_avatar_position(self, obj):
        return getattr(obj.profile, 'avatar_position', 'center') if hasattr(obj, 'profile') else 'center'

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        avatar = obj.profile.avatar if hasattr(obj, 'profile') else None
        if avatar:
            try:
                return request.build_absolute_uri(avatar.url) if request else avatar.url
            except Exception:
                return avatar.url if hasattr(avatar, 'url') else None
        return None


class UserProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    emergency_contact = serializers.CharField(required=False, allow_blank=True)
    somatic_notes = serializers.CharField(required=False, allow_blank=True)
    avatar_shape = serializers.ChoiceField(choices=['circle', 'squircle', 'square'], required=False)
    avatar_position = serializers.ChoiceField(choices=['center', 'top', 'bottom', 'left', 'right'], required=False)

    def update(self, instance, validated_data):
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        instance.save()

        if hasattr(instance, 'profile'):
            profile = instance.profile
            for field in ['phone', 'bio', 'emergency_contact', 'somatic_notes', 'avatar_shape', 'avatar_position']:
                if field in validated_data:
                    setattr(profile, field, validated_data[field])
            profile.save()
        return instance


class ServiceSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'slug', 'title', 'category', 'duration_minutes',
            'location_type', 'location_display', 'price_kes', 'price_eur',
            'image', 'image_url', 'description', 'badge', 'capacity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return obj.image_url or ''


class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'slug', 'title', 'category', 'duration_minutes',
            'location_type', 'location_display', 'price_kes', 'price_eur',
            'image_url', 'description', 'badge', 'capacity'
        ]
        extra_kwargs = {
            'slug': {'required': False},
            'badge': {'required': False, 'allow_blank': True},
            'image_url': {'required': False, 'allow_blank': True, 'allow_null': True},
        }


class TimeSlotSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(source='service', read_only=True)
    service_title = serializers.ReadOnlyField(source='service.title')
    banner_image_url = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = [
            'id', 'service', 'service_id', 'service_title', 'slot_date', 'start_time', 'period',
            'location_name', 'total_capacity', 'spots_left', 'is_full',
            'banner_image', 'banner_image_url', 'session_theme',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_banner_image_url(self, obj):
        request = self.context.get('request')
        if obj.banner_image:
            return request.build_absolute_uri(obj.banner_image.url) if request else obj.banner_image.url
        if obj.banner_url:
            return obj.banner_url
        if obj.service and obj.service.image:
            return request.build_absolute_uri(obj.service.image.url) if request else obj.service.image.url
        return obj.service.image_url if obj.service else ''


class TimeSlotCreateUpdateSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True, required=False
    )

    class Meta:
        model = TimeSlot
        fields = [
            'service_id', 'slot_date', 'start_time', 'period',
            'location_name', 'total_capacity', 'spots_left', 'is_full',
            'banner_url', 'session_theme'
        ]


class BulkSlotGenerateSerializer(serializers.Serializer):
    service_id = serializers.UUIDField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    days_of_week = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=6),
        help_text="0=Monday, 6=Sunday"
    )
    times = serializers.ListField(child=serializers.DictField())
    location_name = serializers.CharField(max_length=200, default='Karen Sanctuary, Nairobi')
    total_capacity = serializers.IntegerField(default=6, min_value=1)


class BookingSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(source='service.id', read_only=True)
    service_title = serializers.CharField(source='service.title', read_only=True)
    user_name = serializers.SerializerMethodField()
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    booking_date = serializers.DateField(source='slot.slot_date', read_only=True)
    time_slot = serializers.CharField(source='slot.start_time', read_only=True)
    location_name = serializers.CharField(source='slot.location_name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'service', 'service_id', 'service_title',
            'user_name', 'user_email', 'user_phone',
            'slot', 'booking_date', 'time_slot', 'location_name',
            'status', 'payment_method', 'payment_reference',
            'currency', 'total_amount', 'notes', 'coach_notes', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def get_user_name(self, obj):
        full = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full if full else obj.user.username


class BookingCreateSerializer(serializers.Serializer):
    service_id = serializers.UUIDField()
    slot_id = serializers.UUIDField()
    payment_method = serializers.ChoiceField(choices=['mpesa', 'card', 'digital', 'studio'], default='mpesa')
    currency = serializers.ChoiceField(choices=['KES', 'EUR'], default='KES')
    notes = serializers.CharField(required=False, allow_blank=True)


class RescheduleBookingSerializer(serializers.Serializer):
    new_slot_id = serializers.UUIDField()


class UserPackageSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_email = serializers.CharField(source='user.email', read_only=True)
    used_sessions = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = UserPackage
        fields = [
            'id', 'user', 'user_name', 'user_email', 'package_name',
            'total_sessions', 'remaining_sessions', 'used_sessions',
            'status', 'is_active', 'valid_until', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_user_name(self, obj):
        full = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full if full else obj.user.username

    def get_used_sessions(self, obj):
        return max(0, obj.total_sessions - obj.remaining_sessions)

    def get_status(self, obj):
        from datetime import date
        today = date.today()
        if obj.remaining_sessions <= 0:
            return 'fully_used'
        if obj.valid_until and obj.valid_until < today:
            return 'expired'
        return 'active'

    def get_is_active(self, obj):
        from datetime import date
        today = date.today()
        return obj.remaining_sessions > 0 and (not obj.valid_until or obj.valid_until >= today)


class IssuePackagePassSerializer(serializers.Serializer):
    package_name = serializers.CharField(max_length=255, default='5-Session Studio Pass')
    total_sessions = serializers.IntegerField(default=5, min_value=1)
    valid_until = serializers.DateField()


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'booking', 'provider', 'merchant_request_id',
            'checkout_request_id', 'amount', 'currency', 'phone_number',
            'status', 'raw_callback_payload', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MpesaPaymentSerializer(serializers.Serializer):
    booking_id = serializers.UUIDField(required=False)
    phone_number = serializers.CharField(max_length=20)
    amount = serializers.IntegerField(required=False)
    currency = serializers.CharField(default='KES')

    def validate_phone_number(self, value):
        cleaned = value.replace(" ", "").replace("-", "")
        if not cleaned.startswith("+254") and not cleaned.startswith("07") and not cleaned.startswith("01") and not cleaned.startswith("254"):
            raise serializers.ValidationError("Must be a valid Kenyan mobile number (e.g. +254 712 345 678)")
        return cleaned


class CustomerCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6, default='Welcome123!')
    name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=UserProfile.Role.choices, default=UserProfile.Role.CLIENT)
    is_staff = serializers.BooleanField(default=False)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value


class CustomerUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=UserProfile.Role.choices, required=False)
    is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    bio = serializers.CharField(required=False, allow_blank=True)
    emergency_contact = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        for field in ['first_name', 'last_name', 'email', 'is_active', 'is_staff']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        if hasattr(instance, 'profile'):
            profile = instance.profile
            for p_field in ['phone', 'role', 'bio', 'emergency_contact']:
                if p_field in validated_data:
                    setattr(profile, p_field, validated_data[p_field])
            profile.save()
        return instance


class AdminBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status', 'notes', 'coach_notes']


class AuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = ['id', 'actor', 'actor_name', 'action', 'target_entity', 'target_id', 'ip_address', 'timestamp', 'metadata']
        read_only_fields = ['id', 'timestamp']

    def get_actor_name(self, obj):
        if obj.actor:
            full = f"{obj.actor.first_name} {obj.actor.last_name}".strip()
            return full if full else obj.actor.username
        return "System"


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        name = validated_data.get('name', '').strip()
        first_name = ''
        last_name = ''
        if name:
            parts = name.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )
        if hasattr(user, 'profile'):
            user.profile.phone = validated_data.get('phone', '')
            user.profile.save(update_fields=['phone'])
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            try:
                user_obj = User.objects.get(email__iexact=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if not user:
            raise serializers.ValidationError("Invalid email/username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        attrs['user'] = user
        return attrs
