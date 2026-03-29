import api from './api';
import type { User } from '../types/user.types';
import type { Booking } from '../types/booking.types';
import type { AnalyticsData } from '../types/api.types';
import type { Class } from '../types/class.types';

// For Admin
const getAllUsers = async (): Promise<User[]> => {
  const response = await api.get<User[]>('/users/');
  return response.data;
};

const getAnalytics = async (): Promise<AnalyticsData> => {
  const response = await api.get<AnalyticsData>('/analytics/');
  return response.data;
};

// For logged-in user
const getUserBookings = async (): Promise<Booking[]> => {
  const response = await api.get<Booking[]>('/users/me/bookings/');
  return response.data;
};

// For Instructor
const getInstructorClasses = async (): Promise<Class[]> => {
  const response = await api.get<Class[]>('/instructors/me/classes/');
  return response.data;
};


export const userService = {
  getAllUsers,
  getAnalytics,
  getUserBookings,
  getInstructorClasses
};
