import uuid

import pytest
from fastapi.testclient import TestClient

from database import Users
from main import app
from data_constraints.input_schema import UsersRegisterSchema


client = TestClient(app)

@pytest.fixture
def sample_user():
    _username = str(uuid.uuid4().hex)
    _password = str(uuid.uuid4())
    return UsersRegisterSchema(
        email=f"{_username}@pytest.org",
        first_name="Pytest",
        last_name="TestUser",
        password=_password,
        username=_username
    )



def test_register_user(sample_user, test_db):
    sample_user_to_register = sample_user.model_dump()
    sample_user_username = sample_user_to_register["username"]
    response = client.post("/user/register", json=sample_user_to_register)
    assert response.status_code == 201
    test_db.flush()
    user_to_register_in_db = test_db.query(Users).filter(Users.username == sample_user_username).first()
    assert user_to_register_in_db.id is not None
    assert user_to_register_in_db.email == sample_user.email
    assert user_to_register_in_db.first_name == sample_user.first_name
    assert user_to_register_in_db.last_name == sample_user.last_name
    assert user_to_register_in_db.hashed_password != sample_user.password
    assert user_to_register_in_db.is_enabled == True


def test_get_current_user_info(add_test_data):
    response = client.get("/user/info")
    assert response.status_code == 200
    response_json = response.json()
    test_user_username = add_test_data["test_user_username"]
    assert response_json["username"] == test_user_username
    assert response_json["first_name"] == "Test"
    assert response_json["last_name"] == "User"
    assert response_json["email"] == f"{test_user_username}@pytest.org"
    assert response_json["is_enabled"] == True