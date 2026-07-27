from pydantic import BaseModel

from src.models.todos.todo_model import TodoModel


class TodosResponseModel(BaseModel):
    todos: list[TodoModel]
    total: int
    skip: int
    limit: int