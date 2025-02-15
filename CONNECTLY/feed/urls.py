from django.urls import path
from feed import views

app_name = 'feed'  # Ensures proper namespacing for the app


urlpatterns = [
    path('', views.feed_home, name='feed_home'),  # Home view
    path('create/', views.create_post, name='create_post'),  # Create post view
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),  # For viewing profile
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_profiles, name='search_profiles'),  # This should be for AJAX requests
    path('search_view/', views.search, name='search'),  # This should render the search.html template
]





from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
