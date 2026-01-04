from typing import List
from model.entities.region import Region
from model.repositories.base_repository import BaseRepository
from database.mongo_connection import db


class RegionRepository(BaseRepository):

    def __init__(self):
        self.collection = db["regions"]

    def get_all(self) -> List[Region]:
        regions = []

        for item in self.collection.find():
            regions.append(
                Region(
                    id=item["id"],
                    name=item["name"]
                )
            )

        return regions
