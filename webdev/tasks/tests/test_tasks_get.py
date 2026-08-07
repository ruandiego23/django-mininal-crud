import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertContains

from webdev.tasks.models import Task


@pytest.fixture
def resp(client: Client, db):
    return client.get(reverse('tasks:home'))


def test_status_page_working(resp):
    assert resp.status_code == 200


def test_title(resp):
    assertContains(resp, '<title>Tasks</title>')


@pytest.fixture
def list_of_pending_tasks(db):
    tarefas = [
        Task(name='Task 1', done=False),
        Task(name='Task 2', done=False),
    ]
    Task.objects.bulk_create(tarefas)
    return tarefas


@pytest.fixture
def resp_with_pending_tasks(client: Client, list_of_pending_tasks):
    response = client.get(reverse('tasks:home'))
    return response


def test_list_of_pending_tasks(resp_with_pending_tasks, list_of_pending_tasks):
    for task in list_of_pending_tasks:
        assertContains(resp_with_pending_tasks, task.name)
