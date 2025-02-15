from django.contrib import admin
from django.urls import path, include
from home import views as home_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include('home.urls')),
    path("accounts/", include(('accounts.urls', 'accounts'), namespace='accounts')),
    path("feed/", include(('feed.urls', 'feed'), namespace='feed')),
    path("", home_views.load_main, name="main"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

