
from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.checkout_page ,name="checkout_home"),
    path('success/', views.checkout_success ,name="checkout_success"),
    path('other/', views.checkout_other ,name="checkout_other"),
    


]