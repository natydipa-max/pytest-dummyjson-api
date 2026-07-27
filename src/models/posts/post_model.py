from pydantic import BaseModel


class ReactionsModel(BaseModel):
    likes: int
    dislikes: int


class PostModel(BaseModel):
    id: int
    title: str
    body: str
    tags: list[str]
    reactions: ReactionsModel
    views: int
    userId: int