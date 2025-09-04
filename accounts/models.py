from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from argon2 import PasswordHasher


ph = PasswordHasher()

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('Learner', 'Learner'), ('Mentor', 'Mentor'), ('Admin', 'Admin')], default='Learner')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete

    last_login_time = models.DateTimeField(null=True, blank=True)
    login_count = models.PositiveIntegerField(default=0, db_index=True)
    resources_viewed = models.PositiveIntegerField(default=0, db_index=True)

    # Profile fields
    skills = models.JSONField(default=list)
    progress = models.FloatField(default=0.0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        self.password = ph.hash(raw_password)

    def check_password(self, raw_password):
        try:
            return ph.verify(self.password, raw_password)
        except:
            return False
        
    def update_login_stats(self):
        self.login_count += 1
        self.last_login_time = timezone.now()
        self.save()
        
class LearningResource(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[('Course', 'Course'), ('Tutorial', 'Tutorial')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

# Phase 2 Models
class ForumPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class JobListing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
    
class AnalyticsEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50)  # e.g., 'login', 'resource_view'
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.event_type} at {self.timestamp}"