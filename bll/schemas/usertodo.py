from typing import Optional
from pydantic import BaseModel

class UpdateTodoSchema(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None

class TodoSchema(UpdateTodoSchema):
    id: str

class CreateTodoSchema(UpdateTodoSchema):
    pass