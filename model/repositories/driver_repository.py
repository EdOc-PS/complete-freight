import json
from typing import List
from model.entities.driver import Driver
from model.repositories.base_repository import BaseRepository

class DriverRepository(BaseRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self) -> List[Driver]:
        with open(self.file_path, encoding="utf-8") as file:
            data = json.load(file)

        return [Driver(**item) for item in data]
