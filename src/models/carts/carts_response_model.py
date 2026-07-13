from pydantic import BaseModel
from src.models.carts.cart_product_model import CartProductModel


class CartsResponseModel(BaseModel):
    carts: list[CartProductModel]
    total: int
    skip: int
    limit: int