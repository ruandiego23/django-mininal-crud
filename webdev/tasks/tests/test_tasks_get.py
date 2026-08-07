import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertContains


@pytest.fixture
def resp(client: Client):
    return client.get(reverse('tasks:home'))


def test_status_page_working(resp):
    assert resp.status_code == 200


def test_title(resp):
    assertContains(resp, '<title>Tasks</title>')
