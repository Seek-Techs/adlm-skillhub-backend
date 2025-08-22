from django.urls import path
from .views import AICareerCoach, NaturalLanguageSearch, PredictiveAnalytics, RecommendationEngine

urlpatterns = [
    path('career-coach/', AICareerCoach.as_view(), name='career-coach'),
    path('recommendations/', RecommendationEngine.as_view(), name='recommendations'),
    path('search/', NaturalLanguageSearch.as_view(), name='search'),
    path('predictive/', PredictiveAnalytics.as_view(), name='predictive'),
]