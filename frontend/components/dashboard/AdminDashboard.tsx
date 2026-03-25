import React, { useState, useEffect } from 'react';
import type { User } from '../../types/user.types';
import type { AnalyticsData } from '../../types/api.types';
import { userService } from '../../services/user.service';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { Card, CardContent, CardHeader } from '../common/Card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { useTheme } from '../../contexts/ThemeContext';

const AdminDashboard: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const { theme } = useTheme();

  const chartTextColor = theme === 'dark' ? '#d1d5db' : '#374151'; // neutral-300 or neutral-700
  const chartGridColor = theme === 'dark' ? '#4b5563' : '#e5e7eb'; // neutral-600 or neutral-200

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [usersData, analyticsData] = await Promise.all([
          userService.getAllUsers(),
          userService.getAnalytics()
        ]);
        setUsers(usersData);
        setAnalytics(analyticsData);
      } catch (error) {
        console.error("Failed to fetch admin data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-64"><LoadingSpinner /></div>;
  }

  return (
    <div className="space-y-8">
      {/* Analytics Section */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Studio Analytics</h2>
        <div className="grid md:grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <CardHeader><h3 className="font-semibold">Monthly Revenue</h3></CardHeader>
            <CardContent>
              {analytics && (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={analytics.revenue}>
                    <CartesianGrid strokeDasharray="3 3" stroke={chartGridColor}/>
                    <XAxis dataKey="month" stroke={chartTextColor} />
                    <YAxis stroke={chartTextColor} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff', border: `1px solid ${chartGridColor}`}}
                      labelStyle={{ color: chartTextColor }} 
                    />
                    <Legend wrapperStyle={{ color: chartTextColor }} />
                    <Bar dataKey="total" fill="#4A90E2" name="Revenue ($)" />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>
          <Card>
            <CardHeader><h3 className="font-semibold">New Members</h3></CardHeader>
            <CardContent>
              {analytics && (
                <ResponsiveContainer width="100%" height={300}>
                   <LineChart data={analytics.newMembers}>
                    <CartesianGrid strokeDasharray="3 3" stroke={chartGridColor}/>
                    <XAxis dataKey="month" stroke={chartTextColor} />
                    <YAxis stroke={chartTextColor} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff', border: `1px solid ${chartGridColor}`}}
                      labelStyle={{ color: chartTextColor }} 
                    />
                    <Legend wrapperStyle={{ color: chartTextColor }} />
                    <Line type="monotone" dataKey="count" stroke="#50C878" name="New Members" />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>
        </div>
      </section>

      {/* User Management Section */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">User Management</h2>
        <Card>
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left text-neutral-500 dark:text-neutral-400">
                    <thead className="text-xs text-neutral-700 uppercase bg-neutral-50 dark:bg-neutral-700 dark:text-neutral-300">
                        <tr>
                            <th scope="col" className="px-6 py-3">Name</th>
                            <th scope="col" className="px-6 py-3">Email</th>
                            <th scope="col" className="px-6 py-3">Role</th>
                            <th scope="col" className="px-6 py-3">Membership</th>
                            <th scope="col" className="px-6 py-3">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <tr key={user.id} className="bg-white border-b dark:bg-neutral-800 dark:border-neutral-700 hover:bg-neutral-50 dark:hover:bg-neutral-600">
                                <td className="px-6 py-4 font-medium text-neutral-900 dark:text-white whitespace-nowrap">{user.name}</td>
                                <td className="px-6 py-4">{user.email}</td>
                                <td className="px-6 py-4 capitalize">{user.role}</td>
                                <td className="px-6 py-4 capitalize">{user.membershipType}</td>
                                <td className="px-6 py-4">
                                    <a href="#" className="font-medium text-primary hover:underline dark:text-primary-light">Edit</a>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Card>
      </section>
    </div>
  );
};

export default AdminDashboard;