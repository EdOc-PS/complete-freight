from controller.dashboard_controller import DashboardController
from model.repositories.freight_repository import FreightRepository
from model.repositories.region_repository import RegionRepository
from model.repositories.driver_repository import DriverRepository
from model.repositories.freight_type_repository import FreightTypeRepository

def main():
    controller = DashboardController(
        FreightRepository(),
        RegionRepository(),
        DriverRepository(),
        FreightTypeRepository()
    )

    controller.export_to_json(
        controller.get_freight_volume_by_region(),
        "view/data/freight_by_region.json"
    )

    controller.export_to_json(
        controller.get_delay_rate_by_region(),
        "view/data/delay_rate_by_region.json"
    )

    controller.export_to_json(
        controller.get_revenue_vs_delay_by_freight_type(),
        "view/data/revenue_vs_delay_by_freight_type.json"
    )

    controller.export_to_json(
        controller.get_driver_performance(),
        "view/data/driver_performance.json"
    )

if __name__ == "__main__":
    main()
