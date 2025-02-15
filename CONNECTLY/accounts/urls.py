"""
URL configuration for PROJECT1 project.

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
from accounts import views
from .views import custom_logout

app_name='accounts'

urlpatterns = [
    path("register/",views.register,name="signup"),
    path("login/",views.user_login,name="login"),
    # path('login_otp/', views.Login_otp, name='login_otp'),
    path('logout/', custom_logout, name='logout'),  # Logout URL
    # path('verify_otp/', views.verify_otp, name='verify_otp')
]