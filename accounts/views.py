import os

from django.contrib.sessions.models import Session
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import UntypedToken
from django.utils import timezone
from django.db.models import Count
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import ForumPost, JobListing, User
from .serializers import ForumPostSerializer, JobListingSerializer, AnalyticsEventSerializer, UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, LearningResourceSerializer, AnalyticsSummarySerializer
from rest_framework.pagination import PageNumberPagination
from ai.models import AnalyticsEvent
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
import traceback
import logging


logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info(f"User registered: {user.email}")
                return Response({'message': 'User registered, check email'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                logger.error(f"Request data: {request.data}\n{traceback.format_exc()}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.warning(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'message': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)

# class VerifyEmailView(APIView):
#     def get(self, request, token):
#         try:
#             decoded = UntypedToken(token)
#             user_id = decoded['user_id']
#             user = User.objects.get(id=user_id)
#             user.is_verified = True
#             user.save()
#             return Response({'message': 'Email verified'})
#         except:
#             return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

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
    pagination_class = PageNumberPagination

    def initial(self, request, *args, **kwargs):
        # print(f"Permission check for user: {request.user}, authenticated: {request.user.is_authenticated}")
        super().initial(request, *args, **kwargs)

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
    pagination_class = PageNumberPagination

class JobListingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnalyticsSummary(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnalyticsSummarySerializer

    def get(self, request):
        today = timezone.now().date()
        daily_logins = User.objects.filter(last_login__date=today).count()
        total_resources_viewed = sum(getattr(user, 'resources_viewed', 0) for user in User.objects.all())

        event_types = AnalyticsEvent.objects.values('event_type').annotate(count=Count('id'))
        data = {
            'daily_active_users': daily_logins,
            'total_resources_viewed': total_resources_viewed,
            'event_count': AnalyticsEvent.objects.count(),
            'event_types': list(event_types),
        }
        serializer = AnalyticsSummarySerializer(data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            # Get the user from validated data
            user_data = serializer.validated_data
            user_id = user_data.get('user_id')  # Adjust based on your CustomTokenObtainPairSerializer
            user = User.objects.get(id=user_id) if user_id else None
            if user:
                user.update_login_stats()  # Update login stats for the authenticated user
            response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return response