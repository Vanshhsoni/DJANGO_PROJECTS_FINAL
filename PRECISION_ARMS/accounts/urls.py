from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path('logout/', views.custom_logout, name='logout'),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('account-settings/', views.account_settings, name='account_settings'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
