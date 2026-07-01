import pytest
from src.models.user_model import UserModel


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

    users = [
        UserModel.model_validate(p)
        for p in response.json()["users"]
    ]

    assert all(user.id > 0 for user in users)
    
    