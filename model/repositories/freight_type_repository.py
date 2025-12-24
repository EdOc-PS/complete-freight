import json
from typing import List
from model.entities.freight_type import FreightType
from model.repositories.base_repository import BaseRepository

class FreightTypeRepository(BaseRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self) -> List[FreightType]:
        with open(self.file_path, encoding="utf-8") as file:
            data = json.load(file)

        return [FreightType(**item) for item in data]
