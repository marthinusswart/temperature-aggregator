from pydantic import BaseModel
from typing import Optional, Union


class TemperatureReadingPayload(BaseModel):
    """
    Represents the payload for a temperature reading.

    The fields in this model use camelCase (e.g., `componentId`) rather than 
    Python's standard snake_case to directly match the incoming JSON payloads 
    from external clients or sensors without requiring Pydantic field aliases.
    """
    componentId: str
    temperature: float
    timestamp: Optional[Union[str, int]] = None