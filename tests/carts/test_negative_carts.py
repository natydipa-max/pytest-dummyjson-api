# Negative tests
from src.models.error_response_model import ErrorResponseModel
from src.client.cart_client import CartClient
import pytest
import requests

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

@pytest.mark.negative
def test_add_cart_malformed_json():
    response = requests.post(
        "https://dummyjson.com/carts/add",
        headers={"Content-Type": "application/json"},
        data='{"userId":1,"products":[{"id":1,"quantity":2]'
    )

    assert response.status_code == 400

    body = response.json()

    assert "Expected ',' or '}'" in body["message"]

@pytest.mark.negative
def test_add_cart_empty_products(carts_client):
    payload = {
        "userId": 1,
        "products": []
    }

    response = carts_client.add_cart(payload)

    assert response.status_code == 400

    body = response.json()

    assert body["message"] == "products can not be empty"

@pytest.mark.negative
def test_add_cart_missing_user_id(carts_client):
    payload = {
        "products": [
            {
                "id": 1,
                "quantity": 1
            }
        ]
    }

    response = carts_client.add_cart(payload)

    assert response.status_code == 400

    body = response.json()

    assert body["message"] == "User id is required"

@pytest.mark.negative
def test_add_cart_non_existing_user(carts_client):
    payload = {
        "userId": 999999,
        "products": [
            {
                "id": 1,
                "quantity": 1
            }
        ]
    }

    response = carts_client.add_cart(payload)

    assert response.status_code == 404

    body = response.json()

    assert body["message"] == "User with id '999999' not found"
