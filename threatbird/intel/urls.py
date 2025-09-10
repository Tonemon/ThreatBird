from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda request: redirect('overview', permanent=True)),

    path('overview', views.kb_overview, name='kb_overview'),
]
