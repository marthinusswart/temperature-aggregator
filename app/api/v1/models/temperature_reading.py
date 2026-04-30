from pydantic import BaseModel
from typing import Optional, Union


class TemperatureReadingPayload(BaseModel):
    componentId: str
    temperature: float
    timestamp: Optional[Union[str, int]] = None