from typing import List
from model.entities.freight_type import FreightType
from model.repositories.base_repository import BaseRepository
from database.mongo_connection import db


class FreightTypeRepository(BaseRepository):

    def __init__(self):
        self.collection = db["freight_types"]

    def get_all(self) -> List[FreightType]:
        freight_types = []

        for item in self.collection.find():
            freight_types.append(
                FreightType(
                    id=item["id"],
                    description=item["description"]
                )
            )

        return freight_types
