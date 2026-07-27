import pytest
from fastapi.testclient import TestClient
from main import app


import router.user as user
from data_constraints.input_schema import UsersRegisterSchema


client = TestClient(app)

@pytest.fixture
def sample_user():
    return UsersRegisterSchema(
        email="test_user@pytest.org",
        first_name="Pytest",
        last_name="TestUser",
        password="test_test_test_test",
        username="PytestTestUser",
    )


