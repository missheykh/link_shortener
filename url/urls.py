from cmath import log
from unicodedata import name
from django.urls import path

from .views import create_short_url,redirect_target_url,validate_url,register,user_static,login,logout
app_name='url'

urlpatterns = [
    path('',create_short_url, name='create_short_url'),
    path('<str:pk>',redirect_target_url,name='redirect_target_ur'),
    # path('validate_url',validate_url,name='validate_url'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('user_static/',user_static,name='user_static'),
   
]


