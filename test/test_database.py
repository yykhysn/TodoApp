import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal, Base


@pytest.fixture
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def test_database_connection(test_db):
    assert test_db.execute(text("Select 1")).scalar() == 1, "App Can't Connect to Database"

def test_database_table_accessible(test_db):
    table_map = Base.metadata.tables
    for table_name in table_map.keys():
        try:
            test_db.execute(text(f"Select 1 from {table_name} limit 1"))
        except SQLAlchemyError as err:
            pytest.fail(f"Table {table_name} Invalid or Inaccessible: {err}")