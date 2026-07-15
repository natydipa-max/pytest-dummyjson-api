# Negative tests
from src.models.error_response_model import ErrorResponseModel
from src.client.cart_client import CartClient
import pytest

@pytest.mark.negative
@pytest.mark.parametrize(
    "cart_id, expected_status",
    [
        ("abc", 404),
        (0, 404),
        (-1, 404),
        (999999, 404),
    ],
)
def test_get_cart_with_invalid_id(carts_client, cart_id, expected_status):
    response = carts_client.get_cart(cart_id)

    assert response.status_code == expected_status

    error = ErrorResponseModel.model_validate(
        response.json()
    )

@pytest.mark.negative
@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        ("abc", 400),
        (-1, 404),
        (999999, 404),
    ],
)
def test_get_cart_with_invalid_user(carts_client, user_id, expected_status):
    response = carts_client.get_cart_by_user(user_id)

    assert response.status_code == expected_status

    error = ErrorResponseModel.model_validate(
        response.json()
    )
