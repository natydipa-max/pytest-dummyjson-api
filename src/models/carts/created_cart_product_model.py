from pydantic import BaseModel
#product obtains after create it

class CreatedCartProductModel(BaseModel):
    id: int
    title: str
    price: float
    quantity: int
    total: float
    discountedPrice: float
    discountPercentage: float
    thumbnail: str
