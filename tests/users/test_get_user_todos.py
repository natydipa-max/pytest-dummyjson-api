import pytest

from src.models.todos.todos_response_model import TodosResponseModel
from src.models.error_response_model import ErrorResponseModel
from src.constants import INVALID_USER_ID_MESSAGE, USER_NOT_FOUND_MESSAGE


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

    # assert response.json() == {
    #     "message": "User with id '999999' not found"
    # }
    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == USER_NOT_FOUND_MESSAGE.format("999999")

@pytest.mark.negative
def test_get_user_todos_with_invalid_user_id_returns_bad_request(users_client):
    response = users_client.get_user_todos("abc")

    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == INVALID_USER_ID_MESSAGE.format("abc")