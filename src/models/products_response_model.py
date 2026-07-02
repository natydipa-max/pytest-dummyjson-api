from pydantic import BaseModel
from typing import List
from src.models.product_model import ProductModel


class ProductsResponseModel(BaseModel):
    products: List[ProductModel]
    total: int
    skip: int
    limit: int