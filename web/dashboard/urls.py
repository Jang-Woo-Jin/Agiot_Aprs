from django.urls import path
from . import views
urlpatterns = [
    path('', views.dash_farm, name='dash_farm'),
    path('dashboard/farm/', views.dash_farm, name='dash_farm'),
    path('dashboard/sensor/', views.dash_farm, name='dash_farm'),
]