from pydantic import BaseModel


class UserCreateResponseModel(BaseModel):
    id: int
    firstName: str
    lastName: str
    age: int