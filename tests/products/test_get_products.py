# GET
from src.models.product_model import ProductModel


def test_get_product_by_id(products_client):
    response = products_client.get_product(1)

    assert response.status_code == 200

    product = ProductModel.model_validate(response.json())

    assert product.id == 1


def test_get_all_products(products_client):
    response = products_client.get_all_products()

    assert response.status_code == 200

    products = [
        ProductModel.model_validate(p)
        for p in response.json()["products"]
    ]

    assert len(products) > 0