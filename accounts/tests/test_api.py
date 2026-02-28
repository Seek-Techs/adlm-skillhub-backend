from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from accounts.models import ForumPost, JobListing, User

class AuthApiTest(APITestCase):
    def test_register_api(self):
        url = reverse('register')
        data = {"email": "api@ex.com", "password": "apipass", "role": "Learner"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    def test_token_api(self):
        User.objects.create_user(email="token@ex.com", password="tokenpass", role="Learner", is_verified=True)
        url = reverse('token_obtain_pair')
        data = {"email": "token@ex.com", "password": "tokenpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertIn("access", response.data["data"])


    def test_token_api_rejects_unverified_user(self):
        User.objects.create_user(email="unverified@ex.com", password="tokenpass", role="Learner", is_verified=False)
        url = reverse('token_obtain_pair')
        data = {"email": "unverified@ex.com", "password": "tokenpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_token_api_updates_login_stats(self):
        user = User.objects.create_user(email="stats@ex.com", password="tokenpass", role="Learner", is_verified=True)
        url = reverse('token_obtain_pair')
        data = {"email": "stats@ex.com", "password": "tokenpass"}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        user.refresh_from_db()
        self.assertEqual(user.login_count, 1)
        self.assertIsNotNone(user.last_login_time)


    def test_refresh_token_api(self):
        user = User.objects.create_user(email="refresh@ex.com", password="tokenpass", role="Learner", is_verified=True)
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh_token = str(RefreshToken.for_user(user))
        url = '/auth/refresh/'
        response = self.client.post(url, {'refresh_token': refresh_token}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertIn("access_token", response.data["data"])

    def test_refresh_token_api_rejects_invalid_token(self):
        url = '/auth/refresh/'
        response = self.client.post(url, {'refresh_token': 'not-a-token'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid refresh token")

    def test_refresh_token_api_requires_token(self):
        url = '/auth/refresh/'
        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "refresh_token is required")

    def test_register_api_invalid_payload_returns_error_envelope(self):
        url = reverse('register')
        response = self.client.post(url, {'role': 'Learner'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_verify_email_invalid_link_returns_error_envelope(self):
        url = '/auth/verify/invalid/invalid-token/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

class ForumPostApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="forum@ex.com", password="pass", role="Learner")
        self.url_forum_list = reverse('forumpost-list')
        self.url_job_list = reverse('joblisting-list')
        self.url_analytics = reverse('analytics-summary')

    def test_create_forum_post(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "New Post", "content": "New Content"}
        response = self.client.post(self.url_forum_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Post")
        self.assertEqual(response.data["author"], self.user.id)

    def test_get_forum_post(self):
        self.client.force_authenticate(user=self.user)
        post = ForumPost.objects.create(title="Existing Post", content="Content", author=self.user)
        url = reverse('forumpost-detail', kwargs={'pk': post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Existing Post")

    def test_create_job_listing(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "New Job", "description": "Part-time", "company": "NewCo"}
        response = self.client.post(self.url_job_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Job")

    def test_get_job_listing(self):
        self.client.force_authenticate(user=self.user)
        job = JobListing.objects.create(title="Old Job", description="Full-time", company="OldCo")
        url = reverse('joblisting-detail', kwargs={'pk': job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Old Job")

    def test_analytics_summary(self):
        active_user = User.objects.create_user(email="active@ex.com", password="pass", role="Learner")
        active_user.last_login_time = timezone.now()
        active_user.save(update_fields=["last_login_time"])

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_analytics)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("daily_active_users", response.data)
        self.assertGreaterEqual(response.data["daily_active_users"], 1)

    def test_unauthorized_forum_post_create(self):
        client = APIClient()  # Fresh unauthenticated client
        data = {"title": "Unauthorized Post", "content": "Content"}
        response = client.post(self.url_forum_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_id_header_is_returned(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_forum_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('X-Request-ID', response)

