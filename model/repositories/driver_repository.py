import json
from typing import List, Optional
from model.entities.driver import Driver
from model.repositories.crud_repository import CrudRepository

class DriverRepository(CrudRepository):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self) -> List[Driver]:
        try:
            with open(self.file_path, encoding="utf-8") as file:
                data = json.load(file)
            return [Driver(**item) for item in data]
        except FileNotFoundError:
            return []

    def get_by_id(self, id: int) -> Optional[Driver]:
        drivers = self.get_all()
        for driver in drivers:
            if driver.id == id:
                return driver
        return None

    def add(self, driver: Driver) -> Driver:
        drivers = self.get_all()
        # Auto-increment ID if not provided (0) or conflict
        if driver.id == 0 or any(d.id == driver.id for d in drivers):
             # simplistic auto-increment
             max_id = max((d.id for d in drivers), default=0)
             driver.id = max_id + 1
        
        drivers.append(driver)
        self._save_all(drivers)
        return driver

    def update(self, driver: Driver) -> Driver:
        drivers = self.get_all()
        for i, d in enumerate(drivers):
            if d.id == driver.id:
                drivers[i] = driver
                self._save_all(drivers)
                return driver
        raise ValueError(f"Driver with id {driver.id} not found")

    def delete(self, id: int) -> bool:
        drivers = self.get_all()
        initial_count = len(drivers)
        drivers = [d for d in drivers if d.id != id]
        if len(drivers) < initial_count:
            self._save_all(drivers)
            return True
        return False

    def _save_all(self, drivers: List[Driver]):
        data = [d.__dict__ for d in drivers]
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
