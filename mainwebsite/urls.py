
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from members.views import home
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('members/', include('members.urls')),
    path('search/', include('car_listing.urls')),
    path('messaging/', include('messaging.urls')),
    path('m/', include ('vehicle_profiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
