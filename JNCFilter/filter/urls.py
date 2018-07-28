from django.urls import path

from .views import *

app_name = 'filter'
urlpatterns = [
    path('', index, name='index'),
    path('set/', set_pref, name='set_pref'),
]
