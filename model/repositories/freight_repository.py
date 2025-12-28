import json
from typing import List, Optional
from datetime import date
from model.entities.freight import Freight
from model.repositories.crud_repository import CrudRepository

class FreightRepository(CrudRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self) -> List[Freight]:
        try:
            with open(self.file_path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []

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

    def get_by_id(self, id: int) -> Optional[Freight]:
        freights = self.get_all()
        for freight in freights:
            if freight.id == id:
                return freight
        return None

    def add(self, freight: Freight) -> Freight:
        freights = self.get_all()
        if freight.id == 0 or any(f.id == freight.id for f in freights):
             max_id = max((f.id for f in freights), default=0)
             freight.id = max_id + 1
        
        freights.append(freight)
        self._save_all(freights)
        return freight

    def update(self, freight: Freight) -> Freight:
        freights = self.get_all()
        for i, f in enumerate(freights):
            if f.id == freight.id:
                freights[i] = freight
                self._save_all(freights)
                return freight
        raise ValueError(f"Freight with id {freight.id} not found")

    def delete(self, id: int) -> bool:
        freights = self.get_all()
        initial_count = len(freights)
        freights = [f for f in freights if f.id != id]
        if len(freights) < initial_count:
            self._save_all(freights)
            return True
        return False

    def _save_all(self, freights: List[Freight]):
        data = []
        for f in freights:
            data.append({
                "id": f.id,
                "region_id": f.region_id,
                "driver_id": f.driver_id,
                "freight_type_id": f.freight_type_id,
                "value": f.value,
                "send_date": f.send_date.isoformat(),
                "expected_date": f.expected_delivery_date.isoformat(),
                "delivery_date": f.delivery_date.isoformat()
            })
            
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
