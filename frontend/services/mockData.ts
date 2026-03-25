
import type { User, Class, Booking, AnalyticsData } from '../types';

export const MOCK_USERS: User[] = [
  { id: 1, name: 'Admin User', email: 'admin@example.com', role: 'admin', membershipType: 'unlimited', membershipExpiry: '2025-12-31T23:59:59Z' },
  { id: 2, name: 'Member User', email: 'member@example.com', role: 'member', membershipType: 'premium', membershipExpiry: '2024-09-30T23:59:59Z' },
  { id: 3, name: 'Instructor User', email: 'instructor@example.com', role: 'instructor', membershipType: 'none' },
  { id: 4, name: 'Jane Doe', email: 'jane.doe@example.com', role: 'member', membershipType: 'basic', membershipExpiry: '2024-08-15T23:59:59Z' },
  { id: 5, name: 'John Smith', email: 'john.smith@example.com', role: 'member', membershipType: 'none' },
];

export const MOCK_CLASSES: Class[] = [
  {
    id: 1,
    title: 'Morning Flow Yoga',
    instructorId: 3,
    instructorName: 'Instructor User',
    startTime: new Date(Date.now() + 1 * 24 * 60 * 60 * 1000).toISOString(),
    endTime: new Date(Date.now() + (1 * 24 * 60 * 60 * 1000) + (60 * 60 * 1000)).toISOString(),
    capacity: 20,
    enrolledCount: 15,
    type: 'yoga',
    level: 'beginner',
    description: 'Start your day with an energizing yet calming yoga flow suitable for all levels.'
  },
  {
    id: 2,
    title: 'Deep Stretch & Recovery',
    instructorId: 3,
    instructorName: 'Instructor User',
    startTime: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(),
    endTime: new Date(Date.now() + (2 * 24 * 60 * 60 * 1000) + (60 * 60 * 1000)).toISOString(),
    capacity: 15,
    enrolledCount: 12,
    type: 'wellness',
    level: 'intermediate',
    description: 'Focus on releasing tension in muscles and improving flexibility with targeted stretches.'
  },
  {
    id: 3,
    title: 'Core Pilates',
    instructorId: 3,
    instructorName: 'Instructor User',
    startTime: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
    endTime: new Date(Date.now() + (3 * 24 * 60 * 60 * 1000) + (50 * 60 * 1000)).toISOString(),
    capacity: 18,
    enrolledCount: 18,
    type: 'pilates',
    level: 'advanced',
    description: 'Challenge your core strength and stability with this dynamic pilates class.'
  },
];

export const MOCK_BOOKINGS: Booking[] = [
  {
    id: 101,
    userId: 2,
    classId: 1,
    classTitle: 'Morning Flow Yoga',
    classStartTime: MOCK_CLASSES[0].startTime,
    status: 'confirmed',
    bookedAt: new Date().toISOString(),
  },
  {
    id: 102,
    userId: 2,
    classId: 2,
    classTitle: 'Deep Stretch & Recovery',
    classStartTime: MOCK_CLASSES[1].startTime,
    status: 'confirmed',
    bookedAt: new Date().toISOString(),
  },
];

export const MOCK_ANALYTICS: AnalyticsData = {
  revenue: [
    { month: 'Jan', total: 4500 },
    { month: 'Feb', total: 4800 },
    { month: 'Mar', total: 5200 },
    { month: 'Apr', total: 5100 },
    { month: 'May', total: 5500 },
    { month: 'Jun', total: 6000 },
  ],
  attendance: [
    { month: 'Jan', total: 320 },
    { month: 'Feb', total: 350 },
    { month: 'Mar', total: 400 },
    { month: 'Apr', total: 390 },
    { month: 'May', total: 420 },
    { month: 'Jun', total: 450 },
  ],
  newMembers: [
    { month: 'Jan', count: 15 },
    { month: 'Feb', count: 18 },
    { month: 'Mar', count: 22 },
    { month: 'Apr', count: 20 },
    { month: 'May', count: 25 },
    { month: 'Jun', count: 28 },
  ]
};
