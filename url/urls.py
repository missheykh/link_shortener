from django.urls import path

from .views import create_short_url,redirect_target_url,validate_url
app_name='url'

urlpatterns = [
    path('',create_short_url, name='create_short_url'),
    path('<str:pk>',redirect_target_url,name='redirect_target_ur'),
    # path('validate_url',validate_url,name='validate_url'),
   
]


