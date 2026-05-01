from fastapi import APIRouter, Depends, HTTPException
import datetime
import time

from app.api.v1.models import TemperatureReadingPayload
from app.controller import MemoryDatabaseController

router = APIRouter()
_db_controller_instance = MemoryDatabaseController()

def get_db_controller():
    return _db_controller_instance

@router.get("/is-alive", status_code=200)
async def is_alive():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "OK"}

@router.post("/temperature-reading", status_code=200)
async def temperature_reading(
    reading: TemperatureReadingPayload,
    db_controller: MemoryDatabaseController = Depends(get_db_controller)
):
    """
    Endpoint to receive temperature readings.
    Expects a JSON payload with temperature data.
    """
    # Extract data from the reading
    component_id = reading.componentId
    temperature = reading.temperature
    timestamp = reading.timestamp
    
    # Replace null or missing timestamp with current time in milliseconds
    if timestamp == "null" or timestamp is None:
        # Get current time in milliseconds since epoch
        current_time_ms = int(time.time() * 1000)
        timestamp = current_time_ms
        # Update the timestamp in the reading data
        reading.timestamp = str(current_time_ms)
    
    # Print the fields to console
    print(f"Component ID: {component_id}")
    print(f"Temperature: {temperature}°C")
    print(f"Timestamp: {timestamp}")
    
    # Process and store the reading (placeholder for future implementation)
    db_controller.store_temperature_reading(reading)
    return {"message": "Temperature reading received", "data": reading}

@router.get("/temperature-readings", status_code=200)
async def get_temperature_readings(
    db_controller: MemoryDatabaseController = Depends(get_db_controller)
):
    """
    Endpoint to retrieve all temperature readings grouped by component ID.
    """
    return db_controller.get_grouped_readings()

@router.get("/temperature-readings/{component_id}", status_code=200)
async def get_temperature_readings_by_component(
    component_id: str,
    db_controller: MemoryDatabaseController = Depends(get_db_controller)
):
    """
    Endpoint to retrieve all temperature readings for a specific component ID.
    """
    return db_controller.get_readings_by_component(component_id)

@router.get("/temperature-readings/{component_id}/latest", status_code=200)
async def get_latest_temperature_reading_by_component(
    component_id: str,
    db_controller: MemoryDatabaseController = Depends(get_db_controller)
):
    """
    Endpoint to retrieve the latest temperature reading for a specific component ID.
    """
    latest_reading = db_controller.get_latest_reading_by_component(component_id)
    if not latest_reading:
        raise HTTPException(status_code=404, detail="No readings found for the specified component ID")
    return latest_reading
