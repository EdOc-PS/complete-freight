from typing import List, Dict, Any
from model.entities.driver import Driver
from model.repositories.driver_repository import DriverRepository

class DriverController:
    def __init__(self, repository: DriverRepository):
        self.repository = repository

    def get_all(self) -> List[Dict[str, Any]]:
        drivers = self.repository.get_all()
        return [d.__dict__ for d in drivers]

    def get_by_id(self, id: int) -> Dict[str, Any]:
        driver = self.repository.get_by_id(id)
        if driver:
            return driver.__dict__
        return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        driver = Driver(id=0, name=data['name'], active=data.get('active', True))
        new_driver = self.repository.add(driver)
        return new_driver.__dict__

    def update(self, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        driver = Driver(id=id, name=data['name'], active=data.get('active', True))
        updated = self.repository.update(driver)
        return updated.__dict__
    
    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
