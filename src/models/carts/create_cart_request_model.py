from pydantic import BaseModel
from src.models.carts.cart_item_request_model import CartItemRequestModel
# body to create a cart with items

class CreateCartRequestModel(BaseModel):
    userId: int
    products: list[CartItemRequestModel]
