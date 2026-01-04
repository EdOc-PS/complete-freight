from typing import List, Dict, Any
from datetime import date
from model.entities.freight import Freight
from model.repositories.freight_repository import FreightRepository

class FreightController:
    def __init__(self, repository: FreightRepository):
        self.repository = repository

    def get_all(self) -> List[Dict[str, Any]]:
        freights = self.repository.get_all()
        return [self._to_dict(f) for f in freights]

    def get_by_id(self, id: int) -> Dict[str, Any]:
        freight = self.repository.get_by_id(id)
        if freight:
            return self._to_dict(freight)
        return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        freight = Freight(
            id=0,
            region_id=int(data['region_id']),
            driver_id=int(data['driver_id']),
            freight_type_id=int(data['freight_type_id']),
            value=float(data['value']),
            send_date=date.fromisoformat(data['send_date']),
            expected_delivery_date=date.fromisoformat(data['expected_delivery_date']),
            delivery_date=date.fromisoformat(data['delivery_date'])
        )
        new_freight = self.repository.add(freight)
        return self._to_dict(new_freight)

    def update(self, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        freight = Freight(
            id=id,
            region_id=int(data['region_id']),
            driver_id=int(data['driver_id']),
            freight_type_id=int(data['freight_type_id']),
            value=float(data['value']),
            send_date=date.fromisoformat(data['send_date']),
            expected_delivery_date=date.fromisoformat(data['expected_delivery_date']),
            delivery_date=date.fromisoformat(data['delivery_date'])
        )
        updated = self.repository.update(freight)
        return self._to_dict(updated)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def _to_dict(self, f: Freight) -> Dict[str, Any]:
        d = f.__dict__.copy()
        d['send_date'] = f.send_date.isoformat()
        d['expected_delivery_date'] = f.expected_delivery_date.isoformat()
        d['delivery_date'] = f.delivery_date.isoformat()
        return d
