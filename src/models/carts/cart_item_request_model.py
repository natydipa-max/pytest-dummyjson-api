from pydantic import BaseModel
# Items to create a cart

class CartItemRequestModel(BaseModel):
    id: int
    quantity: int
    