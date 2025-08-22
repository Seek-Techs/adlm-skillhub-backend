import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from accounts.models import User, LearningResource

User.objects.all().delete()
LearningResource.objects.all().delete()

admin = User.objects.create_superuser(email='admin@example.com', password='password')
resource = LearningResource.objects.create(title='Intro to React', type='Tutorial', content='...')
print('Seeded')


