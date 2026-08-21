import pytest
from django.test import Client
from django.urls import reverse

from webdev.tasks.models import Task


@pytest.fixture
def pending_task(db):
    return Task.objects.create(name='Test Task', done=False)


@pytest.fixture
def resp_with_pending_task(client: Client, pending_task):
    return client.post(
        reverse('tasks:detail', kwargs={'task_id': pending_task.id}),
        data={'done': 'true', 'name': f'{pending_task.name}-modified'},
    )


def test_pending_tasks_done(resp_with_pending_task):
    assert resp_with_pending_task.status_code == 302


def test_done_task(resp_with_pending_task):
    assert Task.objects.first().done


@pytest.fixture
def done_task(db):
    return Task.objects.create(name='Done Task', done=True)


@pytest.fixture
def resp_with_done_task(client: Client, done_task):
    return client.post(
        reverse(
            'tasks:detail', kwargs={'task_id': done_task.id}),
        data={'name': f'{done_task.name}-modified'},
    )


def test_pending_task(resp_with_done_task):
    assert not Task.objects.first().done
