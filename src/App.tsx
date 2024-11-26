import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { Dashboard } from './components/Dashboard';
import { AlertPanel } from './components/AlertPanel';
import type { SensorData, Alert } from './types';
import { Sprout } from 'lucide-react';

// Initialize Socket.IO with proper configuration
const socket = io('http://localhost:8000', {
  transports: ['websocket'],
  autoConnect: true,
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5,
  withCredentials: true
});

function App() {
  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [latestData, setLatestData] = useState<SensorData>();
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Socket connection handlers
    socket.on('connect', () => {
      console.log('Connected to WebSocket');
      setConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket');
      setConnected(false);
    });

    socket.on('connect_error', (error) => {
      console.error('Connection error:', error);
    });

    // Data handlers
    socket.on('sensor_data', (data: SensorData) => {
      console.log('Received sensor data:', data);
      setSensorData(prev => [...prev, data].slice(-100));
      setLatestData(data);
    });

    socket.on('alert', (alert: Alert) => {
      console.log('Received alert:', alert);
      setAlerts(prev => [alert, ...prev].slice(0, 5));
    });

    // Initial data fetch
    fetch('http://localhost:8000/api/data')
      .then(res => res.json())
      .then(data => {
        console.log('Initial data loaded:', data);
        setSensorData(data);
        if (data.length > 0) {
          setLatestData(data[data.length - 1]);
        }
      })
      .catch(error => console.error('Error fetching initial data:', error));

    // Cleanup
    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('sensor_data');
      socket.off('alert');
      socket.off('connect_error');
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Sprout className="w-8 h-8 text-green-500" />
              <span className="ml-2 text-xl font-semibold text-gray-900">Farm Monitor</span>
            </div>
            <div className={`px-3 py-1 rounded-full ${connected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {connected ? 'Connected' : 'Disconnected'}
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <Dashboard sensorData={sensorData} latestData={latestData} />
          <div className="mt-6">
            <AlertPanel alerts={alerts} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;