
from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, Depends
from bll.schemas.authschema import AuthClaimsSchema
from bll.schemas.common import PaginationParams
from bll.schemas.usertodo import CreateTodoSchema, TodoSchema, UpdateTodoSchema
from bll.services.usertodo import UserTodoService
from rest.utils.auth import get_active_user
from rest.utils.container import DIContainer

usertodo_router = APIRouter(prefix="/todo")

@usertodo_router.post('/', response_model=TodoSchema)
def create_todo(todo_dto: CreateTodoSchema, claims: Annotated[AuthClaimsSchema, Depends(get_active_user)], todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))) -> TodoSchema:
    return todo_service.create(todo_dto, claims)

@usertodo_router.get('/', response_model=List[TodoSchema])
def get_todos(claims: Annotated[AuthClaimsSchema, Depends(get_active_user)], pagination: PaginationParams = Depends(), todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))) -> List[TodoSchema]:
    return todo_service.get(pagination, claims)

@usertodo_router.put('/:id', response_model=TodoSchema)
def update_todo(id: UUID, todo_dto: UpdateTodoSchema, claims: Annotated[AuthClaimsSchema, Depends(get_active_user)], todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))) -> TodoSchema:
    return todo_service.update(id, todo_dto, claims)

@usertodo_router.delete('/:id', status_code=204)
def delete_todo(id: UUID, claims: Annotated[AuthClaimsSchema, Depends(get_active_user)], todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))) -> None:
    todo_service.delete(id, claims)

@usertodo_router.get('/:id', response_model=TodoSchema)
def get_todo(id: UUID, claims: Annotated[AuthClaimsSchema, Depends(get_active_user)], todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))) -> TodoSchema:
    return todo_service.get_by_id(id, claims)