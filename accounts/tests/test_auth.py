import pytest
from rest_framework.test import APIClient
from accounts.models import User

@pytest.mark.django_db
def test_register():
    client = APIClient()
    response = client.post('/auth/register/', {'email': 'test@example.com', 'password': 'password', 'role': 'Learner'})
    assert response.status_code == 201