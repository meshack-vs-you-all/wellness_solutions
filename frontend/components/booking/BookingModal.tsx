import React, { useState } from 'react';
import { X } from 'lucide-react';
import { Button } from '../common/Button';
import { Card, CardContent, CardHeader, CardFooter } from '../common/Card';
import { bookingService } from '../../services/booking.service';
import type { Class } from '../../types/class.types';

interface BookingModalProps {
  classToBook: Class;
  onClose: () => void;
  onBookingConfirmed: () => void;
}

const BookingModal: React.FC<BookingModalProps> = ({ classToBook, onClose, onBookingConfirmed }) => {
  const [isBooking, setIsBooking] = useState(false);
  const [error, setError] = useState('');

  const handleConfirmBooking = async () => {
    setIsBooking(true);
    setError('');
    try {
      await bookingService.createBooking(classToBook.id);
      onBookingConfirmed();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to book class. It might be full or you may have a scheduling conflict.');
      console.error(err);
    } finally {
      setIsBooking(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50 p-4" onClick={onClose}>
      <div className="relative w-full max-w-lg" onClick={(e) => e.stopPropagation()}>
        <Card>
          <CardHeader className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Confirm Your Booking</h2>
            <button onClick={onClose} className="text-neutral-500 hover:text-neutral-800 dark:hover:text-neutral-200">
              <X size={24} />
            </button>
          </CardHeader>
          <CardContent className="space-y-4">
            {error && <p className="bg-red-100 text-red-700 p-3 rounded-md">{error}</p>}
            <div>
              <p className="text-sm font-medium text-neutral-500 dark:text-neutral-400">CLASS</p>
              <p className="text-lg font-semibold text-primary dark:text-primary-light">{classToBook.title}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-neutral-500 dark:text-neutral-400">INSTRUCTOR</p>
              <p className="text-lg">{classToBook.instructorName}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-neutral-500 dark:text-neutral-400">DATE & TIME</p>
              <p className="text-lg">
                {new Date(classToBook.startTime).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                <br />
                {new Date(classToBook.startTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - {new Date(classToBook.endTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </CardContent>
          <CardFooter className="flex justify-end space-x-4">
            <Button variant="ghost" onClick={onClose} disabled={isBooking}>Cancel</Button>
            <Button onClick={handleConfirmBooking} disabled={isBooking}>
              {isBooking ? 'Booking...' : 'Confirm & Book'}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default BookingModal;