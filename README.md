# Farm Management System

A real-time farm monitoring system that simulates IoT device data collection for agricultural environments, featuring live data visualization and alerts.

## Features

- 📊 Real-time sensor data monitoring (temperature, humidity, soil moisture)
- 📈 Live data visualization with interactive charts
- ⚡ WebSocket-based real-time updates
- 🔔 Automated alert system for critical conditions
- 🤖 Mock data generation for testing and demonstration

## Tech Stack

### Frontend
- React + TypeScript
- Tailwind CSS
- Recharts for data visualization
- Socket.IO client for real-time updates
- Lucide React for icons

### Backend
- FastAPI (Python)
- PostgreSQL for data storage
- Redis for caching
- Socket.IO for real-time communication
- Docker for containerization

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+
- Python 3.9+

### Environment Setup

1. **Frontend Setup**
   ```bash
   # Copy environment file
   cp .env.example .env
   
   # Install dependencies
   npm install
   ```

2. **Backend Setup**
   ```bash
   cd backend
   
   # Copy environment file
   cp .env.example .env
   
   # Create Python virtual environment
   python3.9 -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start Backend Services**
   ```bash
   cd backend
   docker compose up
   ```
   This starts:
   - PostgreSQL (port 5432)
   - Redis (port 6379)
   - FastAPI server (port 8000)

2. **Start Frontend Development Server**
   ```bash
   npm run dev
   ```
   Access the application at http://localhost:5173

## API Documentation

### Data Endpoints

- `GET /api/data`
  - Retrieves latest sensor data
  - Returns last 100 readings

- `POST /api/data`
  - Submits new sensor reading
  - Required fields:
    ```json
    {
      "deviceId": "string",
      "temperature": "float",
      "humidity": "float",
      "soilMoisture": "float"
    }
    ```

### WebSocket Events

- `sensor_data`: Real-time sensor updates
- `alert`: System alerts for critical conditions

## Alert Thresholds

The system generates alerts when:
- Temperature > 35°C
- Humidity < 30%
- Soil Moisture < 20%

## Development

### Frontend Structure
```
src/
├── components/        # React components
├── types/            # TypeScript interfaces
├── App.tsx           # Main application component
└── main.tsx         # Application entry point
```

### Backend Structure
```
backend/
├── app/
│   ├── models.py     # Database models
│   ├── schemas.py    # Pydantic schemas
│   ├── database.py   # Database configuration
│   └── main.py       # FastAPI application
├── requirements.txt
└── docker-compose.yml
```

## Docker Commands

### Basic Operations

```bash
# Start all services
docker-compose up

# Start specific service
docker-compose up db

# Stop all services
docker-compose down

# View logs
docker-compose logs -f
```

### Database Management

```bash
# Access PostgreSQL
docker-compose exec db psql -U postgres -d farm_management

# Backup database
docker-compose exec db pg_dump -U postgres farm_management > backup.sql
```

## License

MIT License - feel free to use this project for your own purposes.