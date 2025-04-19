from django.urls import path
from . import views

app_name = "feed"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('all/', views.all_users, name='all'),
    path('crush_action/<int:user_id>/', views.crush_action, name='crush_action'),
    path('create-post/', views.create_post, name='create_post'),
    path('explore/', views.explore, name='explore'),
    path('confession/', views.create_confession, name='confession'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/data/', views.get_post_data, name='get_post_data'),
]