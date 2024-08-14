from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:pk>/delete/', views.delete_conversation, name='delete_conversation'),
]
