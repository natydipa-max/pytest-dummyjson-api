import pytest

from src.client.auth_client import AuthClient
from src.client.product_client import ProductClient
from src.client.user_client import UserClient
from src.config import AUTH_USERNAME, AUTH_PASSWORD


@pytest.fixture(scope="session")
def products_client():
    return ProductClient()

@pytest.fixture(scope="session")
def auth_client():
    return AuthClient()


@pytest.fixture(scope="session")
def auth_token(auth_client):
    response = auth_client.login(AUTH_USERNAME, AUTH_PASSWORD)
    return response.json()["accessToken"]


@pytest.fixture(scope="session")
def users_client():
    return UserClient()