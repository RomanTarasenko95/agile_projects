import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from apps.tasks.models import Task, Project

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(username, password, email):
        return User.objects.create_user(username=username, password=password, email=email)

    return _create_user


@pytest.fixture
def create_task(create_user):
    def _create_task(name, description, priority, project_name, owner):
        project, _ = Project.objects.get_or_create(name=project_name)
        return Task.objects.create(
            name=name,
            description=description,
            priority=priority,
            project=project,
            owner=owner
        )

    return _create_task


@pytest.mark.django_db
def test_create_task(api_client, create_user):
    user = create_user('taskuser', 'taskpassword', 'taskuser@example.com')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    url = reverse('task-list-create')
    data = {
        'name': 'New Task',
        'description': 'New Task Description',
        'priority': 1,
        'project': 'New Project',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.filter(name='New Task').exists()


@pytest.mark.django_db
def test_get_all_tasks(api_client, create_user, create_task):
    user = create_user('taskuser', 'taskpassword', 'taskuser@example.com')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    create_task('Task 1', 'Description 1', 1, 'Project 1', user)
    create_task('Task 2', 'Description 2', 2, 'Project 2', user)

    url = reverse('task-list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_task_detail(api_client, create_user, create_task):
    user = create_user('taskuser', 'taskpassword', 'taskuser@example.com')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    task = create_task('Task 1', 'Description 1', 1, 'Project 1', user)
    url = reverse('task-detail', args=[task.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Task 1'
    assert response.data['description'] == 'Description 1'


@pytest.mark.django_db
def test_update_task(api_client, create_user, create_task):
    user = create_user('taskuser', 'taskpassword', 'taskuser@example.com')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    task = create_task('Task 1', 'Description 1', 1, 'Project 1', user)
    url = reverse('task-detail', args=[task.id])
    data = {'description': 'Updated Description'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert Task.objects.get(id=task.id).description == 'Updated Description'


@pytest.mark.django_db
def test_delete_task(api_client, create_user, create_task):
    user = create_user('taskuser', 'taskpassword', 'taskuser@example.com')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    task = create_task('Task 1', 'Description 1', 1, 'Project 1', user)
    url = reverse('task-detail', args=[task.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(id=task.id).exists()
