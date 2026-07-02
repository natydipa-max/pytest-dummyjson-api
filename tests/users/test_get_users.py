import pytest
from src.models.user_model import UserModel
from src.models.users_response_model import UsersResponseModel


@pytest.mark.smoke
def test_get_user_by_id(users_client    ):
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


