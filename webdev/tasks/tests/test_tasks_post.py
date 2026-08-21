import pytest
from django.test import Client
from django.urls import reverse

from webdev.tasks.models import Task


@pytest.fixture
def resp_with_valid_data(client: Client, db):
    return client.post(reverse('tasks:home'), data={'name': 'Test Task'})


def test_task_exists(resp_with_valid_data):
    assert Task.objects.exists()


def test_redirect_page_after_save_db(resp_with_valid_data):
    assert resp_with_valid_data.status_code == 302


@pytest.fixture
def invalid_data(client: Client, db):
    return client.post(reverse('tasks:home'), data={'name': ''})


def test_task_not_found(invalid_data):
    assert not Task.objects.exists()


def test_redirect_invalid_data(invalid_data):
    assert invalid_data.status_code == 400
