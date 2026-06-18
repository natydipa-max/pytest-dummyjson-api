# DELETE
from src.models.product_delete_response_model import ProductDeleteResponseModel


def test_delete_product(products_client):
    response = products_client.delete_product(1)

    assert response.status_code == 200

    deleted = ProductDeleteResponseModel.model_validate(response.json())

    assert deleted.id == 1
    assert deleted.isDeleted is True