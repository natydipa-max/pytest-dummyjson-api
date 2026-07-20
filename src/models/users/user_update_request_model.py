from pydantic import BaseModel

class UserUpdateRequestModel(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    age: int | None = None