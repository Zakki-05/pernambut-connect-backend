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
        
        # Step 1: Requesting OTP (or if otp is null/empty)
        if not otp:
            # Generate a simple OTP (in prod use a random one and save to cache)
            demo_otp = "1234" 
            
            from django.core.mail import send_mail
            from django.conf import settings
            
            email_sent = False
            error_msg = ""
            try:
                send_mail(
                    'Your Pernambut Connect Login Code',
                    f'Your login code is: {demo_otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                print(f"Email error: {e}")
                error_msg = str(e)
            
            if email_sent:
                return Response({
                    "message": "OTP sent successfully to your email", 
                    "demo_otp": demo_otp,
                    "status": "success"
                })
            else:
                # If email fails, we still allow proceeding in demo mode
                return Response({
                    "message": f"Proceeding with demo mode (Email error: {error_msg})",
                    "demo_otp": demo_otp,
                    "warning": "Email delivery failed, but you can use the demo OTP.",
                    "status": "warning"
                }, status=status.HTTP_200_OK) # Change to 200 to allow frontend to proceed
        
        # Step 2: Verifying OTP
        if otp != "1234":
            return Response({"error": "Invalid OTP. Use 1234 for testing."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or get user using email as primary identifier
        # Use the email itself as username to avoid duplicates if possible, 
        # or handle username uniqueness
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create new user
            username = email.replace('@', '_').replace('.', '_')
            # Ensure username is unique if someone else has it
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
                
            user = User.objects.create(
                email=email,
                username=username,
                name=email.split('@')[0].capitalize()
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
            # Try to use Firebase Admin to verify the token
            try:
                from firebase_admin import auth
                decoded_token = auth.verify_id_token(token)
                email = decoded_token.get('email')
                name = decoded_token.get('name', email.split('@')[0])
            except Exception as firebase_error:
                # If firebase-admin fails (e.g. no serviceAccountKey.json), 
                # we fall back to a "demo" mode only if in DEBUG=True
                from django.conf import settings
                if settings.DEBUG:
                    print(f"Firebase verification skipped/failed: {firebase_error}")
                    # In demo mode, we use the token string as the email if it looks like one
                    email = token if '@' in token else "demo-user@example.com"
                    name = email.split('@')[0].capitalize()
                else:
                    raise firebase_error

            if not email:
                return Response({"error": "Invalid token: Email not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create or get user
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
            print(f"Google Login Error: {str(e)}")
            return Response({"error": f"Authentication failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def ping(self, request):
        return Response({"message": "pong"})

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
