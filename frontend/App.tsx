import React from 'react';
import { BrowserRouter, HashRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { runtimeConfig } from './config/runtime';

// Public pages
import Landing from './pages/public/Landing';
import ServicesPage from './pages/public/ServicesPage';
import SchedulePage from './pages/public/SchedulePage';
import Trainers from './pages/public/Trainers';
import OrgRegister from './pages/public/OrgRegister';
import { About, Blog, BlogPost, Privacy, Contact } from './pages/public/StaticPages';
import { PaymentSuccess, PaymentCancel } from './pages/public/PaymentPages';

// Auth pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';

// Protected client pages
import Dashboard from './pages/protected/Dashboard';
import Bookings from './pages/protected/Bookings';
import NewBooking from './pages/protected/NewBooking';
import Profile from './pages/protected/Profile';
import Shop from './pages/protected/Shop';
import Notifications from './pages/protected/Notifications';

// Instructor
import InstructorDashboard from './pages/protected/InstructorDashboard';

// Admin
import AdminDashboard from './pages/protected/AdminDashboard';
import AdminUsers from './pages/protected/AdminUsers';
import AdminClasses from './pages/protected/AdminClasses';

const App: React.FC = () => {
  const Router = runtimeConfig.routerMode === 'hash' ? HashRouter : BrowserRouter;

  return (
    <AuthProvider>
      <Router basename={runtimeConfig.appBasePath}>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
};

const AppRoutes: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#000', color: '#fff' }}>
        <div style={{ width: 40, height: 40, border: '3px solid #333', borderTop: '3px solid #10b981', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  return (
    <Routes>
      {/* Public */}
      <Route path="/" element={<Landing />} />
      <Route path="/services" element={<ServicesPage />} />
      <Route path="/schedule" element={<SchedulePage />} />
      <Route path="/trainers" element={<Trainers />} />
      <Route path="/corporate" element={<OrgRegister />} />
      <Route path="/about" element={<About />} />
      <Route path="/blog" element={<Blog />} />
      <Route path="/blog/:slug" element={<BlogPost />} />
      <Route path="/privacy" element={<Privacy />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/payment/success" element={<PaymentSuccess />} />
      <Route path="/payment/cancel" element={<PaymentCancel />} />

      {/* Auth */}
      <Route path="/login" element={user ? <Navigate to="/dashboard" replace /> : <Login />} />
      <Route path="/register" element={user ? <Navigate to="/dashboard" replace /> : <Register />} />

      {/* Protected client routes */}
      <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/bookings" element={<ProtectedRoute><Bookings /></ProtectedRoute>} />
      <Route path="/booking" element={<ProtectedRoute><NewBooking /></ProtectedRoute>} />
      <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
      <Route path="/shop" element={<ProtectedRoute><Shop /></ProtectedRoute>} />
      <Route path="/notifications" element={<ProtectedRoute><Notifications /></ProtectedRoute>} />

      {/* Instructor */}
      <Route path="/instructor" element={<ProtectedRoute><InstructorDashboard /></ProtectedRoute>} />

      {/* Admin routes */}
      <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
      <Route path="/admin/users" element={<AdminRoute><AdminUsers /></AdminRoute>} />
      <Route path="/admin/classes" element={<AdminRoute><AdminClasses /></AdminRoute>} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

interface RouteProps { children: React.ReactElement; }

const ProtectedRoute: React.FC<RouteProps> = ({ children }) => {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
};

const AdminRoute: React.FC<RouteProps> = ({ children }) => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  const isAdmin = user.role === 'admin' || user.isAdmin || user.isStaff;
  if (!isAdmin) return <Navigate to="/dashboard" replace />;
  return children;
};

export default App;
