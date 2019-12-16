from django.urls import path
from . import views
urlpatterns = [
    path('', views.dash_farm, name='dash_farm'),
    path('dashboard/farm/', views.dash_farm, name='dash_farm'),
    path('dashboard/farm/create', views.farm_create, name='farm_create'),
    path('dashboard/farm/<int:id>', views.farm_detail, name='farm_detail'),
    path('dashboard/sensor/', views.dash_farm, name='dash_farm'),
]