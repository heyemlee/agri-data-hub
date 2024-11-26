import React from 'react';
import { AlertTriangle } from 'lucide-react';
import type { Alert } from '../types';

interface AlertPanelProps {
  alerts: Alert[];
}

export const AlertPanel: React.FC<AlertPanelProps> = ({ alerts }) => {
  const getSeverityColor = (severity: Alert['severity']) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 border-red-500 text-red-700';
      case 'medium':
        return 'bg-yellow-100 border-yellow-500 text-yellow-700';
      case 'low':
        return 'bg-blue-100 border-blue-500 text-blue-700';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center space-x-2 mb-4">
        <AlertTriangle className="w-6 h-6 text-red-500" />
        <h2 className="text-xl font-semibold">Active Alerts</h2>
      </div>
      
      <div className="space-y-4">
        {alerts.length === 0 ? (
          <p className="text-gray-500">No active alerts</p>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-4 border-l-4 rounded ${getSeverityColor(alert.severity)}`}
            >
              <div className="flex justify-between">
                <p className="font-medium">{alert.message}</p>
                <span className="text-sm">{new Date(alert.timestamp).toLocaleTimeString()}</span>
              </div>
              <p className="text-sm mt-1">Device ID: {alert.deviceId}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};