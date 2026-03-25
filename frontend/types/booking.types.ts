export interface Booking {
  id: number;
  userId: number;
  classId: number;
  classTitle: string;
  classStartTime: string; // ISO Date string
  status: 'confirmed' | 'waitlist' | 'cancelled';
  bookedAt: string; // ISO Date string;
}
