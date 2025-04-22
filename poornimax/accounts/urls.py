# accounts/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('signup_or_login/', views.load_signup, name='load_signup'),
    path('signup_access/', views.signup_access, name='signup_access'),
    path('login/', views.load_login, name='load_login'),
    path('login_access/', views.login_access, name='login_access'),
    path('signup/', views.login_signup, name='login_signup'),
    path('x/', views.x, name='x'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('ans/', views.answers_view, name='answers_page'),
    path('questionnaire/', views.questionnaire_view, name='questionnaire_view'),
    path('z/', views.z, name='z'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
