from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Correctly name the URL
    path('logout/', views.admin_logout, name='admin_logout'),
    path('add-adoption/', views.add_adoption, name='add_adoption'),
    path('delete-adoption/<int:pk>/', views.delete_adoption, name='delete_adoption'),
    path('adopt/', views.user_adoption, name='user_adoption'),
    path('volunteers/', views.volunteer_list, name='volunteer_list'),
    path('adoptions/', views.adoption_list, name='adoption_list'),  # Display available adoptions
    path('delete-adoption/<int:pk>/', views.delete_adoption, name='delete_adoption'),  # Delete adoption
]

