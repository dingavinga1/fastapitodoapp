from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from usecases.contracts.itodo import ITodoRepository
from infra.database import Database
from entities.constants import MODIFIED_AT_SORT_KEY
from entities.enums import SortDirection
from entities.exceptions import FilterDoesNotExistException, NotFoundException
from entities.todo import TodoItemEntity
from entities.user import UserEntity

class TodoRepository(ITodoRepository):
    def __init__(self, db: Database):
        self._session = next(db.session())

    def _get_todo_or_none(self, id: UUID) -> Optional[TodoItemEntity]:
        todo = (
            self._session
                .query(TodoItemEntity)
                .filter_by(id=str(id))
                .first()
        )

        return todo

    def get_by_id(self, id: UUID) -> TodoItemEntity:
        todo: TodoItemEntity = self._get_todo_or_none(id)
        if todo is None:
            raise NotFoundException()
        
        return todo

    def create(self, todo: TodoItemEntity) -> TodoItemEntity:
        user_check: Optional[UserEntity] = self._session.query(UserEntity).filter_by(id=todo.owner_id).first()
        if user_check is None:
            raise NotFoundException()

        self._session.add(todo)
        self._session.commit()

        return todo
    
    def update(self, id: UUID, todo: TodoItemEntity) -> TodoItemEntity:
        todo_found: Optional[TodoItemEntity] = self._get_todo_or_none(id)
        if todo_found is None:
            raise NotFoundException()
        
        obj_dict = todo.__dict__
        todo_dict = todo_found.__dict__

        todo_dict.update(obj_dict)
        todo_found.__dict__ = todo_dict

        self._session.commit()

        return todo_found

    def delete(self, id: UUID) -> None:
        todo: Optional[TodoItemEntity] = self._get_todo_or_none(id)
        if todo is None:
            raise NotFoundException()
        
        self._session.delete(todo)
        self._session.commit()

    def get(self, filter_by: Dict[str, Any], sort_by: str = MODIFIED_AT_SORT_KEY, sort_order: SortDirection = SortDirection.ASC, offset: int = 0, limit: int = 10):
        try:
            sort_direction_func = desc if sort_order == SortDirection.DESC else asc

            todos = (
                self._session
                    .query(TodoItemEntity)
                    .filter_by(**filter_by)
                    .order_by(sort_direction_func(getattr(TodoItemEntity, sort_by)))
                    .offset(offset)
                    .limit(limit)
                    .all()
            )

            return todos
        
        except AttributeError:
            raise FilterDoesNotExistException()
