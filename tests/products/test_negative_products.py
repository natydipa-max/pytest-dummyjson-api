# Negative tests
from src.models.error_response_model import ErrorResponseModel
from src.models.product_request_model import ProductRequestModel


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


def test_update_product_with_nonexistent_id_returns_404(products_client):
    product = ProductRequestModel(
        title="Test",
        price=9.99,
        description="Test",
        category="electronics",
    )

    response = products_client.update_product(99999, product)

    assert response.status_code == 404

    error = ErrorResponseModel.model_validate(response.json())

    assert "99999" in error.message


def test_delete_product_with_nonexistent_id_returns_404(products_client):
    response = products_client.delete_product(99999)

    assert response.status_code == 404

    error = ErrorResponseModel.model_validate(response.json())

    assert "99999" in error.message