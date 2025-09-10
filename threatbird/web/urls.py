from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda request: redirect('web_overview', permanent=True), name="webredirect"),

    path('overview', views.web_overview, name='web_overview'),
    path('notifications', views.web_notifications, name='notifications'),
    path('example', views.example, name='example'),
]
