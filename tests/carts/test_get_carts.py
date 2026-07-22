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

@pytest.mark.parametrize(
    "limit, skip, expected_first_id",
    [
        (10, 0, 1),
        (10, 10, 11),
    ],
)
def test_get_carts_pagination(carts_client, limit, skip, expected_first_id):
    response = carts_client.get_all_carts(limit=limit, skip=skip)

    assert response.status_code == 200

    carts = CartsResponseModel.model_validate(response.json())

    assert carts.limit == limit
    assert carts.skip == skip
    assert len(carts.carts) == limit
    assert carts.carts[0].id == expected_first_id

@pytest.mark.boundary
def test_get_carts_limit_zero_returns_all(carts_client):
    response = carts_client.get_all_carts(limit=0)

    assert response.status_code == 200

    carts = CartsResponseModel.model_validate(response.json())

    assert carts.limit == carts.total
    assert len(carts.carts) == carts.total

@pytest.mark.boundary
def test_get_carts_large_limit_returns_all(carts_client):
    response = carts_client.get_all_carts(limit=9999)

    assert response.status_code == 200

    carts = CartsResponseModel.model_validate(response.json())

    assert carts.limit == carts.total
    assert len(carts.carts) == carts.total

@pytest.mark.boundary
def test_get_carts_skip_out_of_range(carts_client):
    response = carts_client.get_all_carts(skip=9999)

    assert response.status_code == 200

    carts = CartsResponseModel.model_validate(response.json())

    assert carts.skip == 9999
    assert carts.limit == 0
    assert carts.carts == []