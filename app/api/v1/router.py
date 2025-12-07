from fastapi import APIRouter
import datetime
import time

router = APIRouter()

@router.get("/is-alive", status_code=200)
async def is_alive():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "OK"}

@router.post("/temperature-reading", status_code=200)
async def temperature_reading(reading: dict):
    """
    Endpoint to receive temperature readings.
    Expects a JSON payload with temperature data.
    """
    # Extract data from the reading    
    component_id = reading.get("componentId")
    temperature = reading.get("temperature")
    timestamp = reading.get("timestamp")
    
    # Replace null timestamp with current time in milliseconds in Zulu time
    if timestamp == "null":
        # Get current time in milliseconds since epoch
        current_time_ms = int(time.time() * 1000)
        timestamp = current_time_ms
        # Update the timestamp in the reading data
        reading["timestamp"] = str(current_time_ms)
    
    # Print the fields to console
    print(f"Component ID: {component_id}")
    print(f"Temperature: {temperature}°C")
    print(f"Timestamp: {timestamp}")
    
    # Process and store the reading (placeholder for future implementation)
    
    return {"message": "Temperature reading received", "data": reading}