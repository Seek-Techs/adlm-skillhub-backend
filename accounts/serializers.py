from django.db import IntegrityError
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import os

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_verified', 'skills', 'progress']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            user = User.objects.create_user(
                email=validated_data['email'],
                password=password,
                role=validated_data.get('role', 'Learner')
            )
            # Send verification email (async with Celery later)
            from django.core.mail import send_mail
            from rest_framework_simplejwt.tokens import UntypedToken
            token = UntypedToken.for_user(user)
            send_mail(
                'Verify Your Account',
                f'Click: http://localhost:8000/auth/verify/{token}',
                os.getenv('EMAIL_HOST_USER'),
                [user.email]
        )
        
            return user
        except KeyError as e:
            raise serializers.ValidationError(f"Missing required field: {e}")
        except IntegrityError:
            raise serializers.ValidationError("Email already exists")
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred: {e}")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_verified:
            raise serializers.ValidationError('Email not verified')
        return data