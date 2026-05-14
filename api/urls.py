from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MosqueViewSet, AnnouncementViewSet, 
    EventViewSet, CommunityUpdateViewSet, DonationViewSet, CommunityLinkViewSet, BayanViewSet
)

router = DefaultRouter()
router.register(r'mosques', MosqueViewSet, basename='mosque')
router.register(r'mosques', MosqueViewSet, basename='mosque')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'events', EventViewSet, basename='event')
router.register(r'community-updates', CommunityUpdateViewSet, basename='community-update')
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'community-links', CommunityLinkViewSet, basename='community-link')
router.register(r'bayans', BayanViewSet, basename='bayan')

urlpatterns = [
    path('', include(router.urls)),
]
