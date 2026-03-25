import api from './api';
import type { Booking } from '../types/booking.types';

// Create a new booking for a class
const createBooking = async (classId: number): Promise<Booking> => {
  const response = await api.post<Booking>('/api/bookings/', { class_id: classId });
  return response.data;
};

// Get all bookings for the current user
const getUserBookings = async (): Promise<Booking[]> => {
  const response = await api.get<Booking[]>('/api/users/me/bookings/');
  return response.data;
};

// Get a specific booking by ID
const getBooking = async (bookingId: number): Promise<Booking> => {
  const response = await api.get<Booking>(`/api/bookings/${bookingId}/`);
  return response.data;
};

// Cancel a booking
const cancelBooking = async (bookingId: number): Promise<void> => {
  await api.delete(`/api/bookings/${bookingId}/`);
};

// Update booking status (if needed)
const updateBookingStatus = async (bookingId: number, status: string): Promise<Booking> => {
  const response = await api.patch<Booking>(`/api/bookings/${bookingId}/`, { status });
  return response.data;
};

export const bookingService = {
  createBooking,
  getUserBookings,
  getBooking,
  cancelBooking,
  updateBookingStatus,
};
