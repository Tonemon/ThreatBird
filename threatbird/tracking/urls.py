from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = "tracking"
urlpatterns = [
    path('', lambda request: redirect('overview', permanent=True)),

    path('start', views.start, name='overview'),
]
