import os

from django.contrib.sessions.models import Session
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import UntypedToken
from django.utils import timezone
from django.db.models import Count
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import AnalyticsEvent, ForumPost, JobListing, User
from .serializers import ForumPostSerializer, JobListingSerializer, AnalyticsEventSerializer, UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, LearningResourceSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({'message': 'User registered, check email'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            decoded = UntypedToken(token)
            user_id = decoded['user_id']
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified'})
        except:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Simple token storage (replace with DB in Phase 2)
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        try:
            decoded = UntypedToken(refresh_token)
            user_id = decoded['user_id']
            user = User.objects.get(id=user_id)
            # Store in session for now
            request.session['refresh_token'] = refresh_token
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken.for_user(user)
            return Response({'access_token': str(access_token)})
        except:
            return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

# Phase 2: Analytics and Forum
class ForumPostListCreate(generics.ListCreateAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ForumPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]

class JobListingListCreate(generics.ListCreateAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [permissions.IsAuthenticated]

class JobListingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnalyticsSummary(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        daily_logins = User.objects.filter(last_login__date=today).count()
        total_resources_viewed = sum(user.resources_viewed for user in User.objects.all())
        data = {
            'daily_active_users': daily_logins,
            'total_resources_viewed': total_resources_viewed,
            'event_count': AnalyticsEvent.objects.count(),
        }
        return Response(data)
    
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = request.user
        user.update_login_stats()
        return response