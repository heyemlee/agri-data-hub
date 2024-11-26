import asyncio
import httpx
from datetime import datetime, timedelta
import random
from . import models
from .config import get_settings

settings = get_settings()

def generate_mock_data(hours: int):
    mock_data = []
    base_time = datetime.now() - timedelta(hours=hours)
    
    for hour in range(hours * 4):  # Generate data every 15 minutes
        timestamp = base_time + timedelta(minutes=15 * hour)
        
        # Generate realistic-looking data with some variation
        temperature = 25 + random.uniform(-5, 5)  # Temperature between 20-30°C
        humidity = 60 + random.uniform(-10, 10)   # Humidity between 50-70%
        soil_moisture = 40 + random.uniform(-5, 5) # Soil moisture between 35-45%
        
        data = models.SensorData(
            deviceId="DEVICE001",
            timestamp=timestamp,
            temperature=temperature,
            humidity=humidity,
            soilMoisture=soil_moisture
        )
        mock_data.append(data)
    
    return mock_data

async def simulate_real_time_data():
    """Generate and send mock data every 15 seconds"""
    while True:
        await asyncio.sleep(settings.DATA_COLLECTION_INTERVAL)
        
        temperature = 25 + random.uniform(-5, 5)
        humidity = 60 + random.uniform(-10, 10)
        soil_moisture = 40 + random.uniform(-5, 5)
        
        data = {
            "deviceId": "DEVICE001",
            "timestamp": datetime.now().isoformat(),
            "temperature": temperature,
            "humidity": humidity,
            "soilMoisture": soil_moisture
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://{settings.HOST}:{settings.PORT}/api/data",
                    json=data,
                    timeout=10.0
                )
                if response.status_code != 200:
                    print(f"Error sending mock data: {response.status_code}")
        except Exception as e:
            print(f"Error in mock data generation: {e}")