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


def test_search_todo():
    def test_todo_item_exist(response):
        test_todo_item_without_public_uuid_field = {
            "title": "Pytest Auto Test Item",
            "description": "Test if the app can get this test todo item",
            "priority": 1,
            "is_completed": False
        }
        assert response.status_code == 200
        response_json = response.json()
        assert any(
            {k: item[k] for k in test_todo_item_without_public_uuid_field} == test_todo_item_without_public_uuid_field
            for item in response_json)

    title_search_parameter = "Pytest Auto Test Item"
    description_search_parameter = "Test if the app can get this test todo item"
    priority_search_parameter = 1
    is_completed_search_parameter = False

    # ========== 1. Single parameter (4 cases) ==========
    test_todo_item_exist(client.get("/todos/search", params={"title": title_search_parameter}))
    test_todo_item_exist(client.get("/todos/search", params={"description": description_search_parameter}))
    test_todo_item_exist(client.get("/todos/search", params={"priority": priority_search_parameter}))
    test_todo_item_exist(client.get("/todos/search", params={"is_completed": is_completed_search_parameter}))
    # ========== 2. Two‑parameter combinations (6 cases) ==========
    test_todo_item_exist(client.get("/todos/search", params={
        "title": title_search_parameter,
        "description": description_search_parameter
    }))
    test_todo_item_exist(client.get("/todos/search", params={
        "title": title_search_parameter,
        "priority": priority_search_parameter
    }))
    test_todo_item_exist(client.get("/todos/search", params={
        "title": title_search_parameter,
        "is_completed": is_completed_search_parameter
    }))
    test_todo_item_exist(client.get("/todos/search", params={
        "description": description_search_parameter,
        "priority": priority_search_parameter
    }))
    test_todo_item_exist(client.get("/todos/search", params={
        "description": description_search_parameter,
        "is_completed": is_completed_search_parameter
    }))
    test_todo_item_exist(client.get("/todos/search", params={
        "priority": priority_search_parameter,
        "is_completed": is_completed_search_parameter
    }))
    # ========== 3. Three‑parameter combinations (4 cases) ==========
    test_todo_item_exist(client.get("/todos/search", params={
        "title": title_search_parameter,
        "description": description_search_parameter,
        "priority": priority_search_parameter
    }))
    test_todo_item_exist(client.get("/todos/search", params={
        "title": title_search_parameter,
        "description": description_search_parameter,
        "is_completed": is_completed_search_parameter
    }))
    test_todo_item_exist(client.get("/todos/search", params={
        "title": title_search_parameter,
        "priority": priority_search_parameter,
        "is_completed": is_completed_search_parameter
    }))
    test_todo_item_exist(client.get("/todos/search", params={
        "description": description_search_parameter,
        "priority": priority_search_parameter,
        "is_completed": is_completed_search_parameter
    }))
    # ========== 4. All four parameters combined (1 case) ==========
    test_todo_item_exist(client.get("/todos/search", params={
        "title": title_search_parameter,
        "description": description_search_parameter,
        "priority": priority_search_parameter,
        "is_completed": is_completed_search_parameter
    }))