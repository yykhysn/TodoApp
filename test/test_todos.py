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