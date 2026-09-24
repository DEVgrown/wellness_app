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
    UserProfileView
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
    
    # Authentication endpoints
    path('auth/signup/', SignUpView.as_view(), name='auth-signup'),
    path('auth/register/', SignUpView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/me/', UserProfileView.as_view(), name='auth-me'),
]
