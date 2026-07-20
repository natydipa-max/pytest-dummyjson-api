# PUT
import pytest
from src.models.users.user_model import UserModel
from src.models.users.user_update_request_model import UserUpdateRequestModel

@pytest.mark.smoke
def test_update_user(users_client):
    payload = UserUpdateRequestModel(
        lastName="Updated"
    )

    response = users_client.update_user(1, payload)
    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

    user = UserModel(**response.json())

    assert user.id == 1
    assert user.lastName == "Updated"


def test_update_multiple_user_fields(users_client):
    payload = UserUpdateRequestModel(
        firstName="Natalia",
        lastName="Updated",
        age=35,
    )

    response = users_client.update_user(1, payload)

    assert response.status_code == 200

    user = UserModel(**response.json())

    assert user.firstName == "Natalia"
    assert user.lastName == "Updated"
    assert user.age == 35

