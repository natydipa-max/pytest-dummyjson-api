from datetime import datetime

from pydantic import BaseModel


class ProductDeleteResponseModel(BaseModel):
    id: int
    title: str
    isDeleted: bool
    deletedOn: datetime
