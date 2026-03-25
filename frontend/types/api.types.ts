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
