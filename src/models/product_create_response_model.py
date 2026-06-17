from pydantic import BaseModel


class ProductCreateResponseModel(BaseModel):
    id: int
    title: str