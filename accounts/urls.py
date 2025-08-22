from django.urls import path
from .views import RegisterView, VerifyEmailView, ProfileView, RefreshTokenView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify/<str:token>/', VerifyEmailView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('refresh/', RefreshTokenView.as_view()),
]