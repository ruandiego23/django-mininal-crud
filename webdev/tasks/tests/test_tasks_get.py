import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertContains

from webdev.tasks.models import Task


@pytest.fixture
def pending_tasks_list(db):
    tasks = [
        Task(name='Task 1', done=False),
        Task(name='Task 2', done=False),
    ]
    Task.objects.bulk_create(tasks)
    return tasks


@pytest.fixture
def resp_pending_tasks(client: Client, pending_tasks_list):
    return client.get(reverse('tasks:home'))


def test_status_code(resp_pending_tasks):
    assert resp_pending_tasks.status_code == 200


def test_home_title(resp_pending_tasks):
    assertContains(resp_pending_tasks, '<title>Tasks</title>')


def test_list_of_pending_tasks(resp_pending_tasks, pending_tasks_list):
    for task in pending_tasks_list:
        assertContains(resp_pending_tasks, task.name)
