from pydantic import BaseModel
from src.models.carts.cart_model import CartModel


class CartsResponseModel(BaseModel):
    carts: list[CartModel]
    total: int
    skip: int
    limit: int