from typing import List, Optional
from model.entities.driver import Driver
from model.repositories.crud_repository import CrudRepository
from database.mongo_connection import db


class DriverRepository(CrudRepository):

    def __init__(self):
        self.collection = db["drivers"]

    def get_all(self) -> List[Driver]:
        drivers = []

        for item in self.collection.find():
            drivers.append(
                Driver(
                    id=item["id"],
                    name=item["name"]
                )
            )

        return drivers

    def get_by_id(self, id: int) -> Optional[Driver]:
        item = self.collection.find_one({"id": id})
        if not item:
            return None

        return Driver(
            id=item["id"],
            name=item["name"]
        )

    def add(self, driver: Driver) -> Driver:
        last = self.collection.find_one(sort=[("id", -1)])
        driver.id = (last["id"] + 1) if last else 1

        self.collection.insert_one({
            "id": driver.id,
            "name": driver.name
        })

        return driver

    def update(self, driver: Driver) -> Driver:
        result = self.collection.update_one(
            {"id": driver.id},
            {"$set": {
                "name": driver.name
            }}
        )

        if result.matched_count == 0:
            raise ValueError(f"Driver with id {driver.id} not found")

        return driver

    def delete(self, id: int) -> bool:
        result = self.collection.delete_one({"id": id})
        return result.deleted_count > 0
