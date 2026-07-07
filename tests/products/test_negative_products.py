# Negative tests
from src.models.error_response_model import ErrorResponseModel
from src.models.products.product_request_model import ProductRequestModel
import pytest

@pytest.mark.negative
@pytest.mark.parametrize(
    "product_id, expected_status",
    [
        ("abc", 404),
        (0, 404),
        (-1, 404),
        (999999, 404),
    ],
)
def test_get_product_with_invalid_id(products_client, product_id, expected_status):
    response = products_client.get_product(product_id)

    assert response.status_code == expected_status

    error = ErrorResponseModel.model_validate(
        response.json()
    )

    assert str(product_id) in error.message

@pytest.mark.negative
def test_create_product_with_malformed_json_returns_400(products_client):
    raw_payload = '{"title":}'  # intentionally invalid JSON

    response = products_client.post_raw_json(
        "/products/add",
        raw_payload
    )

    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(
        response.json()
    )

    assert "Unexpected token" in error.message

@pytest.mark.negative
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


@pytest.mark.negative
def test_delete_product_with_nonexistent_id_returns_404(products_client):
    response = products_client.delete_product(99999)

    assert response.status_code == 404

    error = ErrorResponseModel.model_validate(response.json())

    assert "99999" in error.message