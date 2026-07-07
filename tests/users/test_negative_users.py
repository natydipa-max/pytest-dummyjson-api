import pytest
from src.models.error_response_model import ErrorResponseModel

@pytest.mark.negative
@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        ("abc", 400),
        (0, 404),
        (-1, 404),
        (999999, 404),
    ],
)
def test_get_user_with_invalid_id(users_client, user_id, expected_status):
    response = users_client.get_user(user_id)

    assert response.status_code == expected_status

    error = ErrorResponseModel.model_validate(
        response.json()
    )

    assert str(user_id) in error.message

@pytest.mark.negative
def test_create_user_with_malformed_json_returns_400(users_client):
    raw_payload = '{"firstName":}' # intentionally invalid JSON

    response = users_client.post_raw_json(
        "/users/add",
        raw_payload
    )
    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(
        response.json()
    )

    assert "Unexpected token" in error.message