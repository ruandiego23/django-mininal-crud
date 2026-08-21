import pytest
from django.test import Client
from django.urls import reverse
from webdev.tasks.models import Task


@pytest.fixture
def task(db):
    return Task.objects.create(name='Example', done=True)


@pytest.fixture
def resp(client: Client, task):
    response = client.post(reverse('tasks:erase', kwargs={'task_id': task.id}))
    return response


def test_erase_task(resp):
    assert not Task.objects.exists()
