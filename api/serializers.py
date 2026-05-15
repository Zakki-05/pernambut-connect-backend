from rest_framework import serializers
from .models import User, Mosque, Announcement, Event, CommunityUpdate, Donation, CommunityLink, Bayan

class MosqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mosque
        fields = '__all__'

class BayanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bayan
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    mosque_details = MosqueSerializer(source='selected_mosque', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'name', 'area', 'is_staff', 'is_superuser', 'selected_mosque', 'mosque_details']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'name']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', '')
        )
        # Automatically grant admin access only to this specific email
        if validated_data['email'] == 'zakkiadnan05@gmail.com':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class CommunityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityUpdate
        fields = '__all__'

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

class CommunityLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityLink
        fields = '__all__'
