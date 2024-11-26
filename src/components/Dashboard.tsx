import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';
import { Thermometer, Droplets, Sprout } from 'lucide-react';
import type { SensorData } from '../types';

interface DashboardProps {
  sensorData: SensorData[];
  latestData?: SensorData;
}

export const Dashboard: React.FC<DashboardProps> = ({ sensorData, latestData }) => {
  const formatXAxis = (tickItem: string) => {
    return format(new Date(tickItem), 'HH:mm');
  };

  return (
    <div className="p-6 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center space-x-4">
            <Thermometer className="w-8 h-8 text-red-500" />
            <div>
              <p className="text-gray-500">Temperature</p>
              <p className="text-2xl font-bold">{latestData?.temperature.toFixed(1)}°C</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center space-x-4">
            <Droplets className="w-8 h-8 text-blue-500" />
            <div>
              <p className="text-gray-500">Humidity</p>
              <p className="text-2xl font-bold">{latestData?.humidity.toFixed(1)}%</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center space-x-4">
            <Sprout className="w-8 h-8 text-green-500" />
            <div>
              <p className="text-gray-500">Soil Moisture</p>
              <p className="text-2xl font-bold">{latestData?.soilMoisture.toFixed(1)}%</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Sensor Data Trends</h2>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sensorData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" tickFormatter={formatXAxis} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="temperature" stroke="#ef4444" name="Temperature (°C)" />
              <Line type="monotone" dataKey="humidity" stroke="#3b82f6" name="Humidity (%)" />
              <Line type="monotone" dataKey="soilMoisture" stroke="#22c55e" name="Soil Moisture (%)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};