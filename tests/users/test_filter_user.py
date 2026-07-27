# POST
import pytest
from src.models.users.users_response_model import UsersResponseModel

@pytest.mark.smoke
def test_filter_users_by_valid_field(users_client):
    response = users_client.filter_users(
        key="hair.color",
        value="Brown"
    )

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.total > 0
    assert len(users.users) == users.total

    assert all(
        user.hair["color"] == "Brown"
        for user in users.users
    )

@pytest.mark.parametrize(
    "key,value",
    [
        ("firstName", "Emily"),
        ("age", "29"),
    ],
)
def test_filter_users_by_supported_fields(users_client, key, value):
    response = users_client.filter_users(
        key=key,
        value=value
    )

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.total > 0

@pytest.mark.boundary
@pytest.mark.parametrize(
    "key,value",
    [
        ("hair.color", None),
        (None, "Brown"),
    ],
)
def test_filter_users_with_missing_parameters_returns_empty(
        users_client,
        key,
        value,
    ):
    response = users_client.filter_users(
        key=key,
        value=value
    )

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.total == 0
    assert users.users == []

@pytest.mark.boundary
def test_filter_users_with_unknown_field_returns_empty(users_client):
    response = users_client.filter_users(
        key="unknownField",
        value="test"
    )

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.total == 0
    assert users.users == []