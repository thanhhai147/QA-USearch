from django.urls import path
from ..views.user import SignupAPIView, LoginAPIView, LogoutAPIView


urlpatterns = [
    path('signup', SignupAPIView.as_view(), name='signup'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='lgout'),
]