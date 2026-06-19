from pydantic import BaseModel


class LoginResponseModel(BaseModel):
    accessToken: str
    refreshToken: str
    id: int
    username: str
    email: str