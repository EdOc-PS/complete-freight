import json
from typing import List
from datetime import date
from model.entities.freight import Freight
from model.repositories.base_repository import BaseRepository

class FreightRepository(BaseRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self) -> List[Freight]:
        with open(self.file_path, encoding="utf-8") as file:
            data = json.load(file)

        freights = []
        for item in data:
            freights.append(
                Freight(
                    id=item["id"],
                    region_id=item["region_id"],
                    driver_id=item["driver_id"],
                    freight_type_id=item["freight_type_id"],
                    send_date=date.fromisoformat(item["send_date"]),
                    expected_delivery_date=date.fromisoformat(item["expected_date"]),
                    delivery_date=date.fromisoformat(item["delivery_date"]),
                    value=item["value"]
                )
            )
        return freights
