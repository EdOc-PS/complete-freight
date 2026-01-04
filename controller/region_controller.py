from typing import List, Dict, Any
from model.repositories.region_repository import RegionRepository

class RegionController:
    def __init__(self, repository: RegionRepository):
        self.repository = repository

    def get_all(self) -> List[Dict[str, Any]]:
        regions = self.repository.get_all()
        return [r.__dict__ for r in regions]
