from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_vehicle_profile, name='create_vehicle_profile'),
    path('<int:pk>/edit/', views.edit_vehicle_profile, name='edit_vehicle_profile'),
    path('<int:pk>/delete/', views.delete_vehicle_profile, name='delete_vehicle_profile'),
    path('<int:pk>/', views.vehicle_profile_detail, name='vehicle_profile_detail'),
    path('dashboard/', views.vehicle_profile_dashboard, name='vehicle_profile_dashboard'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),  # Add this line
]

