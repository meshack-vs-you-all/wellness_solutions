export interface User {
  id: number;
  email: string;
  name: string;
  phone?: string;
  membershipType: 'basic' | 'premium' | 'unlimited' | 'none';
  membershipExpiry?: string;
  credits?: number;
  role: 'member' | 'instructor' | 'admin';
  isAdmin?: boolean;
  isStaff?: boolean;
}
