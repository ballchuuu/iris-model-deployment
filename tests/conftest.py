import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def auth_client():
    from app.main import app
    client = TestClient(app)
    return client