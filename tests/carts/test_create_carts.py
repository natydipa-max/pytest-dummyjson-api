#POST
import pytest
from src.models.carts.cart_item_request_model import CartItemRequestModel
from src.models.carts.create_cart_request_model import CreateCartRequestModel
from src.models.carts.created_cart_model import CreatedCartModel

@pytest.mark.smoke
@pytest.mark.parametrize(
    "new_cart_request",
    [
        CreateCartRequestModel(
            userId=1,
            products=[
                CartItemRequestModel(id=1, quantity=2),
                CartItemRequestModel(id=50, quantity=1),
            ],
        ),
        CreateCartRequestModel(
            userId=1,
            products=[
                CartItemRequestModel(id=1, quantity=1),
            ],
        ),
    ],
)

def test_add_cart_success(carts_client, new_cart_request):
    response = carts_client.add_cart(new_cart_request)

    assert response.status_code == 201

    created = CreatedCartModel.model_validate(response.json())

    assert created.userId == new_cart_request.userId
    assert created.totalProducts == len(new_cart_request.products)
    assert created.totalQuantity == sum(
        item.quantity for item in new_cart_request.products
    )

    assert len(created.products) == len(new_cart_request.products)

    assert created.id > 0
    assert created.total > 0
    assert created.discountedTotal > 0
    assert created.discountedTotal <= created.total

    returned_ids = [item.id for item in created.products]
    expected_ids = [item.id for item in new_cart_request.products]

    assert returned_ids == expected_ids

# API behavior: invalid product IDs are ignored when creating a cart
def test_add_cart_invalid_product_id(carts_client):
    payload = {
        "userId": 1,
        "products": [
            {
                "id": 999999,
                "quantity": 1
            }
        ]
    }

    response = carts_client.add_cart(payload)

    assert response.status_code == 201

    created = CreatedCartModel.model_validate(response.json())

    assert created.products == []
    assert created.totalProducts == 0
    assert created.totalQuantity == 0
    assert created.total == 0
    assert created.discountedTotal == 0
