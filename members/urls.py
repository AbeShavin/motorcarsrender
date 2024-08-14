from django.urls import path
from .views import members, profile_view, member_conversations

urlpatterns = [
    path('', members, name='members'),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('conversations/', member_conversations, name='member_conversations')
]