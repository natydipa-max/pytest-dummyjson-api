# GET
import pytest
from src.models.product_model import ProductModel


@pytest.mark.smoke
def test_get_product_by_id(products_client):
    response = products_client.get_product(1)

    assert response.status_code == 200

    product = ProductModel.model_validate(response.json())

    assert product.id == 1


@pytest.mark.smoke
def test_get_all_products(products_client):
    response = products_client.get_all_products()

    assert response.status_code == 200

    products = [
        ProductModel.model_validate(p)
        for p in response.json()["products"]
    ]

    assert all(product.id > 0 for product in products)