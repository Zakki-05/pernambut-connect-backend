from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Mosque, Announcement, Event, CommunityUpdate, Donation, CommunityLink, Bayan
from .serializers import (
    UserSerializer, MosqueSerializer, AnnouncementSerializer, 
    EventSerializer, CommunityUpdateSerializer, DonationSerializer, CommunityLinkSerializer, BayanSerializer
)
import math

class BayanViewSet(viewsets.ModelViewSet):
    queryset = Bayan.objects.all().order_by('-created_at')
    serializer_class = BayanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

# ... (AuthViewSet and others remain)

class CommunityLinkViewSet(viewsets.ModelViewSet):
    queryset = CommunityLink.objects.all()
    serializer_class = CommunityLinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 1: Requesting OTP
        if not otp:
            # Simulate sending OTP
            print(f"\n[EMAIL GATEWAY] Sending OTP 1234 to {email}\n")
            return Response({"message": "OTP sent successfully to your email", "demo_otp": "1234"})
        
        # Step 2: Verifying OTP
        if otp != "1234":
            return Response({"error": "Invalid OTP. Use 1234 for testing."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Auto-create user for simplicity if doesn't exist
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': email.split('@')[0]}
        )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['post'])
    def google_login(self, request):
        token = request.data.get('token')
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # In a real app, use firebase_admin to verify:
            # decoded_token = auth.verify_id_token(token)
            # email = decoded_token['email']
            # name = decoded_token.get('name', '')
            
            # For demo purposes, we'll assume the token is the email
            # IMPORTANT: Replace this with real verification in production!
            email = token if '@' in token else "google-user@example.com"
            name = email.split('@')[0].capitalize()
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'name': name
                }
            )
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['put'])
    def select_mosque(self, request):
        mosque_id = request.data.get('mosque_id')
        try:
            mosque = Mosque.objects.get(id=mosque_id)
            request.user.selected_mosque = mosque
            request.user.save()
            return Response(UserSerializer(request.user).data)
        except Mosque.DoesNotExist:
            return Response({"error": "Mosque not found"}, status=status.HTTP_404_NOT_FOUND)

class MosqueViewSet(viewsets.ModelViewSet):
    queryset = Mosque.objects.all()
    serializer_class = MosqueSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def nearest(self, request):
        lat = float(request.data.get('latitude', 0))
        lng = float(request.data.get('longitude', 0))
        
        if not lat or not lng:
            return Response({"error": "Latitude and longitude required"}, status=status.HTTP_400_BAD_REQUEST)
        
        mosques = Mosque.objects.all()
        # Simple Euclidean distance for demo (should use Haversine in prod)
        nearest_mosque = min(
            mosques, 
            key=lambda m: math.hypot(m.latitude - lat, m.longitude - lng),
            default=None
        )
        
        if nearest_mosque:
            return Response(MosqueSerializer(nearest_mosque).data)
        return Response({"error": "No mosques found"}, status=status.HTTP_404_NOT_FOUND)

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        mosque_id = self.request.query_params.get('mosque_id')
        if mosque_id:
            return Announcement.objects.filter(mosque_id=mosque_id).order_by('-created_at')
        return Announcement.objects.none()

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        mosque_id = self.request.query_params.get('mosque_id')
        if mosque_id:
            return Event.objects.filter(mosque_id=mosque_id).order_by('date', 'time')
        return Event.objects.none()

class CommunityUpdateViewSet(viewsets.ModelViewSet):
    queryset = CommunityUpdate.objects.all()
    serializer_class = CommunityUpdateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        mosque_id = self.request.query_params.get('mosque_id')
        if mosque_id:
            return CommunityUpdate.objects.filter(mosque_id=mosque_id).order_by('-created_at')
        return CommunityUpdate.objects.none()

class DonationViewSet(viewsets.ModelViewSet):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user).order_by('-created_at')
