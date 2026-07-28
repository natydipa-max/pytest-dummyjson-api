# PUT
import pytest
from src.models.users.user_model import UserModel
from src.models.users.user_update_request_model import UserUpdateRequestModel

@pytest.mark.smoke
def test_update_user(users_client):
    original = users_client.get_user(1)
    original_user = UserModel.model_validate(original.json())

    response = users_client.update_user(
        1,
        UserUpdateRequestModel(lastName="Updated")
    )

    updated = UserModel.model_validate(response.json())

    assert updated.lastName == "Updated"

    assert updated.firstName == original_user.firstName
    assert updated.age == original_user.age
    assert updated.email == original_user.email


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

