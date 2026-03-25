# Build a Modern Frontend for Wellness Solutions - Fitness & Stretching Studio Management System

## Project Overview
Create a modern, responsive React frontend application for Wellness Solutions - a comprehensive web application for managing bookings, payments, and user accounts at a stretching and fitness studio. The frontend should be professional, clean, and optimized for both desktop and mobile devices.

## Design Theme & Branding
- **Business Type**: Premium stretching and fitness studio
- **Target Audience**: Health-conscious individuals seeking flexibility training, recovery, and wellness services
- **Visual Style**: 
  - Clean, modern, and minimalist design
  - Calming color palette with blues, whites, and accent colors (suggested: #4A90E2 primary, #7FD5EA secondary, #50C878 success)
  - Professional typography (suggested: Inter or Poppins for headings, Open Sans for body)
  - Smooth animations and transitions
  - High-quality imagery of stretching, yoga, and fitness activities
  - Ample white space for breathing room

## Tech Stack Requirements
```json
{
  "framework": "React 18+ with TypeScript",
  "styling": "Tailwind CSS + Shadcn/ui components",
  "state": "Zustand or Redux Toolkit",
  "routing": "React Router v6",
  "forms": "React Hook Form + Zod validation",
  "api": "Axios or TanStack Query",
  "auth": "Token-based with localStorage/sessionStorage",
  "calendar": "FullCalendar or react-big-calendar",
  "payments": "Stripe integration ready",
  "charts": "Recharts for analytics",
  "animations": "Framer Motion",
  "icons": "Lucide React",
  "date": "date-fns",
  "testing": "Jest + React Testing Library"
}
```

## Backend API Endpoints (Django REST Framework)

### Authentication
- `POST /api/auth-token/` - Login (username: email, password)
- `POST /api/auth/logout/` - Logout
- `POST /accounts/signup/` - Register new user
- `POST /accounts/password/reset/` - Password reset
- `POST /accounts/password/change/` - Change password

### User Management
- `GET /api/users/` - List all users (admin only)
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user profile
- `GET /api/users/me/` - Get current user info

### API Documentation
- `GET /api/schema/` - OpenAPI schema
- `GET /api/docs/` - Swagger documentation

## Core Features to Implement

### 1. Public Pages (No Auth Required)
- **Landing Page**: Hero section, services overview, testimonials, pricing, CTA
- **Services Page**: List of stretching/fitness services with descriptions
- **Pricing Page**: Membership tiers, drop-in rates, package deals
- **Schedule Page**: Public view of class schedule
- **About Page**: Studio information, instructors, philosophy
- **Contact Page**: Contact form, location map, hours

### 2. Authentication System
- **Login Page**: Email/password with "Remember me"
- **Register Page**: Full registration with email verification
- **Forgot Password**: Password reset flow
- **Email Verification**: Verify email after registration

### 3. User Dashboard (Authenticated)
```typescript
interface UserDashboard {
  upcomingBookings: Booking[];
  membershipStatus: MembershipInfo;
  recentActivity: Activity[];
  accountBalance: number;
  quickActions: QuickAction[];
}
```

### 4. Booking System
- **Class Schedule View**: Calendar/list view of available classes
- **Booking Flow**: Select class → Choose spot → Confirm → Payment
- **My Bookings**: View, cancel, reschedule bookings
- **Waitlist**: Join waitlist for full classes
- **Booking Rules**: Cancellation policy, booking limits

### 5. Membership Management
- **Membership Types**: Monthly, quarterly, annual, drop-in packages
- **Purchase/Upgrade**: Select plan → Payment → Activation
- **Membership Status**: Current plan, expiry, benefits used
- **Auto-renewal Settings**: Manage subscription

### 6. Payment Integration
- **Payment Methods**: Add/remove cards (Stripe)
- **Payment History**: Invoices, receipts
- **Account Balance**: Credits, outstanding payments
- **Checkout Flow**: Secure payment for bookings/memberships

### 7. User Profile
- **Profile Information**: Name, email, phone, emergency contact
- **Health Information**: Injuries, limitations (private)
- **Preferences**: Notification settings, favorite instructors
- **Goals**: Fitness goals tracking

### 8. Class Management (Instructor View)
- **Instructor Dashboard**: Upcoming classes, attendance
- **Class Check-in**: Mark attendance
- **Class Notes**: Add notes for students

### 9. Admin Panel (Admin Users)
- **User Management**: View, edit, deactivate users
- **Class Management**: Create, edit, cancel classes
- **Instructor Management**: Assign instructors to classes
- **Reports**: Revenue, attendance, member analytics
- **Settings**: Studio settings, pricing, policies

## Component Structure
```
src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   ├── ProtectedRoute.tsx
│   │   └── AuthProvider.tsx
│   ├── booking/
│   │   ├── ClassSchedule.tsx
│   │   ├── BookingModal.tsx
│   │   ├── BookingCard.tsx
│   │   └── BookingCalendar.tsx
│   ├── dashboard/
│   │   ├── UserDashboard.tsx
│   │   ├── InstructorDashboard.tsx
│   │   └── AdminDashboard.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Sidebar.tsx
│   │   └── MobileNav.tsx
│   ├── membership/
│   │   ├── MembershipPlans.tsx
│   │   ├── PurchaseFlow.tsx
│   │   └── MembershipStatus.tsx
│   ├── payment/
│   │   ├── PaymentForm.tsx
│   │   ├── PaymentHistory.tsx
│   │   └── StripeCheckout.tsx
│   └── common/
│       ├── Button.tsx
│       ├── Card.tsx
│       ├── Modal.tsx
│       ├── Toast.tsx
│       └── LoadingSpinner.tsx
├── pages/
│   ├── public/
│   │   ├── Landing.tsx
│   │   ├── Services.tsx
│   │   ├── Pricing.tsx
│   │   └── Contact.tsx
│   ├── auth/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   └── ForgotPassword.tsx
│   └── protected/
│       ├── Dashboard.tsx
│       ├── Bookings.tsx
│       ├── Profile.tsx
│       └── Settings.tsx
├── services/
│   ├── api.ts
│   ├── auth.service.ts
│   ├── booking.service.ts
│   ├── user.service.ts
│   └── payment.service.ts
├── store/
│   ├── authStore.ts
│   ├── bookingStore.ts
│   └── userStore.ts
├── utils/
│   ├── constants.ts
│   ├── helpers.ts
│   └── validators.ts
└── types/
    ├── user.types.ts
    ├── booking.types.ts
    └── api.types.ts
```

## API Integration Example
```typescript
// services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// services/auth.service.ts
export const authService = {
  async login(email: string, password: string) {
    const response = await api.post('/api/auth-token/', {
      username: email, // Django expects username field
      password,
    });
    const { token } = response.data;
    localStorage.setItem('authToken', token);
    return token;
  },

  async getCurrentUser() {
    const response = await api.get('/api/users/me/');
    return response.data;
  },

  logout() {
    localStorage.removeItem('authToken');
  },
};
```

## Key UI/UX Requirements

### Mobile Responsiveness
- Full mobile optimization with touch gestures
- Bottom navigation for mobile
- Swipeable calendar views
- One-thumb reachability for CTAs

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- High contrast mode option

### Performance
- Lazy loading for images
- Code splitting by route
- Optimistic UI updates
- PWA capabilities with offline support

### User Experience
- Intuitive booking flow (max 3 clicks)
- Clear visual feedback for all actions
- Smart defaults (remember preferences)
- Helpful empty states
- Progressive disclosure for complex forms

## Sample Data Models

```typescript
interface User {
  id: number;
  email: string;
  name: string;
  phone?: string;
  membershipType?: 'basic' | 'premium' | 'unlimited';
  membershipExpiry?: Date;
  credits?: number;
  isInstructor?: boolean;
  isAdmin?: boolean;
}

interface Class {
  id: number;
  title: string;
  instructor: User;
  startTime: Date;
  endTime: Date;
  capacity: number;
  enrolledCount: number;
  type: 'wellness' | 'yoga' | 'pilates' | 'recovery';
  level: 'beginner' | 'intermediate' | 'advanced';
  description: string;
  price?: number;
}

interface Booking {
  id: number;
  user: User;
  class: Class;
  status: 'confirmed' | 'waitlist' | 'cancelled';
  bookedAt: Date;
  attendanceMarked?: boolean;
}

interface Membership {
  id: number;
  type: string;
  price: number;
  duration: 'monthly' | 'quarterly' | 'annual';
  benefits: string[];
  classCredits?: number;
}
```

## Environment Variables
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_STRIPE_PUBLIC_KEY=pk_test_...
REACT_APP_GOOGLE_MAPS_KEY=...
REACT_APP_SENTRY_DSN=...
```

## Development Workflow

1. **Setup**: Create React app with TypeScript, install dependencies
2. **Authentication**: Implement auth flow first (login, register, token management)
3. **Layout**: Create responsive layout with navigation
4. **Core Features**: Build booking system, dashboard, profile
5. **Payments**: Integrate Stripe for payments
6. **Testing**: Write tests for critical flows
7. **Optimization**: Performance optimization, PWA setup
8. **Deployment**: Build and deploy to Vercel/Netlify

## Additional Features (Phase 2)
- **Mobile App**: React Native version
- **Notifications**: Push notifications for class reminders
- **Social Features**: Friend invites, social sharing
- **Rewards Program**: Points, referrals, achievements
- **Analytics Dashboard**: Business metrics for admin
- **Multi-language Support**: i18n implementation
- **Virtual Classes**: Video streaming integration
- **Wearable Integration**: Apple Watch, Fitbit sync

## Testing Credentials
- Admin: admin@example.com / admin123
- Test endpoints first using the token from `/api/auth-token/`

## IMPORTANT: Start by creating a simple login page that connects to the backend at http://localhost:8000, then progressively build out features once authentication is working.

Generate the complete React application with all the components, services, and features described above. Focus on creating a production-ready, professional fitness studio management system frontend.
