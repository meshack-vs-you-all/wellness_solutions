import React, { useState, useEffect } from 'react';
import { Calendar, Clock, Users, Tag } from 'lucide-react';
import type { Class } from '../../types/class.types';
import { classService } from '../../services/class.service';
import { LoadingSpinner } from '../../components/common/LoadingSpinner';
import { Card, CardContent } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import BookingModal from '../../components/booking/BookingModal';

const Schedule: React.FC = () => {
  const [classes, setClasses] = useState<Class[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();
  const navigate = useNavigate();
  const [selectedClass, setSelectedClass] = useState<Class | null>(null);

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const data = await classService.getClasses();
        setClasses(data);
      } catch (err) {
        setError('Failed to load schedule. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchClasses();
  }, []);

  const handleBookClick = (cls: Class) => {
    if (!user) {
      navigate('/login');
    } else {
      setSelectedClass(cls);
    }
  };
  
  const handleCloseModal = () => {
    setSelectedClass(null);
  }

  const handleBookingConfirmed = () => {
    // Optionally refetch classes to update enrolled count, or update state optimistically
    setSelectedClass(null);
     navigate('/bookings');
  }

  if (loading) {
    return <div className="flex justify-center items-center h-64"><LoadingSpinner /></div>;
  }

  if (error) {
    return <div className="text-center text-red-500">{error}</div>;
  }

  return (
    <div className="px-2 sm:px-0">
      <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-6 sm:mb-8 text-center">Class Schedule</h1>
      <div className="space-y-4 sm:space-y-6">
        {classes.length > 0 ? (
          classes.map((cls) => (
            <Card key={cls.id} className="transition-shadow hover:shadow-lg dark:hover:shadow-primary/20">
              <CardContent className="flex flex-col sm:grid sm:grid-cols-4 gap-4 sm:items-center">
                <div className="sm:col-span-3">
                  <h2 className="text-xl sm:text-2xl font-semibold text-primary dark:text-primary-light">{cls.title}</h2>
                  <p className="text-sm sm:text-base text-neutral-600 dark:text-neutral-300 mt-1">{cls.description}</p>
                  <div className="flex flex-wrap items-center gap-x-3 sm:gap-x-4 gap-y-2 mt-3 sm:mt-4 text-xs sm:text-sm text-neutral-700 dark:text-neutral-400">
                    <span className="flex items-center"><Calendar size={14} className="mr-1 sm:mr-1.5" /> {new Date(cls.startTime).toLocaleDateString()}</span>
                    <span className="flex items-center"><Clock size={14} className="mr-1 sm:mr-1.5" /> {new Date(cls.startTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - {new Date(cls.endTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                    <span className="flex items-center"><Users size={14} className="mr-1 sm:mr-1.5" /> {cls.enrolledCount} / {cls.capacity}</span>
                    <span className="flex items-center capitalize"><Tag size={14} className="mr-1 sm:mr-1.5" />{cls.level}</span>
                  </div>
                </div>
                <div className="mt-4 sm:mt-0 sm:text-right">
                  <Button 
                    onClick={() => handleBookClick(cls)} 
                    disabled={cls.enrolledCount >= cls.capacity}
                    className="w-full sm:w-auto"
                  >
                    {cls.enrolledCount >= cls.capacity ? 'Class Full' : 'Book Now'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <p className="text-center text-neutral-500 dark:text-neutral-400">No classes available at the moment.</p>
        )}
      </div>
      {selectedClass && (
        <BookingModal 
          classToBook={selectedClass} 
          onClose={handleCloseModal}
          onBookingConfirmed={handleBookingConfirmed}
        />
      )}
    </div>
  );
};

export default Schedule;