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
    Sample REST API application
    """
    resp = api_client.get('/')

    assert b'hello world!' in resp.data
