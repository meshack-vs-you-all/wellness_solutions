import React, { useState, useEffect } from 'react';
import type { Booking } from '../../types/booking.types';
import { bookingService } from '../../services/booking.service';
import { useAuth } from '../../contexts/AuthContext';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { Card, CardContent, CardHeader } from '../common/Card';
import { Calendar, CheckCircle, Clock } from 'lucide-react';
import { Button } from '../common/Button';
import { Link } from 'react-router-dom';

const UserDashboard: React.FC = () => {
  const { user } = useAuth();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBookings = async () => {
      if (user) {
        try {
          const data = await bookingService.getUserBookings();
          // Filter for upcoming bookings
          const upcoming = data.filter(b => new Date(b.classStartTime) > new Date());
          setBookings(upcoming);
        } catch (error) {
          console.error("Failed to fetch bookings", error);
        } finally {
          setLoading(false);
        }
      }
    };
    fetchBookings();
  }, [user]);

  if (loading) {
    return <div className="flex justify-center items-center h-48"><LoadingSpinner /></div>;
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8">
      {/* Upcoming Bookings */}
      <div className="lg:col-span-2">
        <h2 className="text-xl sm:text-2xl font-semibold mb-3 sm:mb-4">Upcoming Bookings</h2>
        <Card>
          <CardContent>
            {bookings.length > 0 ? (
              <ul className="divide-y divide-neutral-200 dark:divide-neutral-700">
                {bookings.map(booking => (
                  <li key={booking.id} className="py-4 flex justify-between items-center">
                    <div>
                      <p className="font-semibold text-primary dark:text-primary-light">{booking.classTitle}</p>
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 flex items-center mt-1">
                        <Calendar size={14} className="mr-2" />
                        {new Date(booking.classStartTime).toLocaleDateString()}
                        <Clock size={14} className="ml-4 mr-2" />
                        {new Date(booking.classStartTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                     <Link to="/bookings">
                        <Button variant="outline" size="sm">Manage</Button>
                     </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-center py-8">
                <p className="text-neutral-500 dark:text-neutral-400 mb-4">You have no upcoming bookings.</p>
                <Link to="/schedule">
                  <Button>Book a Class</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Membership Status */}
      <div>
        <h2 className="text-xl sm:text-2xl font-semibold mb-3 sm:mb-4">Membership</h2>
        <Card className="bg-gradient-to-br from-primary to-blue-600 text-white">
          <CardHeader className="border-b border-white/20">
            <p className="text-lg font-bold capitalize">{user?.membershipType} Plan</p>
          </CardHeader>
          <CardContent>
            {user?.membershipType !== 'none' ? (
              <div className="space-y-2">
                 <p className="flex items-center"><CheckCircle size={16} className="mr-2" /> Access to all classes</p>
                 <p className="flex items-center"><CheckCircle size={16} className="mr-2" /> Free towel service</p>
                <p className="mt-4 text-sm opacity-90">
                  Expires on: {user?.membershipExpiry ? new Date(user.membershipExpiry).toLocaleDateString() : 'N/A'}
                </p>
              </div>
            ) : (
              <div>
                <p>You are not currently on a plan.</p>
                 <Link to="/pricing">
                     <Button variant="outline" className="mt-4 bg-white text-primary hover:bg-neutral-100 border-transparent">Explore Plans</Button>
                 </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default UserDashboard;