from pydantic import BaseModel

from src.models.carts.cart_item_request_model import CartItemRequestModel


class CreateCartRequestModel(BaseModel):
    userId: int
    products: list[CartItemRequestModel]