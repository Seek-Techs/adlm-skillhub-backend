from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from .models import Recommendation, AnalyticsEvent
from accounts.models import LearningResource, ForumPost
import faiss
from rest_framework import permissions
from sklearn.linear_model import LinearRegression
import numpy as np


class AICareerCoach(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        generator = pipeline("text-generation", model="gpt2")  # Replace with better model for production
        response = generator(query, max_length=50, num_return_sequences=1)[0]['generated_text']
        return Response({"advice": response})


class RecommendationEngine(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        resources = LearningResource.objects.all()
        model = SentenceTransformer('all-MiniLM-L6-v2')
        user_skills = " ".join(user.skills) if user.skills else ""
        user_embedding = model.encode(user_skills)
        scores = []
        for resource in resources:
            resource_embedding = model.encode(resource.content)
            score = util.cos_sim(user_embedding, resource_embedding)[0][0]
            Recommendation.objects.update_or_create(user=user, resource=resource, defaults={'score': score})
            scores.append({"resource": resource.title, "score": score})
        return Response(scores)
    
    

# from sentence_transformers import SentenceTransformer


class NaturalLanguageSearch(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        model = SentenceTransformer('all-MiniLM-L6-v2')
        posts = list(ForumPost.objects.all())  # Convert to list for indexing
        post_contents = [post.content for post in posts]
        if not post_contents:
            return Response({"error": "No posts available"}, status=status.HTTP_404_NOT_FOUND)

        embeddings = model.encode(post_contents)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        query_embedding = model.encode([query])
        distances, indices = index.search(query_embedding, min(5, len(posts)))  # Limit to available posts
        # Use indices to get corresponding posts from the list
        result_posts = [posts[i] for i in indices[0] if i < len(posts)]  # Ensure index is valid
        return Response([{"title": post.title, "content": post.content} for post in result_posts])
    


class PredictiveAnalytics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = AnalyticsEvent.objects.filter(event_type='login').order_by('timestamp')
        if not events:
            return Response({"forecast": "No data"})
        timestamps = [event.timestamp.timestamp() for event in events]
        X = np.array(timestamps).reshape(-1, 1)
        y = np.arange(len(events))  # Sequential engagement
        model = LinearRegression()
        model.fit(X, y)
        future_timestamp = (timezone.now() + timezone.timedelta(days=1)).timestamp()
        forecast = model.predict([[future_timestamp]])
        return Response({"forecasted_engagement": int(forecast[0])})