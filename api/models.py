from django.db import models
from django.contrib.auth.models import AbstractUser

class Mosque(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True)
    
    # Prayer Timings
    fajr = models.TimeField(null=True, blank=True)
    dhuhr = models.TimeField(null=True, blank=True)
    asr = models.TimeField(null=True, blank=True)
    maghrib = models.TimeField(null=True, blank=True)
    isha = models.TimeField(null=True, blank=True)
    jummah = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=100, blank=True)
    selected_mosque = models.ForeignKey(Mosque, on_delete=models.SET_NULL, null=True, blank=True)

    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name or self.email

class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('URGENT', '🔴 Urgent'),
        ('IMPORTANT', '🟡 Important'),
        ('NORMAL', '⚪ Normal'),
    ]
    TYPE_CHOICES = [
        ('GENERAL', 'General'),
        ('EMERGENCY', 'Emergency'),
        ('RELIGIOUS', 'Religious'),
    ]
    
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='NORMAL')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='GENERAL')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mosque.name} - {self.title}"

class Event(models.Model):
    TYPE_CHOICES = [
        ('NIKAH', 'Nikah'),
        ('BAYAN', 'Bayan'),
        ('LECTURE', 'Lecture'),
        ('MEETING', 'Meeting'),
    ]
    
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CommunityUpdate(models.Model):
    TYPE_CHOICES = [
        ('BIRTH', 'Birth Announcement'),
        ('DEATH', 'Death Announcement'),
        ('ALERT', 'Local Alert'),
    ]
    
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name='community_updates')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content = models.TextField()
    image = models.FileField(upload_to='community_updates/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Donation(models.Model):
    CATEGORY_CHOICES = [
        ('MAINTENANCE', 'Mosque Maintenance'),
        ('CHARITY', 'Charity / Zakat'),
    ]
    
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE, related_name='donations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='SUCCESS')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"

class CommunityLink(models.Model):
    PLATFORM_CHOICES = [
        ('INSTAGRAM', 'Instagram'),
        ('WHATSAPP', 'WhatsApp'),
        ('FACEBOOK', 'Facebook'),
        ('YOUTUBE', 'YouTube'),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_platform_display()}: {self.url}"

class Bayan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    speaker = models.CharField(max_length=255)
    date = models.DateField()
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.speaker} - {self.title}"
