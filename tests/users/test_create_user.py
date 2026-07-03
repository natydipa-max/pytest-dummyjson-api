# POST
import pytest

from src.models.users.user_request_model import UserRequestModel
from src.models.users.user_create_response_model import UserCreateResponseModel


@pytest.mark.smoke
def test_create_user(users_client):
    user = UserRequestModel(
        firstName="Natalia",
        lastName="Di Paolo",
        age=47,
    )

    response = users_client.create_user(user)

    assert response.status_code == 201

    created = UserCreateResponseModel.model_validate(response.json())

    assert created.firstName == user.firstName
    assert created.lastName == user.lastName
    assert created.age == user.age