from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from bll.repositories.ienvironment import IEnvironmentVariables

T = TypeVar('T')
U = TypeVar('U')

class IAuthentication(Generic[T, U], ABC):
    @abstractmethod
    def create(self, obj: U, env: IEnvironmentVariables) -> T:
        pass 

    @abstractmethod
    def verify(self, claims: T) -> U:
        pass