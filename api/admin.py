from django.contrib import admin
from .models import User, Mosque, Announcement, Event, CommunityUpdate, Donation

admin.site.register(User)
admin.site.register(Mosque)
admin.site.register(Announcement)
admin.site.register(Event)
admin.site.register(CommunityUpdate)
admin.site.register(Donation)
