from pydantic import BaseModel
from typing import Optional

class UpdateTodoRequestDto(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None

class TodoResponseDto(UpdateTodoRequestDto):
    id: str

class CreateTodoRequestDto(UpdateTodoRequestDto):
    pass