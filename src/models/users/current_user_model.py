from pydantic import BaseModel


class CurrentUserModel(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str

    model_config = {"extra": "allow"}