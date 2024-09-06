import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(username, password, email):
        return User.objects.create_user(username=username, password=password, email=email)
    return _create_user

@pytest.mark.django_db
def test_get_all_users(api_client, create_user):
    create_user('testuser1', 'testpassword1', 'testuser1@example.com')
    create_user('testuser2', 'testpassword2', 'testuser2@example.com')
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

@pytest.mark.django_db
def test_register_new_user(api_client):
    url = reverse('register-user')
    data = {
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_registration_validation_errors(api_client):
    url = reverse('register-user')
    response = api_client.post(url, {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert 'password' in response.data

    User.objects.create_user(username='existinguser', password='password123', email='existing@example.com')
    data = {
        'username': 'existinguser',
        'password': 'newpassword',
        'email': 'newuser@example.com'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data

    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'invalid-email'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

@pytest.mark.django_db
def test_get_user_info(api_client, create_user):
    user = create_user('user1', 'password', 'user1@example.com')
    url = reverse('user-detail', args=[user.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == 'user1'
    assert response.data['email'] == 'user1@example.com'
    assert 'first_name' in response.data
    assert 'last_name' in response.data
    assert 'phone' in response.data
    assert 'position' in response.data
    assert 'project' in response.data

@pytest.mark.django_db
def test_get_user_info_not_found(api_client):
    url = reverse('user-detail', args=[999])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No User matches the given query.'

