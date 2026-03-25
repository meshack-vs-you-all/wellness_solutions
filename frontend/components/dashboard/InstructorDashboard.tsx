import React, { useState, useEffect } from 'react';
import type { Class } from '../../types/class.types';
import { userService } from '../../services/user.service';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { Card, CardContent, CardHeader } from '../common/Card';
import { Calendar, Clock, Users } from 'lucide-react';

const InstructorDashboard: React.FC = () => {
  const [classes, setClasses] = useState<Class[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInstructorClasses = async () => {
      try {
        const data = await userService.getInstructorClasses();
        const upcoming = data.filter(c => new Date(c.startTime) > new Date());
        setClasses(upcoming.sort((a,b) => new Date(a.startTime).getTime() - new Date(b.startTime).getTime()));
      } catch (err) {
        setError('Could not load your classes.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchInstructorClasses();
  }, []);

  if (loading) {
    return <div className="flex justify-center"><LoadingSpinner /></div>;
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Your Upcoming Classes</h2>
      {classes.length > 0 ? (
        <div className="space-y-4">
          {classes.map(cls => (
            <Card key={cls.id}>
              <CardContent>
                <h3 className="text-xl font-bold text-primary">{cls.title}</h3>
                <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-2 text-sm text-neutral-600">
                  <span className="flex items-center"><Calendar size={14} className="mr-1.5" />{new Date(cls.startTime).toLocaleDateString()}</span>
                  <span className="flex items-center"><Clock size={14} className="mr-1.5" />{new Date(cls.startTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                  <span className="flex items-center"><Users size={14} className="mr-1.5" />{cls.enrolledCount} / {cls.capacity} booked</span>
                </div>
                <div className="mt-4">
                  {/* In a real app, this would link to a class management view */}
                  <a href="#" className="text-sm font-semibold text-primary hover:underline">View Roster</a>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <p>You have no upcoming classes scheduled.</p>
      )}
    </div>
  );
};

export default InstructorDashboard;
