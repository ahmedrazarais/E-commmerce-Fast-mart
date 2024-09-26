
from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.login_home_page ,name="signin_home"),
    path('login_form/', views.login_form_page ,name="signin_form"),
   
    path('forgotpassword/', views.forgot_pswd ,name="forgot_pswrd"),
    path('logout/', views.logout_view, name='logout'),
   
 

 
]