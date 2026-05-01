from typing import List, Dict, Optional
from app.api.v1.models import TemperatureReadingPayload
from app.data import MemoryDatabase

class MemoryDatabaseController:
    def __init__(self):
        self.memory_db = MemoryDatabase()

    def store_temperature_reading(self, reading: TemperatureReadingPayload) -> None:
        """Passes the temperature reading payload to the memory database for storage."""
        self.memory_db.save_reading(reading)

    def get_all_readings(self) -> List[TemperatureReadingPayload]:
        """Retrieves all temperature readings from the memory database."""
        return self.memory_db.get_all_readings()

    def get_readings_by_component(self, component_id: str) -> List[TemperatureReadingPayload]:
        """Retrieves temperature readings for a specific component ID from the memory database."""
        return self.memory_db.get_readings_by_component(component_id)

    def get_grouped_readings(self) -> Dict[str, List[TemperatureReadingPayload]]:
        """Retrieves all temperature readings grouped by component ID."""
        readings = self.get_all_readings()
        grouped_readings = {}
        for reading in readings:
            if reading.componentId not in grouped_readings:
                grouped_readings[reading.componentId] = []
            grouped_readings[reading.componentId].append(reading)
        return grouped_readings

    def get_latest_reading_by_component(self, component_id: str) -> Optional[TemperatureReadingPayload]:
        """Retrieves the latest temperature reading for a specific component ID."""
        readings = self.get_readings_by_component(component_id)
        if not readings:
            return None
        return max(readings, key=lambda r: int(r.timestamp) if r.timestamp else 0)