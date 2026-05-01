from typing import List

from app.api.v1.models import TemperatureReadingPayload


class MemoryDatabase:
    def __init__(self):
        # A strongly-typed list holding Pydantic models in memory
        self.readings: List[TemperatureReadingPayload] = []

    def save_reading(self, reading: TemperatureReadingPayload) -> None:
        """
        Receives a TemperatureReadingPayload and stores it.
        """
        self.readings.append(reading)

    def get_all_readings(self) -> List[TemperatureReadingPayload]:
        """Returns all stored temperature readings."""
        return self.readings

    def get_readings_by_component(self, component_id: str) -> List[TemperatureReadingPayload]:
        """Returns temperature readings for a specific component ID."""
        return [reading for reading in self.readings if reading.componentId == component_id]