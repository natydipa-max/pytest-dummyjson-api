import pytest

from src.models.todos.todos_response_model import TodosResponseModel


@pytest.mark.smoke
def test_get_user_todos(users_client):
    response = users_client.get_user_todos(1)

    assert response.status_code == 200

    todos = TodosResponseModel.model_validate(response.json())

    assert todos.total > 0
    assert len(todos.todos) == todos.total

    assert all(todo.userId == 1 for todo in todos.todos)

@pytest.mark.negative
def test_get_user_todos_invalid_user_id(users_client):
    response = users_client.get_user_todos(999999)

    assert response.status_code == 404

    assert response.json() == {
        "message": "User with id '999999' not found"
    }