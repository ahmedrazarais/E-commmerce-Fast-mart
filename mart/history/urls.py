

from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_history , name='history_page'),
    
   
]  