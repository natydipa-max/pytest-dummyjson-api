from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    firstName: str
    lastName: str
    username: str
    email: str

    model_config = {"extra": "allow"}