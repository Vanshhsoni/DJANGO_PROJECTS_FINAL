# feed/urls.py

from django.urls import path
from . import views

app_name = "feed"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('all/', views.all_users, name='all'),
    path('crush_action/<int:user_id>/', views.crush_action, name='crush_action'),
]
