from pydantic import BaseModel
from src.models.carts.cart_product_model import CartProductModel


class CartModel(BaseModel):
    id: int
    products: list[CartProductModel]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int