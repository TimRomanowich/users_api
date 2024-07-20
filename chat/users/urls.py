from django.urls import path
from .views import LoginView, RegisterView, LogoutView, UserProfileView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/profile/', UserProfileView.as_view(), name='api-profile'),
]