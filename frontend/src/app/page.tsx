"use client"
import {
  AlertTriangle,
  BarChart,
  Bell,
  Filter,
  Search,
  Shield,
  TrendingUp
} from 'lucide-react';
import { useState } from 'react';
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

// Mock data - replace with actual API integration
const mockNotifications = [
  {
    id: 1,  
    eventType: 'Anomaly',
    description: 'Unusual traffic spike detected',
    timestamp: '2024-01-25 14:30:45',
    evidence: 'Traffic increased by 200% in 5 minutes', 
    severity: 'high'
  },
  {
    id: 2,
    eventType: 'Security Alert',
    description: 'Potential unauthorized access',
    timestamp: '2024-01-25 15:12:22',
    evidence: 'Multiple login attempts from unknown IP',
    severity: 'critical'
  }
  ,
  {
    id: 3,
    eventType: 'Security Alert',
    description: 'Potential unauthorized access',
    timestamp: '2024-01-25 15:12:22',
    evidence: 'Multiple login attempts from unknown IP',
    severity: 'high'
  }
  ,
  {
    id: 4,
    eventType: 'Security Alert',
    description: 'Potential unauthorized access',
    timestamp: '2024-01-25 15:12:22',
    evidence: 'Multiple login attempts from unknown IP',
    severity: 'critical'
  }
  ,
  {
    id: 5,
    eventType: 'Security Alert',
    description: 'Potential unauthorized access',
    timestamp: '2024-01-25 15:12:22',
    evidence: 'Multiple login attempts from unknown IP',
    severity: 'critical'
  }
  ,
  {
    id: 6,
    eventType: 'Security Alert',
    description: 'Potential unauthorized access',
    timestamp: '2024-01-25 15:12:22',
    evidence: 'Multiple login attempts from unknown IP',
    severity: 'critical'
  }
  ,
  {
    id: 7,
    eventType: 'Security Alert',
    description: 'Potential unauthorized access',
    timestamp: '2024-01-25 15:12:22',
    evidence: 'Multiple login attempts from unknown IP',
    severity: 'critical'
  }
  ,
  {
    id: 8,
    eventType: 'Security Alert',
    description: 'Potential unauthorized access',
    timestamp: '2024-01-25 15:12:22',
    evidence: 'Multiple login attempts from unknown IP',
    severity: 'critical'
  }
  ,
  {
    id: 9,
    eventType: 'Security Alert',
    description: 'Potential unauthorized access',
    timestamp: '2024-01-25 15:12:22',
    evidence: 'Multiple login attempts from unknown IP',
    severity: 'critical'
  }
  
];

const trafficData = [
  { name: '12am', traffic: 400, anomalies: 20 },
  { name: '6am', traffic: 300, anomalies: 15 },
  { name: '12pm', traffic: 200, anomalies: 10 },
  { name: '6pm', traffic: 278, anomalies: 25 },
  { name: '11pm', traffic: 189, anomalies: 8 }
];

const MonitoringDashboard = () => {
  const [notifications, setNotifications] = useState(mockNotifications);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('');

  console.log(setNotifications);
  // Filtering logic
  const filteredNotifications = notifications.filter(notification => 
    (filterType ? notification.eventType === filterType : true) &&
    (searchTerm 
      ? notification.description.toLowerCase().includes(searchTerm.toLowerCase()) 
      : true)
  );

  // Severity color mapping
  const getSeverityColor = (severity: string) => {
    switch(severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      default: return 'bg-green-500';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl md:text-3xl font-bold text-gray-800 flex items-center">
            <Bell className="mr-3 text-blue-600" />
            Blockchain Monitoring Dashboard
          </h1>
        </div>

        {/* Filters */}
        <div className="bg-white shadow-md rounded-lg p-4 mb-6">
          <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
            <div className="relative flex-grow">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input 
                type="text"
                placeholder="Search notifications..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 p-2 border rounded-md focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>
            <div className="relative">
              <select 
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="w-full p-2 border rounded-md appearance-none pr-8 focus:ring-2 focus:ring-blue-500 transition"
              >
                <option value="">All Event Types</option>
                <option value="Anomaly">Anomaly</option>
                <option value="Security Alert">Security Alert</option>
              </select>
              <Filter className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" />
            </div>
          </div>
        </div>

        {/* Visualization Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Traffic Patterns */}
          <div className="bg-white shadow-md rounded-lg p-6">
            <div className="flex items-center mb-4">
              <TrendingUp className="mr-3 text-blue-600" />
              <h2 className="text-xl font-semibold text-gray-800">Traffic Patterns</h2>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trafficData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', borderRadius: '8px' }}
                  itemStyle={{ color: '#333' }}
                />
                <Legend />
                <Line type="monotone" dataKey="traffic" stroke="#3b82f6" strokeWidth={3} activeDot={{r: 8}} />
                <Line type="monotone" dataKey="anomalies" stroke="#ef4444" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Anomaly Trends */}
          <div className="bg-white shadow-md rounded-lg p-6">
            <div className="flex items-center mb-4">
              <Shield className="mr-3 text-red-600" />
              <h2 className="text-xl font-semibold text-gray-800">Anomaly Trends</h2>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trafficData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', borderRadius: '8px' }}
                  itemStyle={{ color: '#333' }}
                />
                <Line type="monotone" dataKey="anomalies" stroke="#ef4444" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Notifications Table */}
        <div className="bg-white shadow-md rounded-lg overflow-x-auto">
          <div className="flex items-center p-6 pb-0">
            <BarChart className="mr-3 text-green-600" />
            <h2 className="text-xl font-semibold text-gray-800">Blockchain Notifications</h2>
          </div>
          <table className="w-full">
            <thead>
              <tr className="bg-gray-100 border-b">
                <th className="p-4 text-left">Event Type</th>
                <th className="p-4 text-left">Description</th>
                <th className="p-4 text-left hidden md:table-cell">Timestamp</th>
                <th className="p-4 text-left hidden lg:table-cell">Evidence</th>
                <th className="p-4 text-left">Severity</th>
              </tr>
            </thead>
            <tbody>
              {filteredNotifications.map(notification => (
                <tr key={notification.id} className="border-b hover:bg-gray-50 transition">
                  <td className="p-4">
                    <div className="flex items-center">
                      {notification.eventType === 'Anomaly' && <AlertTriangle className="mr-2 text-yellow-500" />}
                      {notification.eventType}
                    </div>
                  </td>
                  <td className="p-4">{notification.description}</td>
                  <td className="p-4 hidden md:table-cell">{notification.timestamp}</td>
                  <td className="p-4 hidden lg:table-cell">{notification.evidence}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded-full text-xs text-white ${getSeverityColor(notification.severity)}`}>
                      {notification.severity}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default MonitoringDashboard;