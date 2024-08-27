

from typing import List
from uuid import UUID
from bll.repositories.itodo import ITodoRepository
from bll.repositories.iuser import IUserRepository
from bll.schemas.authschema import AuthClaimsSchema
from bll.schemas.common import PaginationParams
from bll.schemas.usertodo import CreateTodoSchema, TodoSchema, UpdateTodoSchema
from models.exceptions import NotFoundException
from models.todo import TodoItem

class UserTodoService:
    def __init__(self, todo_repository: ITodoRepository):
        self._todo_repository = todo_repository

    def create(self, todo_dto: CreateTodoSchema, claims: AuthClaimsSchema) -> TodoSchema:
        new_todo: TodoItem = TodoItem(
            owner_id = UUID(claims.id),
            name = todo_dto.name,
            content = todo_dto.content
        )

        new_todo = self._todo_repository.create(new_todo)

        return TodoSchema(
            id = str(new_todo.id),
            name = new_todo.name,
            content = new_todo.content
        )
        

    def get(self, pagination: PaginationParams, claims: AuthClaimsSchema) -> List[TodoSchema]:
        filter_by_dict = {}
        if pagination.filter_key and pagination.filter_value:
            filter_by_dict.update({pagination.filter_key: pagination.filter_value})

        filter_by_dict.update({'owner_id': claims.id})

        todos: List[TodoItem] = self._todo_repository.get(
            filter_by = filter_by_dict,
            sort_by = pagination.sort_by,
            sort_order=pagination.sort_direction,
            offset=pagination.offset,
            limit=pagination.limit
        )

        mapped_todos: List[TodoSchema] = map(lambda x: TodoSchema(name=x.name, content=x.content, id=str(x.id)), todos)

        return mapped_todos
    
    def get_by_id(self, id: UUID, claims: AuthClaimsSchema) -> TodoSchema:
        saved: TodoItem = self._todo_repository.get_by_id(id)
 
        if saved.owner_id != UUID(claims.id):
            raise NotFoundException()


        return TodoSchema(
            id = str(saved.id),
            name = saved.name,
            content = saved.content
        )

    def update(self, id: UUID, todo_dto: UpdateTodoSchema, claims: AuthClaimsSchema) -> TodoSchema:
        existing_todo: TodoItem = self._todo_repository.get_by_id(id)

        if existing_todo.owner_id != UUID(claims.id):
            raise NotFoundException()

        existing_todo.name = todo_dto.name
        existing_todo.content = todo_dto.content

        updated_todo: TodoItem = self._todo_repository.update(id, existing_todo)
        
        return TodoSchema(
            name=updated_todo.name,
            content=updated_todo.content,
            id=str(updated_todo.id)
        )

    def delete(self, id: UUID, claims: AuthClaimsSchema) -> None:
        existing_todo: TodoItem = self._todo_repository.get_by_id(id)

        if existing_todo.owner_id != UUID(claims.id):
            raise NotFoundException()
        
        self._todo_repository.delete(id)
