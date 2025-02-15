"""
URL configuration for PRECISION_ARMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from armory import views 

app_name = "armory"

urlpatterns = [
    path("armory_home/", views.armory_home, name="armory_home"),
    path("AR/", views.AR, name="AR"),
    path("DMR/", views.DMR, name="DMR"),
    path("ETC/", views.ETC, name="ETC"),
    path("HANDGUN/", views.HANDGUN, name="HANDGUN"),
    path("MELEE/", views.MELEE, name="MELEE"),
    path("SHOTGUN/", views.SHOTGUN, name="SHOTGUN"),
    path("SMG/", views.SMG, name="SMG"),
    path("SR/", views.SR, name="SR"),
    path("THROWABLE/", views.THROWABLE, name="THROWABLE"),
    path('buy/<str:weapon_name>/', views.buy_load, name='buy_load'), 
    path("ATTACHMENTS_MAIN/", views.ATTACHMENTS_MAIN, name="ATTACHMENTS_MAIN"),
    path("ABOUT_US/", views.ABOUT_US, name="ABOUT_US")
]




