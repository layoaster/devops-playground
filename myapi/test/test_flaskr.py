import pytest

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
    assert 'Hello World!' in resp.json


def test_hello_world_counter(api_client):
    """
    Test the helloworld page hit counter increments.
    """
    first_resp = api_client.get('/')
    second_resp = api_client.get('/')

    init_count = first_resp.json['Hello World!']
    inc_count = second_resp.json['Hello World!']

    assert inc_count == init_count + 1
