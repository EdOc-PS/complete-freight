from typing import List, Dict, Any
from model.repositories.freight_type_repository import FreightTypeRepository

class FreightTypeController:
    def __init__(self, repository: FreightTypeRepository):
        self.repository = repository

    def get_all(self) -> List[Dict[str, Any]]:
        freight_types = self.repository.get_all()
        return [ft.__dict__ for ft in freight_types]
