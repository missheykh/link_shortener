from django.urls import path

from .views import create_short_url,redirect_url
app_name='url'

urlpatterns = [
    path('create_short_url/',create_short_url, name='create_short_url'),
   
]


