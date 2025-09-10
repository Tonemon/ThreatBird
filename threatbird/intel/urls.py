from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = "intel"
urlpatterns = [
    path('', lambda request: redirect('overview', permanent=True)),

    path('home', views.overview, name='overview'),
]
