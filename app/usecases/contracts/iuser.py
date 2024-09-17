from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from entities.enums import SortDirection
from entities.user import UserEntity

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: UUID) -> UserEntity:
        pass
    
    @abstractmethod
    def get_by_email(self, email:str) -> UserEntity:
        pass

    @abstractmethod
    def create(self, UserEntity: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def update(self, id: UUID, UserEntity: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass

    @abstractmethod
    def get(self, filter_by: Dict[str, Any], sort_by: str, sort_order: SortDirection, offset: int, limit: int) -> List[UserEntity]:
        pass