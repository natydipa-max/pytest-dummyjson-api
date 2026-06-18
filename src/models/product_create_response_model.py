from pydantic import BaseModel


class ProductCreateResponseModel(BaseModel):
    id: int
    title: str
    price: float
    description: str
    category: str