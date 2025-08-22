from django.db import models
from accounts.models import User, LearningResource
from django.utils import timezone


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(LearningResource, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"Recommendation for {self.user.email}: {self.resource.title}"
    

class AnalyticsEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_events')
    event_type = models.CharField(max_length=50, choices=[
        ('login', 'Login'),
        ('resource_view', 'Resource View'),
        ('forum_post', 'Forum Post'),
    ])
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.event_type} by {self.user.email} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']