import pytest

from src.models.carts.carts_response_model import CartsResponseModel


@pytest.mark.smoke
def test_get_user_carts(users_client):
    response = users_client.get_user_carts(1)

    assert response.status_code == 200

    carts = CartsResponseModel.model_validate(response.json())

    assert carts.total > 0
    assert len(carts.carts) == carts.total

    assert all(cart.userId == 1 for cart in carts.carts)

@pytest.mark.negative
def test_get_user_carts_invalid_user_id(users_client):
    response = users_client.get_user_carts(999999)

    assert response.status_code == 404

    assert response.json() == {
        "message": "User with id '999999' not found"
    }