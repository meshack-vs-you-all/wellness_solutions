
import type { User, Class, Booking, AnalyticsData } from '../types';
import { MOCK_USERS, MOCK_CLASSES, MOCK_BOOKINGS, MOCK_ANALYTICS } from './mockData';

// Helper to simulate network delay
const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

// This service would use fetch() to an actual API in a real application.
// For now, it returns mock data.

export const apiService = {
  async getClasses(): Promise<Class[]> {
    await delay(500);
    console.log("API: Fetching all classes");
    return MOCK_CLASSES;
  },

  async getUserBookings(userId: number): Promise<Booking[]> {
    await delay(500);
    console.log(`API: Fetching bookings for user ${userId}`);
    return MOCK_BOOKINGS.filter(b => b.userId === userId);
  },

  // Admin-only functions
  async getAllUsers(): Promise<User[]> {
    await delay(500);
    console.log("API: Fetching all users (admin)");
    return MOCK_USERS;
  },

  async getAnalytics(): Promise<AnalyticsData> {
    await delay(800);
    console.log("API: Fetching analytics data (admin)");
    return MOCK_ANALYTICS;
  }
};
