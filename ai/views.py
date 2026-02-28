from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from .models import Recommendation, AnalyticsEvent
from accounts.models import LearningResource, ForumPost
import faiss
from sklearn.linear_model import LinearRegression
import numpy as np
from django.utils import timezone
from functools import lru_cache

import logging

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_text_generator():
    return pipeline("text-generation", model="gpt2")


@lru_cache(maxsize=1)
def get_sentence_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

class AICareerCoach(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use a prompt to guide the model
            prompt = f"Provide a structured response to the following query about a career path: {query}"
            generator = get_text_generator()
            response = generator(
                prompt,
                max_length=200,  # Increase to allow more text
                num_return_sequences=1,
                truncation=True,  # Explicitly enable truncation
                pad_token_id=generator.tokenizer.eos_token_id  # Ensure proper padding
            )[0]['generated_text']
            return Response({"advice": response})
        except Exception as e:
            logger.error(f"Error generating advice: {str(e)}")
            return Response({"error": "Failed to generate advice"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecommendationEngine(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        resources = list(LearningResource.objects.all())
        if not resources:
            return Response([])

        model = get_sentence_model()
        user_skills = " ".join(user.skills) if user.skills else ""
        user_embedding = model.encode([user_skills], convert_to_tensor=True)
        resource_contents = [resource.content for resource in resources]
        resource_embeddings = model.encode(resource_contents, convert_to_tensor=True)
        similarity_scores = util.cos_sim(user_embedding, resource_embeddings)[0]

        scores = []
        for resource, score_tensor in zip(resources, similarity_scores):
            score = float(score_tensor)
            Recommendation.objects.update_or_create(user=user, resource=resource, defaults={'score': score})
            scores.append({"resource": resource.title, "score": score})
        return Response(scores)
   
# from sentence_transformers import SentenceTransformer

class NaturalLanguageSearch(APIView):
    permission_classes = [AllowAny]

    _model = None
    _index = None
    _post_embeddings = None
    _posts = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = get_sentence_model()
        return cls._model

    @classmethod
    def initialize_index(cls):
        if cls._index is None:
            try:
                posts = list(ForumPost.objects.all())
                cls._posts = posts
                post_contents = [post.content for post in posts]
                if not post_contents:
                    logger.warning("No posts available for indexing")
                    return
                cls._post_embeddings = cls.get_model().encode(post_contents)
                logger.info(f"Generated embeddings for {len(post_contents)} posts")
                cls._index = faiss.IndexFlatL2(cls._post_embeddings.shape[1])
                cls._index.add(cls._post_embeddings)
                logger.info("FAISS index created successfully")
            except Exception as e:
                logger.error(f"Index initialization failed: {str(e)}")
                cls._index = None

    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Query is required"}, status=400)

        try:
            if self._index is None:
                self.initialize_index()
            if self._index is None or not self._posts:
                return Response({"error": "No posts available or index failed to initialize"}, status=404)

            query_embedding = self.get_model().encode([query])
            logger.info(f"Encoded query: {query}")
            distances, indices = self._index.search(query_embedding, k=min(5, len(self._posts)))
            result_posts = [self._posts[i] for i in indices[0] if i < len(self._posts)]
            results = [
                {
                    "title": post.title,
                    "content": post.content,
                    "created_at": post.created_at.isoformat(),
                    "distance": float(distances[0][j])
                }
                for j, post in enumerate(result_posts)
            ]
            return Response(results)
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return Response({"error": "Search failed"}, status=500)

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