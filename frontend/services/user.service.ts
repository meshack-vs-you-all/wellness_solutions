import api from './api';
import type { User } from '../types/user.types';
import type { Booking } from '../types/booking.types';
import type { AnalyticsData } from '../types/api.types';
import type { Class } from '../types/class.types';

// For Admin
const getAllUsers = async (): Promise<User[]> => {
  const response = await api.get<User[]>('/api/users/');
  return response.data;
};

const getAnalytics = async (): Promise<AnalyticsData> => {
  // NOTE: Endpoint '/api/analytics/' is an assumption.
  const response = await api.get<AnalyticsData>('/api/analytics/');
  return response.data;
};

// For logged-in user
const getUserBookings = async (): Promise<Booking[]> => {
  // NOTE: Endpoint '/api/users/me/bookings/' is an assumption.
  const response = await api.get<Booking[]>('/api/users/me/bookings/');
  return response.data;
};

// For Instructor
const getInstructorClasses = async (): Promise<Class[]> => {
  // NOTE: Endpoint '/api/instructors/me/classes/' is an assumption.
  const response = await api.get<Class[]>('/api/instructors/me/classes/');
  return response.data;
};


export const userService = {
  getAllUsers,
  getAnalytics,
  getUserBookings,
  getInstructorClasses
};
