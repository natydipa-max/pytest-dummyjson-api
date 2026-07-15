# GET
import pytest
from src.models.carts.cart_model import CartModel
from src.models.carts.carts_response_model import CartsResponseModel


@pytest.mark.smoke
def test_get_cart_by_id(carts_client):
    response = carts_client.get_cart(1)

    assert response.status_code == 200

    cart = CartModel.model_validate(response.json())

    assert cart.id == 1


@pytest.mark.smoke
def test_get_all_carts(carts_client):
    response = carts_client.get_all_carts()

    assert response.status_code == 200

    carts = CartsResponseModel.model_validate(response.json())

    assert all(cart.id > 0 for cart in carts.carts)
    assert carts.total == 208
    assert carts.limit == 30

@pytest.mark.smoke
def test_get_cart_by_user(carts_client):
    response = carts_client.get_cart_by_user(1)

    assert response.status_code == 200

    result = CartsResponseModel.model_validate(response.json())

    assert len(result.carts) > 0
    assert all(cart.userId == 1 for cart in result.carts)