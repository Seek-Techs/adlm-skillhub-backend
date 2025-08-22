from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AnalyticsEvent, ForumPost, JobListing, User, LearningResource

# Define the admin class for the custom User model
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_verified', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register the models
admin.site.register(User, CustomUserAdmin)
admin.site.register(LearningResource)
admin.site.register(ForumPost)
admin.site.register(JobListing)
admin.site.register(AnalyticsEvent)