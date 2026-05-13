from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "app": "Pernambut Connect API",
        "status": "running",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "mosques": "/api/mosques/",
            "announcements": "/api/announcements/",
            "events": "/api/events/",
        }
    })

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
