from pydantic import BaseModel


class CartItemRequestModel(BaseModel):
    id: int
    quantity: int