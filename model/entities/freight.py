from datetime import date

class Freight:
    def __init__(
        self,
        id: int,
        region_id: int,
        driver_id: int,
        freight_type_id: int,
        send_date: date,
        expected_delivery_date: date,
        delivery_date: date,
        value: float
    ):
        self.id = id
        self.region_id = region_id
        self.driver_id = driver_id
        self.freight_type_id = freight_type_id
        self.send_date = send_date
        self.expected_delivery_date = expected_delivery_date
        self.delivery_date = delivery_date
        self.value = value

    def is_delayed(self) -> bool:
        return self.delivery_date > self.expected_delivery_date
