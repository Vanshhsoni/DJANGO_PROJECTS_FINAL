from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("orders/", views.show_orders, name="show_orders"),
    path("previous/", views.previous_orders, name="previous"),
    path('buy/<str:weapon_name>/', views.buy_weapon, name='buy'),
    path('update_quantity/', views.update_order_quantity, name='update_quantity'),  # Add this line
    path('delete/<int:weapon_id>/', views.delete_order, name='delete_order'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),

]
