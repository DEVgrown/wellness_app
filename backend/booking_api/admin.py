from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Service, TimeSlot, Booking, UserPackage, PaymentTransaction, AuditLog


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Wellness Profile & RBAC'
    fields = ('role', 'phone', 'avatar', 'bio', 'emergency_contact', 'somatic_notes')


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('profile__role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__phone')
    ordering = ('-date_joined',)

    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else 'Client'
    get_role.short_description = 'Studio Role'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at', 'updated_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration_minutes', 'price_kes', 'price_eur', 'capacity', 'updated_at')
    list_filter = ('category', 'location_type')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('service', 'slot_date', 'start_time', 'period', 'spots_left', 'total_capacity', 'is_full', 'location_name')
    list_filter = ('slot_date', 'period', 'is_full', 'service')
    search_fields = ('service__title', 'session_theme', 'location_name')
    date_hierarchy = 'slot_date'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'slot', 'status', 'payment_method', 'currency', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'currency', 'created_at')
    search_fields = ('id', 'user__username', 'user__email', 'payment_reference', 'service__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(UserPackage)
class UserPackageAdmin(admin.ModelAdmin):
    list_display = ('user', 'package_name', 'remaining_sessions', 'total_sessions', 'valid_until', 'created_at')
    list_filter = ('package_name', 'valid_until')
    search_fields = ('user__username', 'user__email', 'package_name')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('checkout_request_id', 'booking', 'provider', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'provider', 'currency', 'created_at')
    search_fields = ('checkout_request_id', 'merchant_request_id', 'phone_number')
    readonly_fields = ('created_at',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'target_entity', 'target_id', 'ip_address')
    list_filter = ('action', 'target_entity', 'timestamp')
    search_fields = ('actor__username', 'action', 'target_entity', 'target_id')
    readonly_fields = ('timestamp',)
