from django.urls import path
from .views import LoginView, RegisterView, LogoutView, UserProfileView, LoginStatusView, profile_page

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/profile/', UserProfileView.as_view(), name='api-profile'),
    path('api/login-status/', LoginStatusView.as_view(), name='api-login-status'),
    path('profile.html', profile_page, name='profile-page'), 
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
]