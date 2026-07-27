import pytest
from src.models.users.users_response_model import UsersResponseModel


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