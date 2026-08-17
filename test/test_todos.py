import pytest
from fastapi.testclient import TestClient

from main import app
from data_constraints.input_schema import ToDosInputSchema
from database import ToDoListTable


client = TestClient(app)


@pytest.fixture
def sample_todo():
    return ToDosInputSchema(
        title="PytestTestTodoTitle",
        description="PytestTestTodoDescription",
        priority=2,
        is_completed=False
    )

def is_sample_todo_in_db(db):
    sample_todo_in_db = db.query(ToDoListTable).filter(
        ToDoListTable.title == "PytestTestTodoTitle",
        ToDoListTable.description == "PytestTestTodoDescription",
        ToDoListTable.priority == 2,
        ToDoListTable.is_completed == False).first()
    return sample_todo_in_db is not None


def test_get_all_todos():
    response = client.get("/todos/getAll")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json[0]["title"] == "Pytest Auto Test Item"
    assert response_json[0]["description"] == "Test if the app can get this test todo item"
    assert response_json[0]["priority"] == 1
    assert response_json[0]["is_completed"] is False
    assert response_json[0]["public_uuid"] is not None

def test_create_todo(sample_todo, test_db):
    assert is_sample_todo_in_db(test_db) is False
    response = client.post("/todos/create", json=sample_todo.model_dump())
    assert response.status_code == 201
    assert response.json() == "Success! PytestTestTodoTitle's todo has been created!"
    test_db.flush()
    assert is_sample_todo_in_db(test_db) is True