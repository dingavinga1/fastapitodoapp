from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from entities.enums import SortDirection
from entities.todo import TodoItemEntity


class ITodoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: UUID) -> TodoItemEntity:
        pass

    @abstractmethod
    def create(self, todo: TodoItemEntity) -> TodoItemEntity:
        pass

    @abstractmethod
    def update(self, id: UUID, todo: TodoItemEntity) -> TodoItemEntity:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass

    @abstractmethod
    def get(self, filter_by: Dict[str, Any], sort_by: str, sort_order: SortDirection, offset: int, limit: int) -> List[TodoItemEntity]:
        pass