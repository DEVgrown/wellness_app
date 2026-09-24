from rest_framework import serializers

class ServiceSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    slug = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=50)
    duration_minutes = serializers.IntegerField(default=60)
    location_type = serializers.CharField(max_length=100)
    location_display = serializers.CharField(max_length=255)
    price_kes = serializers.IntegerField()
    price_eur = serializers.IntegerField()
    image_url = serializers.CharField(allow_blank=True, required=False)
    description = serializers.CharField()
    badge = serializers.CharField(allow_blank=True, required=False)
    capacity = serializers.CharField(allow_blank=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)

class TimeSlotSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    service_id = serializers.UUIDField(required=False, allow_null=True)
    slot_date = serializers.DateField()
    start_time = serializers.CharField(max_length=20)
    period = serializers.CharField(max_length=20)
    location_name = serializers.CharField(max_length=255)
    spots_left = serializers.IntegerField(default=2)
    is_full = serializers.BooleanField(default=False)
    waitlist_available = serializers.BooleanField(default=False)

class BookingSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    service_id = serializers.UUIDField(required=False, allow_null=True)
    service_title = serializers.CharField(max_length=255)
    user_name = serializers.CharField(max_length=100, default='Sarah')
    user_email = serializers.EmailField(default='sarah@example.com')
    user_phone = serializers.CharField(max_length=50, default='+254 712 345 678')
    booking_date = serializers.DateField()
    time_slot = serializers.CharField(max_length=50)
    location_name = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=['confirmed', 'completed', 'cancelled'], default='confirmed')
    payment_method = serializers.ChoiceField(choices=['mpesa', 'card', 'digital', 'studio'], default='mpesa')
    payment_reference = serializers.CharField(max_length=100, required=False, allow_blank=True)
    currency = serializers.ChoiceField(choices=['KES', 'EUR'], default='KES')
    total_amount = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    coach_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

class BookingCreateSerializer(serializers.Serializer):
    service_id = serializers.UUIDField(required=False, allow_null=True)
    service_title = serializers.CharField(max_length=255)
    user_name = serializers.CharField(max_length=100, default='Sarah')
    user_email = serializers.EmailField(default='sarah@example.com')
    user_phone = serializers.CharField(max_length=50, default='+254 712 345 678')
    booking_date = serializers.DateField()
    time_slot = serializers.CharField(max_length=50)
    location_name = serializers.CharField(max_length=255, default='Karen Studio, Nairobi')
    payment_method = serializers.ChoiceField(choices=['mpesa', 'card', 'digital', 'studio'], default='mpesa')
    currency = serializers.ChoiceField(choices=['KES', 'EUR'], default='KES')
    total_amount = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)

class RescheduleBookingSerializer(serializers.Serializer):
    booking_date = serializers.DateField()
    time_slot = serializers.CharField(max_length=50)

class MpesaPaymentSerializer(serializers.Serializer):
    booking_id = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20)
    amount = serializers.IntegerField()
    currency = serializers.CharField(default='KES')

    def validate_phone_number(self, value):
        cleaned = value.replace(" ", "").replace("-", "")
        if not cleaned.startswith("+254") and not cleaned.startswith("07") and not cleaned.startswith("01") and not cleaned.startswith("254"):
            raise serializers.ValidationError("Must be a valid Kenyan mobile number (e.g. +254 712 345 678)")
        return cleaned

class UserPackageSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user_name = serializers.CharField(max_length=100)
    package_name = serializers.CharField(max_length=255)
    total_sessions = serializers.IntegerField()
    remaining_sessions = serializers.IntegerField()
    valid_until = serializers.CharField(max_length=100)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'name']

    def get_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username

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
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Support login with either username or email
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

