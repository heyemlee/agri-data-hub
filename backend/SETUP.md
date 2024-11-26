# Detailed Backend Setup Instructions

## Prerequisites Installation

1. Install PostgreSQL:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib

   # macOS with Homebrew
   brew install postgresql
   ```

2. Install Redis:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server

   # macOS with Homebrew
   brew install redis
   ```

## Step-by-Step Setup Process

1. **Create and activate Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup PostgreSQL database**
   ```bash
   # Login to PostgreSQL
   sudo -u postgres psql

   # Create database and user
   CREATE DATABASE farm_management;
   CREATE USER postgres WITH PASSWORD 'postgres';
   GRANT ALL PRIVILEGES ON DATABASE farm_management TO postgres;
   
   # Exit PostgreSQL
   \q
   ```

4. **Configure environment variables**
   ```bash
   # Copy example environment file
   cp .env.example .env
   ```

5. **Start Redis server**
   ```bash
   # Start Redis in background
   redis-server &
   ```

6. **Start the FastAPI server**
   ```bash
   # Development mode with auto-reload
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Verification Steps

1. **Check FastAPI Documentation**
   - Open browser and visit: http://localhost:8000/docs
   - All endpoints should be visible and documented

2. **Verify Database Connection**
   ```bash
   # Connect to database
   psql -U postgres -d farm_management
   
   # List tables
   \dt
   
   # Should see sensor_data table
   ```

3. **Test WebSocket Connection**
   ```bash
   # Using wscat (install with: npm install -g wscat)
   wscat -c ws://localhost:8000/ws
   ```

4. **Monitor Real-time Data**
   - Check FastAPI logs for mock data generation
   - Verify data in PostgreSQL:
     ```sql
     SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 5;
     ```

## Troubleshooting

1. **Database Connection Issues**
   ```bash
   # Check PostgreSQL status
   sudo service postgresql status
   
   # Restart if needed
   sudo service postgresql restart
   ```

2. **Redis Issues**
   ```bash
   # Check Redis status
   redis-cli ping
   # Should return PONG
   
   # Restart Redis if needed
   sudo service redis-server restart
   ```

3. **No Data Flowing**
   - Check FastAPI logs for errors
   - Verify mock data generation is running
   - Check database connections in .env file
   - Ensure CORS settings match your frontend URL

## Common Issues and Solutions

1. **CORS Errors**
   - Verify CORS_ORIGINS in .env matches your frontend URL
   - Default development URL is http://localhost:5173

2. **WebSocket Connection Failed**
   - Check if frontend WebSocket URL matches backend
   - Ensure no firewall blocking WebSocket connections
   - Verify CORS settings include WebSocket origin

3. **No Real-time Updates**
   - Check if mock data generation is running
   - Verify Socket.IO connection in frontend console
   - Ensure database writes are successful