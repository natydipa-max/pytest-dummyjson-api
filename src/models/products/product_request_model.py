from pydantic import BaseModel


class ProductRequestModel(BaseModel):
    title: str
    description: str
    category: str
    price: float