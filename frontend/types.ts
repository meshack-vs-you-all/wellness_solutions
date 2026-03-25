
export interface User {
  id: number;
  email: string;
  name: string;
  phone?: string;
  membershipType: 'basic' | 'premium' | 'unlimited' | 'none';
  membershipExpiry?: string; // ISO Date string
  credits?: number;
  role: 'member' | 'instructor' | 'admin';
}

export interface Class {
  id: number;
  title: string;
  instructorId: number;
  instructorName: string;
  startTime: string; // ISO Date string
  endTime: string; // ISO Date string
  capacity: number;
  enrolledCount: number;
  type: 'wellness' | 'yoga' | 'pilates' | 'recovery';
  level: 'beginner' | 'intermediate' | 'advanced';
  description: string;
  price?: number;
}

export interface Booking {
  id: number;
  userId: number;
  classId: number;
  classTitle: string;
  classStartTime: string; // ISO Date string
  status: 'confirmed' | 'waitlist' | 'cancelled';
  bookedAt: string; // ISO Date string;
}

export interface Membership {
  id: number;
  type: 'Basic Monthly' | 'Premium Quarterly' | 'Unlimited Annual';
  price: number;
  duration: 'monthly' | 'quarterly' | 'annual';
  benefits: string[];
  classCredits?: number;
}

export interface AnalyticsData {
  revenue: { month: string; total: number }[];
  attendance: { month: string; total: number }[];
  newMembers: { month: string; count: number }[];
}
