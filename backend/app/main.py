from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import socketio
from datetime import datetime
import asyncio
from typing import List
import json
from .database import SessionLocal, engine
from . import models, schemas
from .mock_data import generate_mock_data, simulate_real_time_data
from .config import get_settings

# Create database tables
models.Base.metadata.create_all(bind=engine)

settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title="Farm Management System",
    description="Real-time farm monitoring system with IoT sensor data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize Socket.IO with proper CORS configuration
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["http://localhost:5173"],
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

socket_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path='socket.io'
)

# Setup CORS for FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO app
app.mount('/ws', socket_app)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connection_established', {'status': 'connected'})

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@app.get("/api/data", response_model=List[schemas.SensorData])
async def get_sensor_data():
    db = next(get_db())
    data = db.query(models.SensorData).order_by(models.SensorData.timestamp.desc()).limit(100).all()
    return data

@app.post("/api/data", response_model=schemas.SensorData)
async def add_sensor_data(data: schemas.SensorDataCreate):
    db = next(get_db())
    db_data = models.SensorData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    
    # Convert to dict for Socket.IO emission
    sensor_data_dict = schemas.SensorData.from_orm(db_data).dict()
    # Convert datetime to ISO format string
    sensor_data_dict['timestamp'] = sensor_data_dict['timestamp'].isoformat()
    
    # Emit the new data via Socket.IO
    await sio.emit('sensor_data', sensor_data_dict)
    
    # Check alert conditions
    await check_alert_conditions(db_data)
    
    return db_data

async def check_alert_conditions(sensor_data: models.SensorData):
    alerts = []
    
    if sensor_data.temperature > settings.TEMPERATURE_MAX_THRESHOLD:
        alerts.append(schemas.Alert(
            deviceId=sensor_data.deviceId,
            message=f"High temperature alert: {sensor_data.temperature}°C",
            severity="high",
            timestamp=datetime.now().isoformat()
        ))
    
    if sensor_data.humidity < settings.HUMIDITY_MIN_THRESHOLD:
        alerts.append(schemas.Alert(
            deviceId=sensor_data.deviceId,
            message=f"Low humidity alert: {sensor_data.humidity}%",
            severity="medium",
            timestamp=datetime.now().isoformat()
        ))
    
    if sensor_data.soilMoisture < settings.SOIL_MOISTURE_MIN_THRESHOLD:
        alerts.append(schemas.Alert(
            deviceId=sensor_data.deviceId,
            message=f"Low soil moisture alert: {sensor_data.soilMoisture}%",
            severity="high",
            timestamp=datetime.now().isoformat()
        ))
    
    # Emit alerts via Socket.IO
    for alert in alerts:
        await sio.emit('alert', alert.dict())

@app.on_event("startup")
async def startup_event():
    # Generate initial mock data
    db = next(get_db())
    if db.query(models.SensorData).count() == 0:
        mock_data = generate_mock_data(24)  # Generate 24 hours of data
        db.bulk_save_objects(mock_data)
        db.commit()
    
    # Start background task for real-time data simulation
    asyncio.create_task(simulate_real_time_data())