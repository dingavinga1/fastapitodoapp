from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from models.enums import SortDirection
from models.user import User

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: UUID) -> User:
        pass
    
    @abstractmethod
    def get_by_email(self, email:str) -> User:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, id: UUID, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass

    @abstractmethod
    def get(self, filter_by: Dict[str, Any], sort_by: str, sort_order: SortDirection, offset: int, limit: int) -> List[User]:
        pass