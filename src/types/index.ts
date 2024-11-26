export interface SensorData {
  id: number;
  deviceId: string;
  timestamp: string;
  temperature: number;
  humidity: number;
  soilMoisture: number;
}

export interface Rule {
  id: number;
  ruleName: string;
  condition: string;
  action: string;
}

export interface Alert {
  id: number;
  deviceId: string;
  message: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high';
}