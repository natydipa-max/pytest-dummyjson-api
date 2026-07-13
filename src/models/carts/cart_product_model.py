from pydantic import BaseModel


class CartProductModel(BaseModel):
    id: int
    title: str
    price: float
    quantity: int
    total: float
    discountPercentage: float
    discountedPrice: float
    thumbnail: str