import pytest
from fastapi.testclient import TestClient

from little_nest.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
