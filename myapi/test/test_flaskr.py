from unittest.mock import patch

import pytest
from redis.exceptions import ConnectionError

from myapi.app import app


@pytest.fixture
def api_client():
    """
    Initializes the application to be used in tests.
    """
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_hello_world(api_client):
    """
    Sample REST API application.
    """
    resp = api_client.get('/')

    assert isinstance(resp.json, dict)
    assert resp.json
    assert 'Hello-World! hits' in resp.json


def test_hello_world_counter(api_client):
    """
    Tests the helloworld page hit counter increments.
    """
    first_resp = api_client.get('/')
    second_resp = api_client.get('/')

    init_count = first_resp.json['Hello-World! hits']
    inc_count = second_resp.json['Hello-World! hits']

    assert inc_count == init_count + 1


def test_health_check(api_client):
    """
    Tests the app's health check handler.
    """
    # App is not healty
    with patch('myapi.app.redis.Redis.info', side_effect=ConnectionError):
        resp = api_client.get('/healthz')

        assert resp.status_code == 503
        assert resp.json['status'] == 'fail'

    # App is healty
    resp = api_client.get('/healthz')

    assert resp.status_code == 200
    assert resp.json['status'] == 'pass'
