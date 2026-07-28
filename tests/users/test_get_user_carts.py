import pytest

from src.models.carts.carts_response_model import CartsResponseModel
from src.models.error_response_model import ErrorResponseModel
from src.constants import INVALID_USER_ID_MESSAGE, USER_NOT_FOUND_MESSAGE


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

    # assert response.json() == {
    #     "message": "User with id '999999' not found"
    # }
    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == USER_NOT_FOUND_MESSAGE.format("999999")



@pytest.mark.negative
def test_get_user_carts_with_invalid_user_id_returns_bad_request(users_client):
    response = users_client.get_user_carts("abc")

    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == INVALID_USER_ID_MESSAGE.format("abc")