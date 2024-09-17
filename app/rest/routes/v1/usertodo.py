
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Request
from usecases.models.common import PaginationParams
from usecases.models.usertodo import CreateTodoRequestModel, TodoResponseModel, UpdateTodoRequestModel
from rest.dtos.usertodo import CreateTodoRequestDto, TodoResponseDto, UpdateTodoRequestDto
from usecases.services.usertodo import UserTodoService
from rest.middlewares.authcontext import get_active_user
from configs.container import DIContainer

usertodo_router = APIRouter(prefix="/todo", dependencies=[Depends(get_active_user)])

@usertodo_router.post('/', response_model=TodoResponseDto)
def create_todo(
    todo_dto: CreateTodoRequestDto,
    request: Request,
    todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))
) -> TodoResponseDto:
    todo_model: CreateTodoRequestModel = CreateTodoRequestModel(name=todo_dto.name, content=todo_dto.content)
    response: TodoResponseModel = todo_service.create(todo_model, request.state.auth_context)
    return TodoResponseDto(name=response.name, content=response.content, id=response.id)

@usertodo_router.get('/', response_model=List[TodoResponseDto])
def get_todos(
    request: Request,
    pagination: PaginationParams = Depends(),
    todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))
) -> List[TodoResponseDto]:
    response: List[TodoResponseModel] = todo_service.get(pagination, request.state.auth_context)
    return map(lambda x: TodoResponseDto(name=x.name, content=x.content, id=x.id), response)

@usertodo_router.put('/:id', response_model=TodoResponseDto)
def update_todo(
    id: UUID,
    todo_dto: UpdateTodoRequestDto,
    request: Request,
    todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))
) -> TodoResponseDto:
    todo_model: UpdateTodoRequestModel = UpdateTodoRequestModel(name=todo_dto.name, content=todo_dto.content)
    response: TodoResponseModel = todo_service.update(id, todo_model, request.state.auth_context)
    return TodoResponseDto(name=response.name, content=response.content, id=response.id)

@usertodo_router.delete('/:id', status_code=204)
def delete_todo(
    id: UUID,
    request: Request,
    todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))
) -> None:
    todo_service.delete(id, request.state.auth_context)

@usertodo_router.get('/:id', response_model=TodoResponseDto)
def get_todo(
    id: UUID,
    request: Request,
    todo_service: UserTodoService = Depends(lambda: DIContainer.get_instance(UserTodoService))
) -> TodoResponseDto:
    response: TodoResponseModel = todo_service.get_by_id(id, request.state.auth_context)
    return TodoResponseDto(name=response.name, content=response.content, id=response.id)