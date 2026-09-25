from django.urls import path
from .views import (
    ApiRootView,
    ServiceListView,
    ServiceDetailView,
    TimeSlotListView,
    BookingListCreateView,
    BookingCancelView,
    BookingRescheduleView,
    MpesaSTKPushView,
    UserPackageView,
    SignUpView,
    LoginView,
    LogoutView,
    UserProfileView,
    UserProfileDetailView,
    UserAvatarManageView,
    AdminOverviewView,
    AdminServiceListCreateView,
    AdminServiceDetailView,
    AdminServiceImageManageView,
    AdminTimeSlotListCreateView,
    AdminTimeSlotBulkCreateView,
    AdminTimeSlotDetailView,
    AdminSessionBannerManageView,
    AdminBookingListView,
    AdminBookingDetailView,
    AdminCustomerListView,
    AdminCustomerDetailView,
    AdminCustomerPassView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'),
    path('services/', ServiceListView.as_view(), name='services-list'),
    path('services/<uuid:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('slots/', TimeSlotListView.as_view(), name='slots-list'),
    path('bookings/', BookingListCreateView.as_view(), name='bookings-list-create'),
    path('bookings/<uuid:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    path('bookings/<uuid:pk>/reschedule/', BookingRescheduleView.as_view(), name='booking-reschedule'),
    path('payments/mpesa-stk/', MpesaSTKPushView.as_view(), name='mpesa-stk-push'),
    path('user-packages/', UserPackageView.as_view(), name='user-packages'),

    # Simple JWT Authentication Endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Authentication & User Profile endpoints
    path('auth/signup/', SignUpView.as_view(), name='auth-signup'),
    path('auth/register/', SignUpView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/me/', UserProfileView.as_view(), name='auth-me'),
    path('auth/profile/', UserProfileDetailView.as_view(), name='auth-profile'),
    path('auth/profile/avatar/', UserAvatarManageView.as_view(), name='auth-profile-avatar'),

    # Admin Management & Media Endpoints
    path('admin/overview/', AdminOverviewView.as_view(), name='admin-overview'),
    path('admin/services/', AdminServiceListCreateView.as_view(), name='admin-services'),
    path('admin/services/<uuid:pk>/', AdminServiceDetailView.as_view(), name='admin-service-detail'),
    path('admin/services/<uuid:pk>/image/', AdminServiceImageManageView.as_view(), name='admin-service-image'),
    path('admin/slots/', AdminTimeSlotListCreateView.as_view(), name='admin-slots'),
    path('admin/slots/bulk-generate/', AdminTimeSlotBulkCreateView.as_view(), name='admin-slots-bulk-generate'),
    path('admin/slots/<uuid:pk>/', AdminTimeSlotDetailView.as_view(), name='admin-slot-detail'),
    path('admin/slots/<uuid:pk>/banner/', AdminSessionBannerManageView.as_view(), name='admin-session-banner'),
    path('admin/bookings/', AdminBookingListView.as_view(), name='admin-bookings'),
    path('admin/bookings/<uuid:pk>/', AdminBookingDetailView.as_view(), name='admin-booking-detail'),
    path('admin/customers/', AdminCustomerListView.as_view(), name='admin-customers'),
    path('admin/customers/<str:pk>/', AdminCustomerDetailView.as_view(), name='admin-customer-detail'),
    path('admin/customers/<str:pk>/passes/', AdminCustomerPassView.as_view(), name='admin-customer-pass'),
]
