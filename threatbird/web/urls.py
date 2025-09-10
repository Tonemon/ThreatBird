from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = "web"
urlpatterns = [
    path('', lambda request: redirect('overview', permanent=True), name="webredirect"),

    path('overview', views.overview, name='overview'),
    path('notifications', views.notifications, name='notifications'),
    path('example', views.example, name='example'),
]
