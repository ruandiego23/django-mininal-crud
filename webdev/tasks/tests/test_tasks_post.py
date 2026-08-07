import pytest
from django.test import Client
from django.urls import reverse
from webdev.tasks.models import Task


@pytest.fixture
def resp(client: Client, db):
    # to create a post, use data= {'name': 'Task'}
    return client.post(reverse('tasks:home'), data={'name': 'Task'})


def test_task_exists(resp):
    # You'll need to modify the views to receive the post and create a forms file
    assert Task.objects.exists()


def test_redirect_page_after_saved(resp):
    assert resp.status_code == 302


@pytest.fixture
def data_invalid(client: Client, db):
    return client.post(reverse('tasks:home'), data={'name': ''})


def test_task_not_exists(data_invalid):
    assert not Task.objects.exists()


def test_data_invalid(data_invalid):
    assert data_invalid.status_code == 400
