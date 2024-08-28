from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')

class IAuthentication(Generic[T, U], ABC):
    @abstractmethod
    def create(self, obj: U) -> T:
        pass 

    @abstractmethod
    def verify(self, claims: T) -> U:
        pass