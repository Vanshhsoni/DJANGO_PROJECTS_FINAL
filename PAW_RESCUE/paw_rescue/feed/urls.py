from django.urls import path
from . import views
urlpatterns = [
    path('', views.feed, name='feed'),  # Feed page
    path('report/', views.report, name='report'),
    path('adoptions/', views.adoption_public, name='adoption_public'),
    path('volunteer/', views.volunteer_form, name='volunteer_form'),
    path('food/', views.food_view, name="food"),
    path('health/', views.health, name="health"),
    path('donate/',views.donate,name="donate"),
    path('location/',views.location,name="location")

]
