import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

interface Booking {
  id: number;
  class: { id: number; title: string; startTime: string; endTime: string; instructor: { name: string } };
  status: string;
  bookedAt: string;
}

const NavBar = () => {
  const { user, logout } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.isAdmin || user?.isStaff;
  const isInstructor = user?.role === 'instructor';

  return (
    <header style={{ padding: '16px 24px', borderBottom: '1px solid #222', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(18,18,18,0.7)', backdropFilter: 'blur(10px)', position: 'sticky', top: 0, zIndex: 10 }}>
      <Link to="/" style={{ fontWeight: 800, fontSize: '1.1rem', color: '#fff', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 8 }}>
        <div style={{ width: 28, height: 28, background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', borderRadius: 7 }} />Wellness Solutions
      </Link>
      <div style={{ display: 'flex', gap: 20, alignItems: 'center' }}>
        {isAdmin ? (
          <>
            <Link to="/admin" style={{ color: '#fff', textDecoration: 'none', fontSize: '0.9rem' }}>Admin Dashboard</Link>
            <Link to="/admin/users" style={{ color: '#888', textDecoration: 'none', fontSize: '0.9rem' }}>Users</Link>
            <Link to="/admin/classes" style={{ color: '#888', textDecoration: 'none', fontSize: '0.9rem' }}>Schedule</Link>
          </>
        ) : isInstructor ? (
          <>
            <Link to="/instructor" style={{ color: '#fff', textDecoration: 'none', fontSize: '0.9rem' }}>Instructor Dashboard</Link>
            <Link to="/bookings" style={{ color: '#888', textDecoration: 'none', fontSize: '0.9rem' }}>My Bookings</Link>
          </>
        ) : (
          <>
            <Link to="/dashboard" style={{ color: '#fff', textDecoration: 'none', fontSize: '0.9rem' }}>Dashboard</Link>
            <Link to="/bookings" style={{ color: '#888', textDecoration: 'none', fontSize: '0.9rem' }}>My Bookings</Link>
            <Link to="/shop" style={{ color: '#888', textDecoration: 'none', fontSize: '0.9rem' }}>Shop</Link>
          </>
        )}
        <Link to="/notifications" style={{ color: '#888', textDecoration: 'none', fontSize: '1.1rem' }} title="Notifications">🔔</Link>
        <Link to="/profile" style={{ color: '#888', textDecoration: 'none', fontSize: '0.9rem' }}>Profile</Link>
        <button onClick={logout} style={{ background: 'transparent', border: '1px solid #222', color: '#888', padding: '6px 14px', borderRadius: 8, cursor: 'pointer', fontSize: '0.9rem' }}>Logout</button>
      </div>
    </header>
  );
};

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [rebookData, setRebookData] = useState<any>(null);

  useEffect(() => {
    // Role-based redirection
    if (user) {
      if (user.role === 'admin' || user.isAdmin || user.isStaff) {
        navigate('/admin');
      } else if (user.role === 'instructor') {
        navigate('/instructor');
      }
    }

    api.get('/bookings/me/').then(res => {
      setBookings(res.data);
    }).catch(() => { }).finally(() => setLoading(false));

    // Smart Rebook Logic
    api.get('/ai/rebook/').then(res => {
      setRebookData(res.data);
    }).catch(() => {
      setRebookData({ available: false });
    });
  }, [user, navigate]);

  const upcoming = bookings.filter(b => new Date(b.class.startTime) > new Date() && b.status !== 'cancelled');
  const past = bookings.filter(b => new Date(b.class.startTime) <= new Date() || b.status === 'cancelled');

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />

      {/* Promotion Banner */}
      <div style={{ background: 'linear-gradient(90deg, var(--dark), var(--brand-primary), var(--dark))', padding: '12px 20px', textAlign: 'center', fontSize: '0.9rem', fontWeight: 700, color: '#fff' }}>
        🚀 FLASH SALE: 20% Off all Recovery Gear this weekend! <Link to="/shop" style={{ color: '#fff', textDecoration: 'underline', marginLeft: 8 }}>Shop Now</Link>
      </div>

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ marginBottom: 48, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: 20 }}>
          <div>
            <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.8rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>
              Welcome back, {user?.name?.split(' ')[0] || 'there'} 👋
            </h1>
            <p style={{ color: '#888', fontSize: '1.1rem' }}>Here's your wellness journey at a glance.</p>
          </div>

          {/* Clinical Insight Mini-Card */}
          <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 16, padding: '12px 20px', maxWidth: 350 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--brand-primary)', fontWeight: 700, fontSize: '0.8rem', textTransform: 'uppercase', marginBottom: 4 }}>
              <span>💡 Clinical Insight</span>
            </div>
            <p style={{ color: '#a1a1aa', fontSize: '0.85rem', margin: 0, lineHeight: 1.4 }}>
              Consistent stretching improves blood flow and reduces cortisol levels by 15%.
            </p>
          </div>
        </div>

        {/* Stat cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 20, marginBottom: 48 }}>
          {[
            { label: 'Upcoming Sessions', value: upcoming.length, color: 'var(--brand-primary)' },
            { label: 'Total Bookings', value: bookings.length, color: '#3b82f6' },
            { label: 'Sessions Completed', value: past.filter(b => b.status !== 'cancelled').length, color: '#8b5cf6' },
          ].map(({ label, value, color }) => (
            <div key={label} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: '28px 24px' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 800, color }}>{value}</div>
              <div style={{ color: '#888', fontSize: '0.9rem', marginTop: 4 }}>{label}</div>
            </div>
          ))}
        </div>

        {/* Main Content Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: 32, alignItems: 'start' }}>
          <div>
            {/* AI Smart Rebook Widget */}
            <div style={{ background: 'linear-gradient(135deg, rgba(15,173,182,0.1), var(--soft-dark))', border: '1px solid rgba(15,173,182,0.2)', borderRadius: 20, padding: '24px 32px', marginBottom: 48, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 20 }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                  <span style={{ fontSize: '1.2rem' }}>✨</span>
                  <h3 style={{ color: 'var(--brand-primary)', fontWeight: 700, margin: 0, fontSize: '1.2rem' }}>Smart Rebook</h3>
                </div>
                {rebookData ? (
                  rebookData.available ? (
                    <p style={{ color: '#a1a1aa', margin: 0, fontSize: '0.95rem' }}>
                      It looks like you prefer <strong>{rebookData.suggested_time}</strong> for {rebookData.service_name}.
                    </p>
                  ) : (
                    <p style={{ color: '#a1a1aa', margin: 0, fontSize: '0.95rem' }}>Book a few more sessions so we can learn your routine!</p>
                  )
                ) : (
                  <p style={{ color: '#a1a1aa', margin: 0, fontSize: '0.95rem' }}>Analyzing your routine...</p>
                )}
              </div>
              <button
                onClick={() => navigate('/booking')}
                disabled={!rebookData?.available}
                style={{
                  background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', border: 'none', padding: '12px 24px', borderRadius: 12,
                  fontWeight: 700, cursor: rebookData?.available ? 'pointer' : 'not-allowed',
                  opacity: rebookData?.available ? 1 : 0.5, transition: 'all 0.3s'
                }}>
                {rebookData?.available ? rebookData.message : 'No Routine Yet'}
              </button>
            </div>

            {/* Upcoming sessions */}
            <div style={{ marginBottom: 40 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0 }}>Upcoming Sessions</h2>
                <Link to="/booking" style={{ background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '10px 20px', borderRadius: 10, textDecoration: 'none', fontWeight: 600, fontSize: '0.9rem' }}>+ Book New</Link>
              </div>
              {loading ? (
                <div style={{ color: '#555', padding: '40px 0', textAlign: 'center' }}>Loading sessions...</div>
              ) : upcoming.length === 0 ? (
                <div style={{ background: '#111', border: '1px solid #1a1a1a', borderRadius: 20, padding: 40, textAlign: 'center' }}>
                  <div style={{ fontSize: '2rem', marginBottom: 16 }}>🧘</div>
                  <p style={{ color: '#888' }}>No upcoming sessions. <Link to="/booking" style={{ color: '#10b981', textDecoration: 'none' }}>Book one now!</Link></p>
                </div>
              ) : upcoming.map(b => (
                <div key={b.id} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 16, padding: '20px 24px', marginBottom: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '1.05rem', marginBottom: 4 }}>{b.class.title}</div>
                    <div style={{ color: '#888', fontSize: '0.9rem' }}>
                      {new Date(b.class.startTime).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                      {b.class.instructor?.name && ` • ${b.class.instructor.name}`}
                    </div>
                  </div>
                  <span style={{ background: 'rgba(15,173,182,0.1)', color: 'var(--brand-primary)', border: '1px solid rgba(15,173,182,0.2)', borderRadius: 8, padding: '4px 12px', fontSize: '0.85rem', fontWeight: 600 }}>
                    {b.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Action Sidebar */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: 24 }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 16 }}>Quick Actions</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                <button onClick={() => navigate('/shop')} style={{ background: 'rgba(15,173,182,0.1)', color: 'var(--brand-primary)', border: '1px solid rgba(15,173,182,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left', fontSize: '0.85rem' }}>💳 Purchase Membership</button>
                <button onClick={() => alert('Opening Clinical History (PDF)...')} style={{ background: 'rgba(59,130,246,0.1)', color: '#3b82f6', border: '1px solid rgba(59,130,246,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left', fontSize: '0.85rem' }}>📄 View Clinical History</button>
                <button onClick={() => alert('Referral Link Copied!')} style={{ background: 'rgba(245,158,11,0.1)', color: '#f59e0b', border: '1px solid rgba(245,158,11,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left', fontSize: '0.85rem' }}>🎁 Refer a Friend</button>
              </div>
            </div>

            <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: 24, textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', marginBottom: 12 }}>📱</div>
              <h4 style={{ margin: '0 0 8px', fontSize: '0.95rem' }}>App Integration</h4>
              <p style={{ color: '#555', fontSize: '0.8rem', margin: '0 0 16px' }}>Sync your progress with Apple Health or Google Fit.</p>
              <button style={{ width: '100%', background: '#222', border: 'none', color: '#888', padding: '10px', borderRadius: 10, fontSize: '0.8rem', fontWeight: 600 }}>Connected</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export { NavBar };
