from django.urls import path
from .views import RegisterView, LoginView, ProfileView, RefreshTokenView, ForumPostListCreate, ForumPostRetrieveUpdateDestroy, JobListingListCreate, JobListingRetrieveUpdateDestroy, AnalyticsSummary, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('token/', LoginView.as_view(), name='token_obtain_pair'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('api/forum-posts/', ForumPostListCreate.as_view(), name='forumpost-list'),
    path('api/forum-posts/<int:pk>/', ForumPostRetrieveUpdateDestroy.as_view(), name='forumpost-detail'),
    path('api/job-listings/', JobListingListCreate.as_view(), name='joblisting-list'),
    path('api/job-listings/<int:pk>/', JobListingRetrieveUpdateDestroy.as_view(), name='joblisting-detail'),
    path('api/analytics/summary/', AnalyticsSummary.as_view(), name='analytics-summary'),
]