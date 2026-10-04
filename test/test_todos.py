import time
from random import randint

import pytest
from fastapi.testclient import TestClient

from main import app
from data_constraints.input_schema import ToDosCreateSchema
from database import ToDoListTable
from utils import sql_result_to_dict


client = TestClient(app)


@pytest.fixture
def sample_todo():
    return ToDosCreateSchema(
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
    response = client.get("/api/todos/getAll")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json[0]["title"] == "Pytest Auto Test Item"
    assert response_json[0]["description"] == "Test if the app can get this test todo item"
    assert response_json[0]["priority"] == 1
    assert response_json[0]["is_completed"] is False
    assert response_json[0]["public_uuid"] is not None



def test_create_todo(sample_todo, test_db):
    assert is_sample_todo_in_db(test_db) is False
    response = client.post("/api/todos/create", json=sample_todo.model_dump())
    assert response.status_code == 201
    assert response.json() == {"detail": "PytestTestTodoTitle's Todo created successfully"}
    assert is_sample_todo_in_db(test_db) is True



def test_search_todo():
    def test_todo_item_exist(todo_search_params):
        test_todo_item_without_public_uuid_field = {
            "title": "Pytest Auto Test Item",
            "description": "Test if the app can get this test todo item",
            "priority": 1,
            "is_completed": False
        }
        response = client.get("/api/todos/search", params=todo_search_params)
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
    test_todo_item_exist({"title": title_search_parameter})
    test_todo_item_exist({"description": description_search_parameter})
    test_todo_item_exist({"priority": priority_search_parameter})
    test_todo_item_exist({"is_completed": is_completed_search_parameter})
    # ========== 2. Two‑parameter combinations (6 cases) ==========
    test_todo_item_exist({"title": title_search_parameter, "description": description_search_parameter})
    test_todo_item_exist({"title": title_search_parameter, "priority": priority_search_parameter})
    test_todo_item_exist({"title": title_search_parameter, "is_completed": is_completed_search_parameter})
    test_todo_item_exist({"description": description_search_parameter, "priority": priority_search_parameter})
    test_todo_item_exist({"description": description_search_parameter, "is_completed": is_completed_search_parameter})
    test_todo_item_exist({"priority": priority_search_parameter, "is_completed": is_completed_search_parameter})
    # ========== 3. Three‑parameter combinations (4 cases) ==========
    test_todo_item_exist({"title": title_search_parameter, "description": description_search_parameter, "priority": priority_search_parameter})
    test_todo_item_exist({"title": title_search_parameter, "description": description_search_parameter, "is_completed": is_completed_search_parameter})
    test_todo_item_exist({"title": title_search_parameter, "priority": priority_search_parameter, "is_completed": is_completed_search_parameter})
    test_todo_item_exist({"description": description_search_parameter, "priority": priority_search_parameter, "is_completed": is_completed_search_parameter})
    # ========== 4. All four parameters combined (1 case) ==========
    test_todo_item_exist({"title": title_search_parameter, "description": description_search_parameter,
                          "priority": priority_search_parameter, "is_completed": is_completed_search_parameter})



def test_update_todo(add_test_data, test_db):
    updated_todo_data =  {
            "title": "Todo Test Item Title Updated",
            "description": "Todo Test Item Description Updated",
            "priority": randint(1, 5),
            "is_completed": True
        }

    assert sql_result_to_dict(test_db.query(ToDoListTable.title, ToDoListTable.description, ToDoListTable.priority, ToDoListTable.is_completed)
            .filter(ToDoListTable.public_uuid == add_test_data["test_todo_public_uuid"]).first()) == {
                "title": "Pytest Auto Test Item",
                "description": "Test if the app can get this test todo item",
                "priority": 1,
                "is_completed": False
            }

    response = client.put("/api/todos/update", params={"todo_public_uuid": add_test_data["test_todo_public_uuid"]},
                          json=updated_todo_data)
    assert response.status_code == 200
    assert response.json() == {
        "code": 0,
        "message": "Todo updated successfully",
        "data": {
            "before": {
                "title": "Pytest Auto Test Item",
                "description": "Test if the app can get this test todo item",
                "priority": 1,
                "is_completed": False
            },
            "after": updated_todo_data
        },
        "timestamp": int(time.time())
    }

    assert sql_result_to_dict(test_db.query(ToDoListTable.title, ToDoListTable.description, ToDoListTable.priority,
                                            ToDoListTable.is_completed).filter
                              (ToDoListTable.public_uuid == add_test_data["test_todo_public_uuid"]).first()) == updated_todo_data



def test_delete_todo(add_test_data, test_db):
    assert test_db.query(ToDoListTable).filter(ToDoListTable.public_uuid == add_test_data["test_todo_public_uuid"]).first() is not None

    response = client.delete("/api/todos/deleteTodo", params={"todo_public_uuid": add_test_data["test_todo_public_uuid"]})
    assert response.status_code == 200
    assert response.json() == {
        "code": 0,
        "message": "Todo deleted successfully",
        "data": {
            "title": "Pytest Auto Test Item",
            "description": "Test if the app can get this test todo item",
            "priority": 1,
            "is_completed": False
        },
        "timestamp": int(time.time())
    }

    assert test_db.query(ToDoListTable).filter(ToDoListTable.public_uuid == add_test_data["test_todo_public_uuid"]).first() is None