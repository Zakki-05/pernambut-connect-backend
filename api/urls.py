from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterAPIView, VerifyOTPAPIView, ResendOTPAPIView, LoginAPIView, LogoutAPIView, ProfileAPIView,
    UserViewSet, MosqueViewSet, AnnouncementViewSet, 
    EventViewSet, CommunityUpdateViewSet, DonationViewSet, CommunityLinkViewSet, BayanViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'mosques', MosqueViewSet, basename='mosque')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'events', EventViewSet, basename='event')
router.register(r'community-updates', CommunityUpdateViewSet, basename='community-update')
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'community-links', CommunityLinkViewSet, basename='community-link')
router.register(r'bayans', BayanViewSet, basename='bayan')

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='resend_otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
