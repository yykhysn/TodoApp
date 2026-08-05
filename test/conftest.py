import pytest

from database import SessionLocal, get_db
from main import app


@pytest.fixture
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(autouse=True)
def override_dependency(test_db):
    def _override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()