# PUT
from src.models.product_request_model import ProductRequestModel
from src.models.product_model import ProductModel


def test_update_product(products_client):
    product = ProductRequestModel(
        title="Updated Product",
        price=49.99,
        description="Updated Description",
        category="electronics",
    )

    response = products_client.update_product(1, product)

    assert response.status_code == 200

    updated = ProductModel.model_validate(response.json())

    assert updated.id == 1
    assert updated.title == product.title
    assert updated.price == product.price
    assert updated.description == product.description