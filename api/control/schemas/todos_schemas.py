from pydantic import BaseModel

from api.control.models.models import TodoState

class TodoSchema(BaseModel):
  title: str
  description: str
  state: TodoState

class TodoPublic(TodoSchema):
  id: str

class TodoList(BaseModel):
  todos: list[TodoPublic]

class TodoUpdate(BaseModel):
  title: str | None = None
  description: str | None = None
  state: TodoState | None = None