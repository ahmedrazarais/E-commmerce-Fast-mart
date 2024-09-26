
from django.urls import path
from . import views

urlpatterns = [
    path("" , views.registration_home , name="signup_homepage"),
    path("signup_form/" , views.registration_form , name="signup_form"),
 
  
]