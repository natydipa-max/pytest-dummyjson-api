from pydantic import BaseModel
from src.models.products.product_model import ProductModel


class CartModel(BaseModel):
    id: int
    products: list[ProductModel]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int