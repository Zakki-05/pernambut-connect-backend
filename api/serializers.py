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
