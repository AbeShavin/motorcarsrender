# car_listing/urls.py

from django.urls import path
from . import views
from .views import load_models

urlpatterns = [
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/new/', views.car_create, name='car_create'),
    path('car/<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('car/<int:pk>/delete/', views.car_delete, name='car_delete'),
    path('', views.car_search, name='car_search'),
    path('search_results/', views.search_results, name='search_results'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('car/<int:car_id>/add-favorite/', views.add_favorite, name='add_favorite'),
    path('car/<int:car_id>/remove-favorite/', views.remove_favorite, name='remove_favorite'),
    path('ajax/load-models/', load_models, name='ajax_load_models'),
]
 