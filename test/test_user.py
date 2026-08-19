import uuid

import pytest
from fastapi.testclient import TestClient

from database import Users
from main import app
from data_constraints.input_schema import UsersRegisterSchema, UsersUpdateSchema
from router.user import crypt_context


client = TestClient(app)

@pytest.fixture
def sample_user():
    _username = str(uuid.uuid4().hex)
    _password = str(uuid.uuid4().hex)
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


def test_update_user(add_test_data, test_db):
    user_name = add_test_data["test_user_username"]
    old_password = add_test_data["test_user_password"]
    new_password = str(uuid.uuid4().hex)
    def _update_user_retrieve_in_db():
        test_db.flush()
        return test_db.query(Users).filter(Users.username == user_name).first()

    # Test update password with a wrong old password:
    response = client.put("/user/update", json=UsersUpdateSchema(old_password=str(uuid.uuid4().hex),
                                                                 new_password=new_password).model_dump(exclude_unset=True))
    assert response.status_code == 401, "Test Update Password with Wrong Old Password Fail"
    assert response.json() == {"detail": "Incorrect old password"}, "Test Update Password with Wrong Old Password Fail"
    # Test update password with the right old password:
    response = client.put("/user/update", json=UsersUpdateSchema(old_password=old_password,
                                                                 new_password=new_password).model_dump(exclude_unset=True))
    assert response.status_code == 204, "Test Update Password with Right Old Password Fail"
    user_to_update_in_db = _update_user_retrieve_in_db()
    assert crypt_context.verify(old_password, user_to_update_in_db.hashed_password) == False
    assert user_to_update_in_db.hashed_password != new_password
    assert crypt_context.verify(new_password, user_to_update_in_db.hashed_password)
    # Test update email:
    response = client.put("/user/update", json=UsersUpdateSchema(email=f"{user_name}@change_email.user").
                          model_dump(exclude_unset=True))
    assert response.status_code == 204, "Test Change User Email Fail"
    user_to_update_in_db = _update_user_retrieve_in_db()
    assert user_to_update_in_db.email == f"{user_name}@change_email.user"
    # Test update first_name:
    response = client.put("/user/update", json=UsersUpdateSchema(first_name="new_first_name").model_dump(exclude_unset=True))
    assert response.status_code == 204, "Test Change User First_Name Fail"
    user_to_update_in_db = _update_user_retrieve_in_db()
    assert user_to_update_in_db.first_name == "new_first_name"
    # Test update last_name:
    response = client.put("/user/update", json=UsersUpdateSchema(last_name="new_last_name").model_dump(exclude_unset=True))
    assert response.status_code == 204, "Test Change User Last_Name Fail"
    user_to_update_in_db = _update_user_retrieve_in_db()
    assert user_to_update_in_db.last_name == "new_last_name"
    # Test update is_enabled:
    response = client.put("/user/update",json=UsersUpdateSchema(is_enabled=False).model_dump(exclude_unset=True))
    assert response.status_code == 204, "Test Change User is_enabled Fail"
    user_to_update_in_db = _update_user_retrieve_in_db()
    assert user_to_update_in_db.is_enabled == False