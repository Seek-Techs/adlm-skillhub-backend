from django.db import IntegrityError
from rest_framework import serializers
from .models import AnalyticsEvent, ForumPost, JobListing, LearningResource, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
import os

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_verified', 'skills', 'progress', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    skills = serializers.ListField(child=serializers.CharField(), required=False)
    progress = serializers.FloatField(required=False, default=0.0)


    class Meta:
        model = User
        fields = ['email', 'password', 'role', 'skills', 'progress']

    def create(self, validated_data):
        email = validated_data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already registered.'})

        try:
            password = validated_data.pop('password')
            skills = validated_data.pop('skills', [])
            progress = validated_data.pop('progress', 0.0)
            user = User.objects.create_user(
                email=email,
                password=password,
                role=validated_data.get('role', 'Learner'),
                is_verified=False
            )
            user.skills = skills
            user.progress = progress
            user.save()
            # Send verification email
            self.send_verification_email(user)
            verification_link = f"http://localhost:8000/auth/verify/{uid}/{token}"
            send_verification_email.delay(user.email, verification_link)  # Async call

            return user
        except KeyError as e:
            raise serializers.ValidationError(f"Missing required field: {e}")
        except IntegrityError:
            raise serializers.ValidationError("Email already exists")
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred: {e}")

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = f"http://localhost:8000/auth/verify/{uid}/{token}"

        try:
            send_mail(
                'Verify Your Account',
                f'Click the link to verify your account: {verification_link}',
                os.getenv('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Handle the exception, e.g., log the error or return an error message
            print(f"Error sending email: {e}")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_verified:
            raise serializers.ValidationError('Email not verified')
        return data
    
class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = ['id', 'title', 'description', 'company', 'posted_at', 'is_active']

class AnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsEvent
        fields = ['id', 'user', 'event_type', 'timestamp', 'details']

class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = ['id', 'title', 'type', 'content', 'created_at', 'updated_at']

class AnalyticsSummarySerializer(serializers.Serializer):
    daily_active_users = serializers.IntegerField(read_only=True)
    total_resources_viewed = serializers.IntegerField(read_only=True)
    event_count = serializers.IntegerField(read_only=True)
    event_types = serializers.ListField(child=serializers.DictField(), read_only=True)