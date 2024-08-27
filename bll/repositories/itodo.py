from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from models.enums import SortDirection
from models.todo import TodoItem


class ITodoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: UUID) -> TodoItem:
        pass

    @abstractmethod
    def create(self, todo: TodoItem) -> TodoItem:
        pass

    @abstractmethod
    def update(self, id: UUID, todo: TodoItem) -> TodoItem:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass

    @abstractmethod
    def get(self, filter_by: Dict[str, Any], sort_by: str, sort_order: SortDirection, offset: int, limit: int) -> List[TodoItem]:
        pass