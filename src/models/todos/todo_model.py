from pydantic import BaseModel


class TodoModel(BaseModel):
    id: int
    todo: str
    completed: bool
    userId: int