import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { NavBar } from './Dashboard';
import api from '../../services/api';

interface Booking {
  id: number;
  class: { id: number; title: string; startTime: string; endTime: string; instructor: { name: string } };
  status: string;
  bookedAt: string;
}

export default function Bookings() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [cancellingId, setCancellingId] = useState<number | null>(null);

  const fetchBookings = () => {
    api.get('/bookings/me/').then(res => setBookings(res.data)).catch(() => { }).finally(() => setLoading(false));
  };

  useEffect(() => { fetchBookings(); }, []);

  const handleExportCalendar = async () => {
    try {
      const response = await api.get('/calendar/export/', { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'jpf_schedule.ics');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (e) {
      alert("Failed to export calendar. Please try again later.");
    }
  };

  const handleCancel = async (id: number) => {
    if (!confirm('Cancel this booking?')) return;
    setCancellingId(id);
    try {
      await api.delete(`/bookings/${id}/`);
      fetchBookings();
    } catch {
      alert('Could not cancel. Please try again.');
    } finally {
      setCancellingId(null);
    }
  };

  const statusColor = (s: string) => s === 'confirmed' ? 'var(--brand-primary)' : s === 'cancelled' ? 'var(--red)' : '#f59e0b';

  const [activeTab, setActiveTab] = useState<'upcoming' | 'past'>('upcoming');

  const upcomingBookings = bookings.filter(b => new Date(b.class.startTime) >= new Date());
  const pastBookings = bookings.filter(b => new Date(b.class.startTime) < new Date());
  const displayedBookings = activeTab === 'upcoming' ? upcomingBookings : pastBookings;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 40, flexWrap: 'wrap', gap: 20 }}>
          <div>
            <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>My Bookings</h1>
            <p style={{ color: '#888', margin: 0 }}>View your upcoming stretches and calendar.</p>
          </div>
          <div style={{ display: 'flex', gap: 16 }}>
            <button onClick={handleExportCalendar} style={{ background: 'var(--dark)', border: '1px solid #222', color: '#fff', padding: '12px 20px', borderRadius: 12, cursor: 'pointer', fontWeight: 600, display: 'flex', alignItems: 'center', gap: 8 }}>
              📅 Export to Calendar
            </button>
            <Link to="/booking" style={{ background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '12px 24px', borderRadius: 12, textDecoration: 'none', fontWeight: 700, display: 'inline-block' }}>
              + New Booking
            </Link>
          </div>
        </div>

        {/* Tabs */}
        <div style={{ display: 'flex', gap: 12, marginBottom: 32, borderBottom: '1px solid #222', paddingBottom: 16 }}>
          <button onClick={() => setActiveTab('upcoming')} style={{
            background: activeTab === 'upcoming' ? '#222' : 'transparent', color: activeTab === 'upcoming' ? '#fff' : '#888',
            border: activeTab === 'upcoming' ? '1px solid #333' : '1px solid transparent', padding: '10px 24px', borderRadius: 99, cursor: 'pointer', fontWeight: 600, fontSize: '0.95rem'
          }}>Upcoming Sessions ({upcomingBookings.length})</button>
          <button onClick={() => setActiveTab('past')} style={{
            background: activeTab === 'past' ? '#222' : 'transparent', color: activeTab === 'past' ? '#fff' : '#888',
            border: activeTab === 'past' ? '1px solid #333' : '1px solid transparent', padding: '10px 24px', borderRadius: 99, cursor: 'pointer', fontWeight: 600, fontSize: '0.95rem'
          }}>Past Sessions ({pastBookings.length})</button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', color: '#555', padding: '80px 0' }}>Loading bookings...</div>
        ) : displayedBookings.length === 0 ? (
          <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: '60px 40px', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: 16 }}>{activeTab === 'upcoming' ? '📅' : '🕰️'}</div>
            <h3 style={{ color: '#888', margin: '0 0 16px' }}>No {activeTab} bookings</h3>
            {activeTab === 'upcoming' && <Link to="/booking" style={{ color: 'var(--brand-primary)', textDecoration: 'none', fontWeight: 600 }}>Book your next session →</Link>}
          </div>
        ) : (
          <div>
            {displayedBookings.map(b => {
              const isFuture = new Date(b.class.startTime) >= new Date();
              return (
                <div key={b.id} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 16, padding: '24px', marginBottom: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 20 }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: 6 }}>{b.class.title}</div>
                    <div style={{ color: '#888', fontSize: '0.9rem', marginBottom: 4 }}>
                      {new Date(b.class.startTime).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </div>
                    {b.class.instructor?.name && <div style={{ color: '#666', fontSize: '0.85rem' }}>with {b.class.instructor.name}</div>}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                    <span style={{ background: 'rgba(15,173,182,0.1)', color: 'var(--brand-primary)', border: '1px solid rgba(15,173,182,0.2)', borderRadius: 8, padding: '5px 12px', fontSize: '0.85rem', fontWeight: 600 }}>
                      {b.status}
                    </span>
                    {isFuture && b.status !== 'cancelled' && (
                      <div style={{ display: 'flex', gap: 8 }}>
                        {b.class.instructor?.name && (
                          <a href={`https://wa.me/254700000000?text=Hi%20${b.class.instructor.name.split(' ')[0]},%20I'm%20reaching%20out%20about%20my%20upcoming%20stretch%20session`} target="_blank" rel="noreferrer" style={{ background: '#25D36615', border: '1px solid #25D36633', color: '#25D366', textDecoration: 'none', padding: '6px 14px', borderRadius: 8, fontSize: '0.85rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: 6 }}>
                            💬 Message Trainer
                          </a>
                        )}
                        <button onClick={() => handleCancel(b.id)} disabled={cancellingId === b.id} style={{ background: 'transparent', border: '1px solid #222', color: 'var(--red)', padding: '6px 14px', borderRadius: 8, cursor: 'pointer', fontSize: '0.85rem', fontWeight: 600 }}>
                          {cancellingId === b.id ? 'Cancelling...' : 'Cancel'}
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
