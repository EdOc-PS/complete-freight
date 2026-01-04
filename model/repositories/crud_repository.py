from abc import ABC, abstractmethod
from typing import Any, List, Optional

class CrudRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def add(self, entity: Any) -> Any:
        pass

    @abstractmethod
    def update(self, entity: Any) -> Any:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
