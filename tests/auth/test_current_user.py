from src.config import AUTH_USERNAME
from src.models.current_user_model import CurrentUserModel


def test_get_current_user(auth_client, auth_token):
    response = auth_client.get_current_user(auth_token)

    assert response.status_code == 200

    user = CurrentUserModel.model_validate(
        response.json()
    )

    assert user.username == AUTH_USERNAME


def test_get_current_user_with_invalid_token(auth_client):
    response = auth_client.get_current_user("invalid_token")

    assert response.status_code == 401

    assert response.json()["message"] == "Invalid/Expired Token!"