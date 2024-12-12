from django.urls import path
from ..views.session import CreateSessionAPIView, GetSessionByUserIdAPIView, DeleteSessionAPIView, UpdateSessionNameAPIView


urlpatterns = [
    path('create-session', CreateSessionAPIView.as_view(), name='create-session'),
    path('get-session', GetSessionByUserIdAPIView.as_view(), name='get-session'),
    path('delete-session', DeleteSessionAPIView.as_view(), name='delete-session'),
    path('update-session-name', UpdateSessionNameAPIView.as_view(), name='update-session-name')
]