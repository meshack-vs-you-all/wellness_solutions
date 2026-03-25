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
