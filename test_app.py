import os
import pytest

from app import app  # Assumes your main Flask code is in app.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # You may want to set a dummy HOSTNAME for deterministic output
    os.environ['HOSTNAME'] = 'test-host'
    with app.test_client() as client:
        yield client

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'HelloWorld version:' in response.data
    assert b'test-host' in response.data  # HOSTNAME from ENV

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'Helloworld is healthy' in response.data
