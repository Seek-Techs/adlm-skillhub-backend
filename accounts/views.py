import os

from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import UntypedToken

from .models import User
from .serializers import RegisterSerializer, UserSerializer


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