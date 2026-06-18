# Negative tests
from src.models.error_response_model import ErrorResponseModel


def test_get_product_with_nonexistent_id_returns_404(products_client):
    response = products_client.get_product(99999)

    assert response.status_code == 404

    error = ErrorResponseModel.model_validate(response.json())

    assert "99999" in error.message


def test_get_product_with_non_numeric_id_returns_404(products_client):
    response = products_client.get_product("abc")

    assert response.status_code == 404

    error = ErrorResponseModel.model_validate(response.json())

    assert "abc" in error.message


def test_delete_product_with_nonexistent_id_returns_404(products_client):
    response = products_client.delete_product(99999)

    assert response.status_code == 404

    error = ErrorResponseModel.model_validate(response.json())

    assert "99999" in error.message