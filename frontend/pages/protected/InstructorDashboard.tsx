import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { NavBar } from './Dashboard';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

interface Booking {
  id: number;
  bookingNumber: string;
  client: { id: number; name: string; email: string };
  service: string;
  startTime: string;
  endTime: string;
  status: string;
  paymentStatus: string;
}

const statusColor = (s: string): string =>
  s === 'confirmed' ? 'var(--brand-primary)' : s === 'cancelled' ? 'var(--red)' : '#f59e0b';

export default function InstructorDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [upcomingClasses, setUpcomingClasses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Role-based redirection
    if (user && user.role !== 'instructor') {
      // If admin, they might want to see instructor view, but usually they have their own.
      // For now, only allow instructors.
      if (user.role === 'admin' || user.isAdmin || user.isStaff) {
        // Admins can stay or be redirected to /admin. Let's allow them to see it if they explicitly navigate here.
      } else {
        navigate('/dashboard');
        return;
      }
    }

    Promise.all([
      api.get('/instructor/bookings/').catch(() => ({ data: { bookings: [] } })),
      api.get('/instructor/classes/').catch(() => ({ data: [] })),
    ]).then(([bookRes, classRes]) => {
      setBookings(bookRes.data.bookings || []);
      setUpcomingClasses(classRes.data || []);
    }).finally(() => setLoading(false));
  }, [user, navigate]);

  const todayBookings = bookings.filter(b => {
    const d = new Date(b.startTime);
    const today = new Date();
    return d.toDateString() === today.toDateString();
  });

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ marginBottom: 40, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: 20 }}>
          <div>
            <div style={{ color: 'var(--brand-primary)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 8 }}>Instructor Panel</div>
            <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.8rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>My Schedule</h1>
            <p style={{ color: '#888', margin: 0 }}>Track your sessions, manage client bookings, and view your calendar.</p>
          </div>

          {/* Daily Briefing Widget */}
          <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 16, padding: '16px 20px', display: 'flex', gap: 24 }}>
            <div>
              <div style={{ fontSize: '0.7rem', color: '#555', textTransform: 'uppercase', fontWeight: 700 }}>Today's Load</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 800 }}>{todayBookings.length} Sessions</div>
            </div>
            <div style={{ borderLeft: '1px solid #222', paddingLeft: 24 }}>
              <div style={{ fontSize: '0.7rem', color: '#555', textTransform: 'uppercase', fontWeight: 700 }}>Pending Prep</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#f59e0b' }}>{todayBookings.filter(b => b.status === 'confirmed').length} Clients</div>
            </div>
          </div>
        </div>

        {/* Stat cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 20, marginBottom: 48 }}>
          {[
            { label: "Today's Sessions", value: todayBookings.length, color: 'var(--brand-primary)' },
            { label: 'Total Bookings', value: bookings.length, color: '#3b82f6' },
            { label: 'Upcoming Classes', value: upcomingClasses.length, color: '#8b5cf6' },
            { label: 'Confirmed Today', value: todayBookings.filter(b => b.status === 'confirmed').length, color: '#f59e0b' },
          ].map(({ label, value, color }) => (
            <div key={label} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: '24px 20px' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 800, color }}>{value}</div>
              <div style={{ color: '#888', fontSize: '0.85rem', marginTop: 4 }}>{label}</div>
            </div>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: 32, alignItems: 'start' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: 32 }}>
            {/* Today's bookings */}
            <div>
              <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: 20 }}>Today's Clients</h2>
              {loading ? <div style={{ color: '#555', padding: '40px 0' }}>Loading...</div>
                : todayBookings.length === 0 ? (
                  <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 16, padding: '40px 24px', textAlign: 'center', color: '#555' }}>
                    No sessions today. Enjoy your day off! 🌿
                  </div>
                ) : todayBookings.map(b => (
                  <div key={b.id} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 14, padding: '18px 20px', marginBottom: 10 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 12 }}>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{b.client.name}</div>
                        <div style={{ color: '#888', fontSize: '0.9rem', marginTop: 4 }}>{b.service} • {new Date(b.startTime).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}</div>
                      </div>
                      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                        <span style={{ background: `${statusColor(b.status)}18`, color: statusColor(b.status), border: `1px solid ${statusColor(b.status)}33`, borderRadius: 8, padding: '4px 12px', fontSize: '0.8rem', fontWeight: 600 }}>{b.status}</span>
                        <button onClick={async (e) => {
                          const btn = e.currentTarget;
                          const container = document.getElementById(`insights-${b.id}`);
                          if (container?.style.display === 'block') { container.style.display = 'none'; return; }

                          const oldText = btn.innerHTML;
                          btn.innerHTML = '✨...';
                          try {
                            const res = await api.get(`/ai/insights/${b.id}/`);
                            container!.innerHTML = `<ul style="margin:0; padding-left: 20px; color: #a1a1aa; font-size: 0.9rem; line-height: 1.5;">
                              ${res.data.insights.map((i: string) => `<li>${i}</li>`).join('')}
                            </ul>`;
                            container!.style.display = 'block';
                          } catch {
                            container!.innerHTML = '<div style="color: #ef4444; font-size: 0.85rem;">Failed to load insights.</div>';
                            container!.style.display = 'block';
                          } finally {
                            btn.innerHTML = '✨ Prep Notes';
                          }
                        }} style={{ background: 'linear-gradient(135deg, rgba(15,173,182,0.1), rgba(15,173,182,0.05))', border: '1px solid rgba(15,173,182,0.2)', color: 'var(--brand-primary)', padding: '6px 14px', borderRadius: 8, cursor: 'pointer', fontSize: '0.8rem', fontWeight: 600, transition: 'all 0.2s' }}>
                          ✨ Prep Notes
                        </button>
                      </div>
                    </div>
                    <div id={`insights-${b.id}`} style={{ display: 'none', marginTop: 16, background: '#0a0a0a', border: '1px solid #1a1a1a', borderRadius: 12, padding: '16px' }}></div>
                  </div>
                ))}
            </div>

            {/* Upcoming classes */}
            <div>
              <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: 20 }}>Upcoming Classes</h2>
              {upcomingClasses.length === 0 ? (
                <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 16, padding: '40px 24px', textAlign: 'center', color: '#555' }}>
                  No upcoming classes scheduled.
                </div>
              ) : upcomingClasses.slice(0, 5).map((c, i) => (
                <div key={i} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 14, padding: '18px 20px', marginBottom: 10, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
                  <div>
                    <div style={{ fontWeight: 700 }}>{c.title}</div>
                    <div style={{ color: '#888', fontSize: '0.85rem' }}>
                      {c.startTime ? new Date(c.startTime).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : 'TBD'}
                    </div>
                  </div>
                  <div style={{ color: '#888', fontSize: '0.85rem' }}>
                    {c.enrolledCount}/{c.capacity} enrolled
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Instructor Action Hub */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: 24 }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 16 }}>Instructor Toolset</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                <button onClick={() => alert('Client Checked-in!')} style={{ background: 'rgba(15,173,182,0.1)', color: 'var(--brand-primary)', border: '1px solid rgba(15,173,182,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left', fontSize: '0.85rem' }}>✅ Start Daily Check-in</button>
                <button onClick={() => alert('Timer Started: 60:00')} style={{ background: 'rgba(59,130,246,0.1)', color: '#3b82f6', border: '1px solid rgba(59,130,246,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left', fontSize: '0.85rem' }}>⏱️ Start Session Timer</button>
                <button onClick={() => alert('Opening SOAP Notes template...')} style={{ background: 'rgba(139,92,246,0.1)', color: '#8b5cf6', border: '1px solid rgba(139,92,246,0.2)', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left', fontSize: '0.85rem' }}>📝 Add Session Notes</button>
                <button onClick={() => alert('Availability Management coming soon.')} style={{ background: 'transparent', color: '#555', border: '1px solid #222', padding: '12px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, textAlign: 'left', fontSize: '0.85rem' }}>📅 Update Availability</button>
              </div>
            </div>

            <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: 24, textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', marginBottom: 12 }}>🧘</div>
              <h4 style={{ margin: '0 0 8px', fontSize: '0.95rem' }}>Expert Level</h4>
              <p style={{ color: '#555', fontSize: '0.8rem', margin: '0 0 16px' }}>Master Instructor (Level 4). You have completed 120+ sessions this year.</p>
              <button style={{ width: '100%', background: 'linear-gradient(135deg, #f59e0b, #d97706)', border: 'none', color: '#fff', padding: '10px', borderRadius: 10, fontSize: '0.8rem', fontWeight: 700 }}>VIEW ACHIEVEMENTS</button>
            </div>
          </div>
        </div>

        {/* All bookings table */}
        {bookings.length > 0 && (
          <div style={{ marginTop: 48 }}>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: 20 }}>All Client Bookings</h2>
            <div style={{ overflowX: 'auto', background: 'var(--dark)', borderRadius: 16, border: '1px solid #222' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem', minWidth: 800 }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid #222' }}>
                    {['Booking #', 'Client', 'Service', 'Date & Time', 'Status', 'Payment'].map(h => (
                      <th key={h} style={{ padding: '16px 20px', textAlign: 'left', color: '#555', fontWeight: 600, fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 1 }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {bookings.slice(0, 20).map(b => (
                    <tr key={b.id} style={{ borderBottom: '1px solid #222' }}>
                      <td style={{ padding: '16px 20px', color: '#10b981', fontWeight: 600 }}>{b.bookingNumber}</td>
                      <td style={{ padding: '16px 20px' }}>
                        <div style={{ fontWeight: 600 }}>{b.client.name}</div>
                        <div style={{ color: '#555', fontSize: '0.8rem' }}>{b.client.email}</div>
                      </td>
                      <td style={{ padding: '16px 20px', color: '#888' }}>{b.service}</td>
                      <td style={{ padding: '16px 20px', color: '#888' }}>{new Date(b.startTime).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</td>
                      <td style={{ padding: '16px 20px' }}>
                        <span style={{ color: statusColor(b.status), fontWeight: 600, fontSize: '0.85rem' }}>{b.status}</span>
                      </td>
                      <td style={{ padding: '16px 20px' }}>
                        <span style={{ color: b.paymentStatus === 'paid' ? '#10b981' : '#888', fontSize: '0.85rem' }}>{b.paymentStatus}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
