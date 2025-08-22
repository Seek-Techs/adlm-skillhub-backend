from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import force_authenticate

from accounts.models import ForumPost, JobListing, User

class AuthApiTest(APITestCase):
    def test_register_api(self):
        url = reverse('register')
        data = {"email": "api@ex.com", "password": "apipass", "role": "Learner"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    def test_token_api(self):
        User.objects.create_user(email="token@ex.com", password="tokenpass", role="Learner")
        url = reverse('token_obtain_pair')
        data = {"email": "token@ex.com", "password": "tokenpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

class ForumPostApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="forum@ex.com", password="pass", role="Learner")
        self.client.force_authenticate(user=self.user)

    def test_create_forum_post(self):
        url = reverse('forumpost-list')
        data = {"title": "New Post", "content": "New Content"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Post")
        self.assertEqual(response.data["author"], self.user.id)

    def test_get_forum_post(self):
        post = ForumPost.objects.create(title="Existing Post", content="Content", author=self.user)
        url = reverse('forumpost-detail', kwargs={'pk': post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Existing Post")

    def test_create_job_listing(self):
        url = reverse('joblisting-list')
        data = {"title": "New Job", "description": "Part-time", "company": "NewCo"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Job")

    def test_get_job_listing(self):
        job = JobListing.objects.create(title="Old Job", description="Full-time", company="OldCo")
        url = reverse('joblisting-detail', kwargs={'pk': job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Old Job")

    def test_analytics_summary(self):
        url = reverse('analytics-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("daily_active_users", response.data)
        # Add more assertions after populating data