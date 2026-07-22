import pytest
from src.models.users.user_model import UserModel
from src.models.users.users_response_model import UsersResponseModel


@pytest.mark.smoke
def test_get_user_by_id(users_client):
    response = users_client.get_user(1)

    assert response.status_code == 200

    user = UserModel.model_validate(
        response.json()
    )

    assert user.id == 1


@pytest.mark.smoke
def test_get_all_users(users_client):
    response = users_client.get_all_users()

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert all(user.id > 0 for user in users.users)
    assert users.total >= len(users.users)
    assert users.limit == 30
    assert len(users.users) == users.limit


@pytest.mark.parametrize(
    "limit, skip, expected_first_id",
    [
        (5, 10, 11),
        (10, 20, 21),
    ],
)
def test_get_users_pagination(users_client, limit, skip, expected_first_id):
    response = users_client.get_all_users(limit=limit, skip=skip)

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.limit == limit
    assert users.skip == skip
    assert len(users.users) == limit
    assert users.users[0].id == expected_first_id

@pytest.mark.boundary
def test_get_users_limit_zero_returns_all(users_client):
    response = users_client.get_all_users(limit=0)

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.limit == users.total
    assert len(users.users) == users.total

@pytest.mark.boundary
def test_get_users_large_limit_returns_all(users_client):
    response = users_client.get_all_users(limit=9999)

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.limit == users.total
    assert len(users.users) == users.total

@pytest.mark.boundary
def test_get_users_skip_out_of_range(users_client):
    response = users_client.get_all_users(skip=9999)

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.skip == 9999
    assert users.limit == 0
    assert users.users == []