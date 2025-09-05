import os

from django.contrib.sessions.models import Session
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import UntypedToken
from django.utils import timezone
from django.db.models import Count, Sum
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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache


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
    permission_classes = [AllowAny]

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

class AnalyticsSummary(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request):
        try:
            # Check cache first with error handling
            cache_key = f"analytics_summary_{request.user.id}"
            cached_data = None
            try:
                cached_data = cache.get(cache_key)
            except Exception as cache_e:
                logger.error(f"Cache connection failed: {str(cache_e)}")
            if cached_data is not None:
                logger.info(f"Cache hit for user {request.user.id}")
                return Response(cached_data)

            today = timezone.now().date()
            logger.info(f"Fetching analytics for date: {today}")

            # Database queries with error handling
            try:
                daily_logins = User.objects.filter(last_login__date=today).count()
                logger.info(f"Daily logins count: {daily_logins}")
            except Exception as db_e:
                logger.error(f"Database error for daily logins: {str(db_e)}")
                daily_logins = 0

            try:
                total_resources_query = User.objects.aggregate(total_resources=Sum('resources_viewed'))
                total_resources_viewed = total_resources_query['total_resources'] if total_resources_query['total_resources'] is not None else 0
                logger.info(f"Total resources viewed: {total_resources_viewed}")
            except Exception as db_e:
                logger.error(f"Database error for resources viewed: {str(db_e)}")
                total_resources_viewed = 0

            try:
                event_types = AnalyticsEvent.objects.values('event_type').annotate(count=Count('id'))
                event_count = AnalyticsEvent.objects.count()
                logger.info(f"Event count: {event_count}, Event types: {list(event_types)}")
            except Exception as db_e:
                logger.error(f"Database error for events: {str(db_e)}")
                event_types = []
                event_count = 0

            data = {
                'daily_active_users': daily_logins,
                'total_resources_viewed': total_resources_viewed,
                'event_count': event_count,
                'event_types': list(event_types),
            }
            serializer = AnalyticsSummarySerializer(data)
            response_data = serializer.data

            # Cache the result per user, handle failure
            try:
                cache.set(cache_key, response_data, timeout=60 * 5)
                logger.info(f"Cache set for user {request.user.id}")
            except Exception as cache_e:
                logger.error(f"Cache error: {str(cache_e)}")

            return Response(response_data)
        except Exception as e:
            logger.error(f"Analytics summary error: {str(e)}", exc_info=True)
            return Response({"error": "Failed to retrieve analytics"}, status=500)
    
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