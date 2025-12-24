from abc import ABC, abstractmethod
from typing import List

class BaseRepository(ABC):

    @abstractmethod
    def get_all(self) -> List:
        pass
