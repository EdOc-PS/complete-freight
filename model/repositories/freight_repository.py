from typing import List, Optional
from datetime import date
from bson import ObjectId

from model.entities.freight import Freight
from model.repositories.crud_repository import CrudRepository
from database.mongo_connection import db


class FreightRepository(CrudRepository):

    def __init__(self):
        self.collection = db["freights"]

    def get_all(self) -> List[Freight]:
        freights = []

        for item in self.collection.find():
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
        item = self.collection.find_one({"id": id})
        if not item:
            return None

        return Freight(
            id=item["id"],
            region_id=item["region_id"],
            driver_id=item["driver_id"],
            freight_type_id=item["freight_type_id"],
            send_date=date.fromisoformat(item["send_date"]),
            expected_delivery_date=date.fromisoformat(item["expected_date"]),
            delivery_date=date.fromisoformat(item["delivery_date"]),
            value=item["value"]
        )

    def add(self, freight: Freight) -> Freight:
        last = self.collection.find_one(sort=[("id", -1)])
        freight.id = (last["id"] + 1) if last else 1

        self.collection.insert_one({
            "id": freight.id,
            "region_id": freight.region_id,
            "driver_id": freight.driver_id,
            "freight_type_id": freight.freight_type_id,
            "value": freight.value,
            "send_date": freight.send_date.isoformat(),
            "expected_date": freight.expected_delivery_date.isoformat(),
            "delivery_date": freight.delivery_date.isoformat()
        })

        return freight

    def update(self, freight: Freight) -> Freight:
        result = self.collection.update_one(
            {"id": freight.id},
            {"$set": {
                "region_id": freight.region_id,
                "driver_id": freight.driver_id,
                "freight_type_id": freight.freight_type_id,
                "value": freight.value,
                "send_date": freight.send_date.isoformat(),
                "expected_date": freight.expected_delivery_date.isoformat(),
                "delivery_date": freight.delivery_date.isoformat()
            }}
        )

        if result.matched_count == 0:
            raise ValueError(f"Freight with id {freight.id} not found")

        return freight

    def delete(self, id: int) -> bool:
        result = self.collection.delete_one({"id": id})
        return result.deleted_count > 0
