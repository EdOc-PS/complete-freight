import json
from collections import defaultdict
from typing import List, Dict

from model.entities.freight import Freight
from model.entities.region import Region
from model.entities.driver import Driver
from model.entities.freight_type import FreightType

from model.repositories.freight_repository import FreightRepository
from model.repositories.region_repository import RegionRepository
from model.repositories.driver_repository import DriverRepository
from model.repositories.freight_type_repository import FreightTypeRepository

class DashboardController:

    def __init__(
        self,
        freight_repo: FreightRepository,
        region_repo: RegionRepository,
        driver_repo: DriverRepository,
        freight_type_repo: FreightTypeRepository
    ):
        self.freight_repo = freight_repo
        self.region_repo = region_repo
        self.driver_repo = driver_repo
        self.freight_type_repo = freight_type_repo

    def get_freight_volume_by_region(self) -> Dict:
        freights = self.freight_repo.get_all()
        regions = self.region_repo.get_all()

        region_map = {r.id: r.name for r in regions}
        counter = defaultdict(int)

        for freight in freights:
            counter[freight.region_id] += 1

        return {
            "labels": [region_map[rid] for rid in counter],
            "values": list(counter.values())
        }

    def get_delay_rate_by_region(self) -> Dict:
        freights = self.freight_repo.get_all()
        regions = self.region_repo.get_all()

        region_map = {r.id: r.name for r in regions}
        total = defaultdict(int)
        delayed = defaultdict(int)

        for freight in freights:
            total[freight.region_id] += 1
            if freight.is_delayed():
                delayed[freight.region_id] += 1

        result = {
            "labels": [],
            "values": []
        }

        for region_id in total:
            rate = (delayed[region_id] / total[region_id]) * 100
            result["labels"].append(region_map[region_id])
            result["values"].append(round(rate, 2))

        return result

    def get_driver_performance(self) -> Dict:
        freights = self.freight_repo.get_all()
        drivers = self.driver_repo.get_all()

        driver_map = {d.id: d.name for d in drivers}
        total = defaultdict(int)
        on_time = defaultdict(int)

        for freight in freights:
            total[freight.driver_id] += 1
            if not freight.is_delayed():
                on_time[freight.driver_id] += 1

        result = {
            "labels": [],
            "values": []
        }

        for driver_id in total:
            performance = (on_time[driver_id] / total[driver_id]) * 100
            result["labels"].append(driver_map[driver_id])
            result["values"].append(round(performance, 2))

        return result

    def get_revenue_vs_delay_by_freight_type(self):
        freight_types = self.freight_type_repo.get_all()
        freights = self.freight_repo.get_all()

        data_points = []

        for freight_type in freight_types:
            total = 0
            delayed = 0
            revenue = 0.0

            for freight in freights:
                if freight.freight_type_id == freight_type.id:
                    total += 1
                    revenue += freight.value
                    if freight.is_delayed():
                        delayed += 1

            delay_rate = delayed / total if total > 0 else 0

            data_points.append({
                "x": round(delay_rate, 2),
                "y": round(revenue, 2),
                "label": freight_type.description
            })

        return data_points


    def export_to_json(self, data, output_path: str):
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
