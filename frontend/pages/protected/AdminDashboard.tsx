import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { NavBar } from './Dashboard';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

interface AnalyticsData {
  totalUsers: number;
  totalBookings: number;
  totalRevenue: number;
  activeClasses: number;
  newUsersThisMonth: number;
  bookingsThisMonth: number;
  revenueThisMonth: number;
  growthRate: number;
}

export default function AdminDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Role-based redirection
    if (user && !(user.role === 'admin' || user.isAdmin || user.isStaff)) {
      navigate('/dashboard');
      return;
    }

    api.get('/analytics/').then(res => setData(res.data)).catch(() => {
      setError('Could not load analytics. Make sure you have admin access.');
    }).finally(() => setLoading(false));
  }, [user, navigate]);

  const StatCard = ({ label, value, sub, color }: { label: string; value: string | number; sub?: string; color: string }) => (
    <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: '28px 24px' }}>
      <div style={{ color: '#888', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 12 }}>{label}</div>
      <div style={{ fontSize: '2.5rem', fontWeight: 800, color, marginBottom: sub ? 6 : 0 }}>{value}</div>
      {sub && <div style={{ color: '#555', fontSize: '0.9rem' }}>{sub}</div>}
    </div>
  );

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ marginBottom: 48 }}>
          <div style={{ color: 'var(--brand-primary)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 8 }}>Admin Panel</div>
          <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.8rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: 0 }}>Studio Analytics</h1>
        </div>

        {error && (
          <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 16, padding: '20px', marginBottom: 40, color: '#fca5a5' }}>{error}</div>
        )}

        {loading ? (
          <div style={{ textAlign: 'center', color: '#555', padding: '80px 0' }}>Loading analytics...</div>
        ) : data && (
          <>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 20, marginBottom: 40 }}>
              <StatCard label="Total Users" value={data.totalUsers.toLocaleString()} sub={`+${data.newUsersThisMonth} this month`} color="var(--brand-primary)" />
              <StatCard label="Total Bookings" value={data.totalBookings.toLocaleString()} sub={`+${data.bookingsThisMonth} this month`} color="#3b82f6" />
              <StatCard label="Total Revenue" value={`$${data.totalRevenue.toFixed(0)}`} sub={`$${data.revenueThisMonth.toFixed(0)} this month`} color="#f59e0b" />
              <StatCard label="Active Classes" value={data.activeClasses} sub="Upcoming available slots" color="#8b5cf6" />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 20 }}>
              <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: 32 }}>
                <h3 style={{ fontWeight: 700, marginBottom: 24, color: '#fff' }}>Growth Rate</h3>
                <div style={{ fontSize: '4rem', fontWeight: 800, color: 'var(--brand-primary)' }}>{data.growthRate}%</div>
                <div style={{ color: '#888', marginTop: 8 }}>Month-over-month growth</div>
                <div style={{ marginTop: 24, background: 'var(--surface-black)', borderRadius: 12, height: 8, overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${Math.min(data.growthRate, 100)}%`, background: 'linear-gradient(90deg, var(--brand-primary), var(--brand-secondary))', borderRadius: 12, transition: 'width 1s ease' }} />
                </div>
              </div>

              <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: 32 }}>
                <h3 style={{ fontWeight: 700, marginBottom: 20, color: '#fff' }}>Quick Reports</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  <button onClick={() => alert('Opening Studio Broadcast Tool (Email + In-App)...')} style={{ background: 'rgba(239,68,68,0.1)', color: '#fca5a5', border: '1px solid rgba(239,68,68,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left' }}>
                    📢 Send Studio-wide Announcement
                  </button>
                  <button onClick={() => alert('Generating Weekly Business Report (PDF)...')} style={{ background: 'rgba(15,173,182,0.1)', color: 'var(--brand-primary)', border: '1px solid rgba(15,173,182,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left' }}>
                    📄 Generate Weekly Performance (PDF)
                  </button>
                  <button onClick={() => {
                    const token = localStorage.getItem('authToken');
                    window.open(`${api.defaults.baseURL?.replace('/api', '')}/api/admin/users/export/csv/?token=${token}`, '_blank');
                  }} style={{ background: 'rgba(59,130,246,0.1)', color: '#3b82f6', border: '1px solid rgba(59,130,246,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left' }}>
                    📊 Export User Directory (CSV)
                  </button>
                  <button onClick={() => {
                    const token = localStorage.getItem('authToken');
                    window.open(`${api.defaults.baseURL?.replace('/api', '')}/api/calendar/export/?token=${token}`, '_blank');
                  }} style={{ background: 'rgba(139,92,246,0.1)', color: '#8b5cf6', border: '1px solid rgba(139,92,246,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left' }}>
                    📅 Sync Master Calendar (iCal)
                  </button>
                </div>
                <div style={{ marginTop: 24, padding: '16px', background: 'var(--surface-black)', borderRadius: 12, border: '1px solid #222' }}>
                  <div style={{ fontSize: '0.8rem', color: '#555', marginBottom: 4, textTransform: 'uppercase' }}>System Status</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--brand-primary)', fontWeight: 600, fontSize: '0.9rem' }}>
                    <div style={{ width: 8, height: 8, background: 'var(--brand-primary)', borderRadius: '50%', boxShadow: '0 0 8px var(--brand-primary)' }} />
                    Live Production Instance
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
