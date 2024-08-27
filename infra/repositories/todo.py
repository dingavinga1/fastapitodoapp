from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from bll.repositories.itodo import ITodoRepository
from infra.database import Database
from models.constants import MODIFIED_AT_SORT_KEY
from models.enums import SortDirection
from models.exceptions import FilterDoesNotExistException, NotFoundException
from models.todo import TodoItem
from models.user import User

class TodoRepository(ITodoRepository):
    def __init__(self, db: Database):
        self._session = next(db.session())

    def _get_todo_or_none(self, id: UUID) -> Optional[TodoItem]:
        todo = (
            self._session
                .query(TodoItem)
                .filter_by(id=str(id))
                .first()
        )

        return todo

    def get_by_id(self, id: UUID) -> TodoItem:
        todo: TodoItem = self._get_todo_or_none(id)
        if todo is None:
            raise NotFoundException()
        
        return todo

    def create(self, todo: TodoItem) -> TodoItem:
        user_check: Optional[User] = self._session.query(User).filter_by(id=todo.owner_id).first()
        if user_check is None:
            raise NotFoundException()

        self._session.add(todo)
        self._session.commit()

        return todo
    
    def update(self, id: UUID, todo: TodoItem) -> TodoItem:
        todo_found: Optional[TodoItem] = self._get_todo_or_none(id)
        if todo_found is None:
            raise NotFoundException()
        
        obj_dict = todo.__dict__
        todo_dict = todo_found.__dict__

        todo_dict.update(obj_dict)
        todo_found.__dict__ = todo_dict

        self._session.commit()

        return todo_found

    def delete(self, id: UUID) -> None:
        todo: Optional[TodoItem] = self._get_todo_or_none(id)
        if todo is None:
            raise NotFoundException()
        
        self._session.delete(todo)
        self._session.commit()

    def get(self, filter_by: Dict[str, Any], sort_by: str = MODIFIED_AT_SORT_KEY, sort_order: SortDirection = SortDirection.ASC, offset: int = 0, limit: int = 10):
        try:
            sort_direction_func = desc if sort_order == SortDirection.DESC else asc

            todos = (
                self._session
                    .query(TodoItem)
                    .filter_by(**filter_by)
                    .order_by(sort_direction_func(getattr(TodoItem, sort_by)))
                    .offset(offset)
                    .limit(limit)
                    .all()
            )

            return todos
        
        except AttributeError:
            raise FilterDoesNotExistException()
