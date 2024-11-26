from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SensorDataBase(BaseModel):
    deviceId: str
    temperature: float
    humidity: float
    soilMoisture: float

class SensorDataCreate(SensorDataBase):
    timestamp: Optional[datetime] = None

class SensorData(SensorDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class Alert(BaseModel):
    deviceId: str
    message: str
    severity: str
    timestamp: str