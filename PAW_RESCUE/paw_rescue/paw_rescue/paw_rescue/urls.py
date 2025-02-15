from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import landing_page  # Import the landing_page view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', landing_page, name='landing_page'),  # Landing page route
    path('accounts/', include('accounts.urls')),  # Accounts app URLs (login/signup/logout)
    path('feed/', include('feed.urls')),  # Feed app URLs
    path('adminpanel/', include('adminpanel.urls')),  # Adminpanel app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
