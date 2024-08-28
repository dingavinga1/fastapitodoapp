from typing import List
from uuid import UUID
from usecases.contracts.itodo import ITodoRepository
from usecases.contracts.iuser import IUserRepository
from usecases.models.auth import AuthClaimsModel
from usecases.models.common import PaginationParams
from usecases.models.usertodo import CreateTodoRequestModel, TodoResponseModel, UpdateTodoRequestModel
from entities.exceptions import NotFoundException
from entities.todo import TodoItemEntity

class UserTodoService:
    def __init__(self, todo_repository: ITodoRepository):
        self._todo_repository = todo_repository

    def create(self, todo_dto: CreateTodoRequestModel, claims: AuthClaimsModel) -> TodoResponseModel:
        new_todo: TodoItemEntity = TodoItemEntity(
            owner_id = UUID(claims.id),
            name = todo_dto.name,
            content = todo_dto.content
        )

        new_todo = self._todo_repository.create(new_todo)

        return TodoResponseModel(
            id = str(new_todo.id),
            name = new_todo.name,
            content = new_todo.content
        )
        

    def get(self, pagination: PaginationParams, claims: AuthClaimsModel) -> List[TodoResponseModel]:
        filter_by_dict = {}
        if pagination.filter_key and pagination.filter_value:
            filter_by_dict.update({pagination.filter_key: pagination.filter_value})

        filter_by_dict.update({'owner_id': claims.id})

        todos: List[TodoItemEntity] = self._todo_repository.get(
            filter_by = filter_by_dict,
            sort_by = pagination.sort_by,
            sort_order=pagination.sort_direction,
            offset=pagination.offset,
            limit=pagination.limit
        )

        mapped_todos: List[TodoResponseModel] = map(lambda x: TodoResponseModel(name=x.name, content=x.content, id=str(x.id)), todos)

        return mapped_todos
    
    def get_by_id(self, id: UUID, claims: AuthClaimsModel) -> TodoResponseModel:
        saved: TodoItemEntity = self._todo_repository.get_by_id(id)
 
        if saved.owner_id != UUID(claims.id):
            raise NotFoundException()


        return TodoResponseModel(
            id = str(saved.id),
            name = saved.name,
            content = saved.content
        )

    def update(self, id: UUID, todo_dto: UpdateTodoRequestModel, claims: AuthClaimsModel) -> TodoResponseModel:
        existing_todo: TodoItemEntity = self._todo_repository.get_by_id(id)

        if existing_todo.owner_id != UUID(claims.id):
            raise NotFoundException()

        existing_todo.name = todo_dto.name
        existing_todo.content = todo_dto.content

        updated_todo: TodoItemEntity = self._todo_repository.update(id, existing_todo)
        
        return TodoResponseModel(
            name=updated_todo.name,
            content=updated_todo.content,
            id=str(updated_todo.id)
        )

    def delete(self, id: UUID, claims: AuthClaimsModel) -> None:
        existing_todo: TodoItemEntity = self._todo_repository.get_by_id(id)

        if existing_todo.owner_id != UUID(claims.id):
            raise NotFoundException()
        
        self._todo_repository.delete(id)
