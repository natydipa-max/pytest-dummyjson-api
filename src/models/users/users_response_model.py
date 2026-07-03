from pydantic import BaseModel
from src.models.users.user_model import UserModel


class UsersResponseModel(BaseModel):
    users: list[UserModel]
    total: int
    skip: int
    limit: int