import uuid
import socket
import pytest

from riemann import clients
from riemann import riemann_pb2


@pytest.fixture
def unique():
    return str(uuid.uuid4())


@pytest.fixture
def event(unique):
    return clients.create_event({
        'host': 'test.example.com',
        'tags': [unique],
        'attributes': {
            unique: unique
        },
    })


@pytest.fixture
def response(event):
    return clients.parse_event(event)


def test_create_event(event, unique):
    assert event.host == 'test.example.com'
    assert event.tags == [unique]
    assert event.attributes[0].key == unique
    assert event.attributes[0].value == unique


def test_autosize_metric_value():
    event = riemann_pb2.Event()

    clients.autosize_metric_value(event, 1)
    assert event.metric_sint64 == 1
    assert event.metric_f == float(1)
    assert event.metric_d == 0


def test_parse_event(event, response):
    assert event.host == response['host']
    assert isinstance(event.host, str)
    assert set(event.tags) == set(response['tags'])

    assert isinstance(response['attributes'], dict)
    for attr in event.attributes:
        assert response['attributes'][attr.key] == attr.value
