from abc import ABC, abstractmethod
from typing import Any

class IEnvironmentVariables(ABC):
    @abstractmethod
    def get_var(self, key: str) -> Any:
        pass