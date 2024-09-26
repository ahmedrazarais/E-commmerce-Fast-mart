# Django Imports
from django.urls import path
from . import views

urlpatterns = [
    path("cart_home/", views.cart_home, name="cart_home"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase-quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease-quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('clear/', views.clear_cart, name='clear_cart'),  # Corrected URL f

]

