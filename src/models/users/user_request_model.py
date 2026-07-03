from pydantic import BaseModel


class UserRequestModel(BaseModel):
    firstName: str
    lastName: str
    age: int