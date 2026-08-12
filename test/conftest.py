import uuid

import pytest

from database import SessionLocal, get_db, Users
from main import app
from data_constraints.input_schema import UsersRegisterSchema
from router.user import validate_user_credential, crypt_context


@pytest.fixture
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(autouse=True)
def override_db_dependency(test_db):
    def _override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(autouse=True, scope="session")
def add_test_data():
    test_user_name = str(uuid.uuid4().hex)
    test_user_password = str(uuid.uuid4())
    test_user = UsersRegisterSchema(
        email=f"{test_user_name}@pytest.org",
        first_name="Test",
        last_name="User",
        password=test_user_password,
        username= test_user_name
    ).model_dump()
    test_user["hashed_password"] = crypt_context.hash(test_user.pop("password"))
    test_user = Users(**test_user)
    db = SessionLocal()
    db.add(test_user)
    db.commit()
    def _override_user_dependency():
        return test_user.username

    app.dependency_overrides[validate_user_credential] = _override_user_dependency
    yield
    db.delete(test_user)
    db.commit()
    db.close()