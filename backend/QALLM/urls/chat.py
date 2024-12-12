from django.urls import path
from ..views.chat import CreateChatAPIView, GetChatAPIView, DeleteChatAPIView


urlpatterns = [
    path('create-chat', CreateChatAPIView.as_view(), name='create-chat'),
    path('get-chat', GetChatAPIView.as_view(), name='get-chat'),
    path('delete-chat', DeleteChatAPIView.as_view(), name='delete-chat')
]