from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Mosque, Announcement, Event, CommunityUpdate, Donation, CommunityLink, Bayan

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'name', 'is_staff')
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'area', 'selected_mosque', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'name', 'phone_number', 'area', 'selected_mosque', 'profile_image')}),
    )

admin.site.register(Mosque)
admin.site.register(Announcement)
admin.site.register(Event)
admin.site.register(CommunityUpdate)
admin.site.register(Donation)
admin.site.register(CommunityLink)
admin.site.register(Bayan)
