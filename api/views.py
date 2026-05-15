from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Mosque, Announcement, Event, CommunityUpdate, Donation, CommunityLink, Bayan
from .serializers import (
    UserSerializer, MosqueSerializer, AnnouncementSerializer, 
    EventSerializer, CommunityUpdateSerializer, DonationSerializer, CommunityLinkSerializer, BayanSerializer
)
import math

class BayanViewSet(viewsets.ModelViewSet):
    queryset = Bayan.objects.all().order_by('-created_at')
    serializer_class = BayanSerializer
    permission_classes = [permissions.AllowAny]

class CommunityLinkViewSet(viewsets.ModelViewSet):
    queryset = CommunityLink.objects.all()
    serializer_class = CommunityLinkSerializer
    permission_classes = [permissions.AllowAny]

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer

import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        # Hash password before storing temporarily
        hashed_password = make_password(data.get('password'))
        temp_data = {
            'username': data.get('username') or email.split('@')[0],
            'email': email,
            'password': hashed_password,
            'name': data.get('name', ''),
            'otp': otp
        }
        
        # Store in cache for 3 minutes
        cache.set(f'otp_{email}', temp_data, timeout=180)
        
        # Send Email
        try:
            send_mail(
                'Verify your email - Pernambut Connect',
                f'Your verification code is: {otp}. It expires in 3 minutes.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'OTP sent to email. Please verify to complete registration.'}, status=status.HTTP_200_OK)

class VerifyOTPAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        cached_data = cache.get(f'otp_{email}')
        
        if not cached_data:
            return Response({'error': 'OTP expired or not found. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if cached_data['otp'] == otp:
            # Create actual user
            user = User.objects.create(
                username=cached_data['username'],
                email=cached_data['email'],
                password=cached_data['password'],
                name=cached_data['name']
            )
            
            # Clear cache
            cache.delete(f'otp_{email}')
            
            # Return tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Email verified and registration complete!'
            }, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        cached_data = cache.get(f'otp_{email}')
        
        if not cached_data:
            return Response({'error': 'No pending registration found for this email.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate new OTP
        new_otp = str(random.randint(100000, 999999))
        cached_data['otp'] = new_otp
        cache.set(f'otp_{email}', cached_data, timeout=180)
        
        # Resend Email
        send_mail(
            'New verification code - Pernambut Connect',
            f'Your new verification code is: {new_otp}. It expires in 3 minutes.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        
        return Response({'message': 'New OTP sent to email.'})

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # Use 'username' keyword for the email field as per USERNAME_FIELD
            user = authenticate(username=email, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'Login successful'
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already logged out"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UpdateLanguageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        language = request.data.get('language')
        if language not in ['en', 'ta', 'ur']:
            return Response({'error': 'Unsupported language'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.language = language
        request.user.save()
        return Response({'message': 'Language updated successfully', 'language': language})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admins see all users, regular users see only themselves
        if self.request.user.is_staff:
            return User.objects.all().order_by('-date_joined')
        return User.objects.filter(id=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def toggle_admin(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        user = self.get_object()
        # Prevent admin from removing their own status by accident
        if user.id == request.user.id:
            return Response({"error": "You cannot change your own admin status"}, status=status.HTTP_400_BAD_REQUEST)
            
        user.is_staff = not user.is_staff
        user.is_superuser = user.is_staff # Keep them in sync for simplicity
        user.save()
        
        return Response({
            "message": f"User {user.email} admin status: {user.is_staff}",
            "is_staff": user.is_staff
        })

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
        # Simple Euclidean distance for demo
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
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        mosque_id = self.request.query_params.get('mosque_id')
        if mosque_id:
            return Announcement.objects.filter(mosque_id=mosque_id).order_by('-created_at')
        return Announcement.objects.none()

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        mosque_id = self.request.query_params.get('mosque_id')
        if mosque_id:
            return Event.objects.filter(mosque_id=mosque_id).order_by('date', 'time')
        return Event.objects.none()

class CommunityUpdateViewSet(viewsets.ModelViewSet):
    queryset = CommunityUpdate.objects.all()
    serializer_class = CommunityUpdateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        mosque_id = self.request.query_params.get('mosque_id')
        if mosque_id:
            return CommunityUpdate.objects.filter(mosque_id=mosque_id).order_by('-created_at')
        return CommunityUpdate.objects.none()

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by('-created_at')
    serializer_class = DonationSerializer
    permission_classes = [permissions.AllowAny]

