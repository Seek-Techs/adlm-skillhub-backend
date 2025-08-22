from django.test import TestCase
from accounts.models import ForumPost, JobListing, LearningResource, User, UserManager

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@ex.com", password="testpass", role="Learner")

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@ex.com")
        self.assertEqual(self.user.role, "Learner")
        self.assertTrue(self.user.check_password("testpass"))
        self.assertFalse(self.user.is_staff)

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(email="admin@ex.com", password="adminpass", role="Admin")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_learning_resource_creation(self):
        resource = LearningResource.objects.create(title="Intro to Django", type="Tutorial", content="Content")
        self.assertEqual(str(resource), "Intro to Django")
        self.assertEqual(resource.type, "Tutorial")

    def test_forum_post_creation(self):
        user = User.objects.create_user(email="post@ex.com", password="pass", role="Learner")
        post = ForumPost.objects.create(title="Test Post", content="Content", author=user)
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.author, user)

    def test_job_listing_creation(self):
        job = JobListing.objects.create(title="Dev Job", description="Full-time", company="TechCo")
        self.assertEqual(str(job), "Dev Job at TechCo")
        self.assertTrue(job.is_active)