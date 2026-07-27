from pydantic import BaseModel

from src.models.posts.post_model import PostModel


class PostsResponseModel(BaseModel):
    posts: list[PostModel]
    total: int
    skip: int
    limit: int