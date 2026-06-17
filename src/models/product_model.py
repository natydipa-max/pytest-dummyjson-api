from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    rating: float
    stock: int
    brand: str | None = None
    thumbnail: str