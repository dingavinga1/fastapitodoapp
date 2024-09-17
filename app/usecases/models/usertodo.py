from typing import Optional
from pydantic import BaseModel

class UpdateTodoRequestModel(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None

class TodoResponseModel(UpdateTodoRequestModel):
    id: str

class CreateTodoRequestModel(UpdateTodoRequestModel):
    pass