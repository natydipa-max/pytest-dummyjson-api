from pydantic import BaseModel

from src.models.carts.created_cart_product_model import CreatedCartProductModel
#Response with a product list after create a cart

class CreatedCartModel(BaseModel):
    id: int
    products: list[CreatedCartProductModel]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int
