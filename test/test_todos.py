import pytest
from fastapi.testclient import TestClient

from main import app
from data_constraints.input_schema import ToDosInputSchema


client = TestClient(app)


@pytest.fixture
def sample_todo():
    return ToDosInputSchema(
        title="PytestTestTodoTitle",
        description="PytestTestTodoDescription",
        priority=2,
        is_completed=False
    )

def test_getAll_todos():
    response = client.get("/todos/getAll")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json[0]["title"] == "Pytest Auto Test Item"
    assert response_json[0]["description"] == "Test if the app can get this test todo item"
    assert response_json[0]["priority"] == 1
    assert response_json[0]["is_completed"] is False
    assert response_json[0]["public_uuid"] is not None