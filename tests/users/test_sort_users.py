import pytest
from src.models.users.users_response_model import UsersResponseModel
from src.models.error_response_model import ErrorResponseModel


@pytest.mark.parametrize(
    "sort_by",
    [
        "firstName",
        "age",
    ],
)
def test_get_users_sorted_ascending(users_client, sort_by):
    response = users_client.get_all_users(
        sortBy=sort_by,
        order="asc"
    )

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    values = [
        getattr(user, sort_by)
        for user in users.users
    ]

    assert values == sorted(values)

@pytest.mark.parametrize(
    "sort_by",
    [
        "firstName",
        "age",
    ],
)
def test_get_users_sorted_descending(users_client, sort_by):
    response = users_client.get_all_users(
        sortBy=sort_by,
        order="desc",
    )

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    values = [
        getattr(user, sort_by)
        for user in users.users
    ]

    assert values == sorted(values, reverse=True)

@pytest.mark.negative
def test_get_users_with_invalid_sort_field_returns_default_results(users_client):
    response = users_client.get_all_users(
        sortBy="unknown",
        order="asc"
    )

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.total > 0
    assert len(users.users) == users.limit

@pytest.mark.negative
def test_get_users_with_invalid_sort_order_returns_bad_request(users_client):
    response = users_client.get_all_users(
        sortBy="firstName",
        order="up"
    )

    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == (
        "Invalid 'order' - should be either 'asc' or 'desc'"
    )