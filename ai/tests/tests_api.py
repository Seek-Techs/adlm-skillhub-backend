from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User, ForumPost
from ai.models import AnalyticsEvent
from django.utils import timezone
from unittest.mock import patch
import numpy as np
from ai.views import get_ai_latency_warn_ms
from unittest import TestCase
import os




class FakeSentenceModel:
    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        # deterministic tiny embeddings for tests
        return np.array([[float(len(text))] for text in texts], dtype='float32')


class NaturalLanguageSearchTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sentence_model_patcher = patch('ai.views.get_sentence_model', return_value=FakeSentenceModel())
        cls.sentence_model_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.sentence_model_patcher.stop()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(email="search@ex.com", password="pass", role="Learner")
        self.post1 = ForumPost.objects.create(title="Test Post 1", content="This is a test", author=self.user)
        self.post2 = ForumPost.objects.create(title="Test Post 2", content="Another test content", author=self.user)
        self.url = reverse('search')

    def test_search_valid_query(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {'query': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_search_no_query(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

class PredictiveAnalyticsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="predict@ex.com", password="pass", role="Learner")
        for i in range(5):
            AnalyticsEvent.objects.create(
                user=self.user,
                event_type='login',
                details={"ip": f"192.168.1.{i}"},
                timestamp=timezone.now() - timezone.timedelta(days=i)
            )
        self.url = reverse('predictive')

    def test_predictive_analytics(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("forecasted_engagement", response.data)

class AILatencyThresholdTest(TestCase):
    def test_ai_latency_warn_threshold_default(self):
        original = os.environ.pop('AI_LATENCY_WARN_MS', None)
        try:
            self.assertEqual(get_ai_latency_warn_ms(), 1500.0)
        finally:
            if original is not None:
                os.environ['AI_LATENCY_WARN_MS'] = original

    def test_ai_latency_warn_threshold_override(self):
        original = os.environ.get('AI_LATENCY_WARN_MS')
        os.environ['AI_LATENCY_WARN_MS'] = '2200'
        try:
            self.assertEqual(get_ai_latency_warn_ms(), 2200.0)
        finally:
            if original is None:
                os.environ.pop('AI_LATENCY_WARN_MS', None)
            else:
                os.environ['AI_LATENCY_WARN_MS'] = original

