from src.constants import INVALID_CREDENTIALS_MESSAGE, REQUIRED_CREDENTIALS_MESSAGE
from src.models.login_response_model import LoginResponseModel
from src.models.error_response_model import ErrorResponseModel
from src.config import AUTH_USERNAME, AUTH_PASSWORD


def test_login_with_valid_credentials(auth_client):
    response = auth_client.login(
        AUTH_USERNAME,
        AUTH_PASSWORD
    )

    assert response.status_code == 200

    login_response = LoginResponseModel.model_validate(
        response.json()
    )

    assert login_response.accessToken is not None
    assert len(login_response.accessToken) > 0
    assert login_response.username == AUTH_USERNAME


def test_login_with_invalid_username(auth_client):
    response = auth_client.login(
        username="invalid_user",
        password="password"
    )

    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == INVALID_CREDENTIALS_MESSAGE


def test_login_with_invalid_password(auth_client):
    response = auth_client.login(
        username=AUTH_USERNAME,
        password="wrong_password"
    )

    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == INVALID_CREDENTIALS_MESSAGE


def test_login_with_empty_credentials(auth_client):
    response = auth_client.login(
        username="",
        password=""
    )

    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == REQUIRED_CREDENTIALS_MESSAGE