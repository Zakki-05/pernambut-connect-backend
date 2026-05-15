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

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Registration successful'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            
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

