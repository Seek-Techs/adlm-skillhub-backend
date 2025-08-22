from django.test import TestCase, RequestFactory
from accounts.models import User
from accounts.views import AnalyticsSummary, ProfileView, RegisterView
from accounts.serializers import RegisterSerializer
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = RegisterView.as_view()

    def test_register_success(self):
        data = {"email": "new@ex.com", "password": "newpass", "role": "Learner"}
        request = self.factory.post("/auth/register/", data, format="json")
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.data)

    def test_register_duplicate_email(self):
        User.objects.create_user(email="dup@ex.com", password="pass", role="Learner")
        data = {"email": "dup@ex.com", "password": "newpass", "role": "Learner"}
        request = self.factory.post("/auth/register/", data, format="json")
        response = self.view(request)
        self.assertEqual(response.status_code, 400)


class AnalyticsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="ana@ex.com", password="pass", role="Learner")
        self.factory = RequestFactory()
        self.view = AnalyticsSummary.as_view()

    def test_analytics_summary(self):
        request = self.factory.get("/auth/api/analytics/summary/")
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("daily_active_users", response.data)
        self.assertIn("total_resources_viewed", response.data)
        self.assertIn("event_count", response.data)

class LoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email="login@ex.com", password="loginpass", role="Learner")

    def test_login_success(self):
        url = '/token/'  # Match core/urls.py
        data = {"email": "login@ex.com", "password": "loginpass"}
        request = self.factory.post(url, data, format="json")
        response = TokenObtainPairView.as_view()(request)  # Use TokenObtainPairView directly
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email="profile@ex.com", password="pass", role="Learner")
        self.url = '/auth/profile/'  # Match core/urls.py

    def test_profile_access(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "profile@ex.com")

class LoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email="login@ex.com", password="loginpass", role="Learner")

    def test_login_success(self):
        url = '/token/'  # Matches core/urls.py
        data = {"email": "login@ex.com", "password": "loginpass"}
        request = self.factory.post(url, data, format="json")
        response = TokenObtainPairView.as_view()(request)  # Use TokenObtainPairView directly
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)