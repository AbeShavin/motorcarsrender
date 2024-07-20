# car_listing/urls.py

from django.urls import path
from . import views
from .views import car_search

urlpatterns = [
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/new/', views.car_create, name='car_create'),
    path('car/<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('car/<int:pk>/delete/', views.car_delete, name='car_delete'),
    path('', views.car_search, name='car_search'),
]
 