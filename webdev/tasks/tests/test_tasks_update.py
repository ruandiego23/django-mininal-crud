import pytest
from django.test import Client
from django.urls import reverse
from webdev.tasks.models import Task


@pytest.fixture
def pending_task(db):
    # to create a post, use data= {'name': 'Task'}
    return Task.objects.create(name='Pending Task', done=False)


@pytest.fixture
def resp_pending(client: Client, pending_task):
    # You'll need to modify the views, the model and the forms
    return client.post(reverse('tasks:detail', kwargs={'task_id': pending_task.id}),
                       data={'done': 'true', 'name': f'{pending_task.name}-modified'},)


def test_redirect_page_after_modifying(resp_pending):
    assert resp_pending.status_code == 302


def test_task_done(resp_pending):
    assert Task.objects.first().done


@pytest.fixture
def done_task(db):
    # to create a post, use data= {'name': 'Task'}
    return Task.objects.create(name='Done Task', done=True)


@pytest.fixture
def resp_done(client: Client, done_task):
    # You'll need to modify the views, the model and the forms
    return client.post(reverse('tasks:detail', kwargs={'task_id': done_task.id}),
                       data={'name': f'{done_task.name}-modified'},)


def test_task_pending(resp_done):
    assert not Task.objects.first().done
