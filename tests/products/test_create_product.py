# POST
from src.models.product_request_model import ProductRequestModel
from src.models.product_create_response_model import ProductCreateResponseModel


def test_create_product(products_client):
    product = ProductRequestModel(
        title="Test Product",
        price=10.99,
        description="Test Description",
        category="electronics",
    )

    response = products_client.create_product(product)

    assert response.status_code == 201

    created = ProductCreateResponseModel.model_validate(response.json())

    assert created.title == product.title
    assert created.price == product.price
    assert created.description == product.description
    assert created.category == product.category