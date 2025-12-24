import json
from typing import List
from model.entities.region import Region
from model.repositories.base_repository import BaseRepository

class RegionRepository(BaseRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self) -> List[Region]:
        with open(self.file_path, encoding="utf-8") as file:
            data = json.load(file)

        return [Region(**item) for item in data]
