import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { NavBar } from './Dashboard';
import api from '../../services/api';

interface ClassItem {
  id: number | string;
  title: string;
  description: string;
  price: number;
  startTime: string | null;
  endTime: string | null;
  instructor: { id: number | null; name: string };
  location: { name: string };
  type: string;
}

type Step = 'select' | 'confirm' | 'success';

export default function NewBooking() {
  const navigate = useNavigate();
  const [classes, setClasses] = useState<ClassItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<ClassItem | null>(null);
  const [step, setStep] = useState<Step>('select');
  const [booking, setBooking] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/classes/').then(res => setClasses(res.data)).catch(() => {
      setClasses([]);
    }).finally(() => setLoading(false));
  }, []);

  const handleBook = async () => {
    if (!selected) return;
    setBooking(true);
    setError('');
    try {
      await api.post('/bookings/', { class_id: selected.id });
      setStep('success');
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error;
      setError(msg || 'Booking failed. Please try again.');
    } finally {
      setBooking(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '48px 20px' }}>
        <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>Book a Session</h1>
        <p style={{ color: '#888', marginBottom: 40 }}>Choose from our available classes and secure your spot.</p>

        {step === 'success' ? (
          <div style={{ background: 'linear-gradient(135deg, rgba(15,173,182,0.1), var(--soft-dark))', border: '1px solid rgba(15,173,182,0.3)', borderRadius: 24, padding: '60px 40px', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: 20 }}>🎉</div>
            <h2 style={{ fontWeight: 800, fontSize: '2rem', marginBottom: 12 }}>Booking Confirmed!</h2>
            <p style={{ color: 'var(--brand-primary)', marginBottom: 32, opacity: 0.8 }}>Your session is booked. We'll see you on the mat!</p>
            <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
              <button onClick={() => navigate('/bookings')} style={{ background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '14px 28px', borderRadius: 12, border: 'none', cursor: 'pointer', fontWeight: 700, fontSize: '1rem' }}>View My Bookings</button>
              <button onClick={() => { setStep('select'); setSelected(null); }} style={{ background: 'rgba(255,255,255,0.05)', color: '#fff', padding: '14px 28px', borderRadius: 12, border: '1px solid #222', cursor: 'pointer', fontWeight: 600 }}>Book Another</button>
            </div>
          </div>
        ) : step === 'confirm' && selected ? (
          <div style={{ maxWidth: 500 }}>
            <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: 32, marginBottom: 24 }}>
              <div style={{ color: 'var(--brand-primary)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 12 }}>Booking Summary</div>
              <h3 style={{ fontWeight: 800, fontSize: '1.5rem', margin: '0 0 16px' }}>{selected.title}</h3>
              {selected.startTime && (
                <div style={{ color: '#888', marginBottom: 8 }}>
                  📅 {new Date(selected.startTime).toLocaleString('en-US', { weekday: 'long', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                </div>
              )}
              {selected.instructor.name !== 'TBD' && <div style={{ color: '#888', marginBottom: 8 }}>👤 {selected.instructor.name}</div>}
              <div style={{ color: '#888' }}>📍 {selected.location.name}</div>
              {selected.price > 0 && <div style={{ color: 'var(--brand-primary)', fontWeight: 700, fontSize: '1.5rem', marginTop: 20 }}>${selected.price}</div>}
            </div>

            {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 12, padding: '14px', marginBottom: 20, color: '#fca5a5' }}>{error}</div>}

            <div style={{ display: 'flex', gap: 12 }}>
              <button onClick={() => setStep('select')} style={{ flex: 1, padding: 14, borderRadius: 12, background: 'transparent', border: '1px solid #222', color: '#888', cursor: 'pointer', fontWeight: 600 }}>← Back</button>
              <button onClick={handleBook} disabled={booking} style={{ flex: 2, padding: 14, borderRadius: 12, background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', border: 'none', cursor: booking ? 'default' : 'pointer', fontWeight: 700, opacity: booking ? 0.7 : 1 }}>
                {booking ? 'Confirming...' : 'Confirm Booking'}
              </button>
            </div>
          </div>
        ) : (
          /* Step: Select class */
          loading ? (
            <div style={{ textAlign: 'center', color: '#555', padding: '80px 0' }}>Loading available sessions...</div>
          ) : classes.length === 0 ? (
            <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: '60px 40px', textAlign: 'center' }}>
              <div style={{ fontSize: '3rem', marginBottom: 16 }}>📆</div>
              <p style={{ color: '#888' }}>No upcoming sessions available. Check back soon!</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 20 }}>
              {classes.map(c => (
                <div key={c.id} onClick={() => { setSelected(c); setStep('confirm'); }} style={{
                  background: 'var(--dark)', border: selected?.id === c.id ? '1px solid var(--brand-primary)' : '1px solid #222',
                  borderRadius: 20, padding: 28, cursor: 'pointer', transition: 'all 0.2s', transform: 'translateY(0)',
                }}
                  onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.borderColor = 'var(--brand-primary)'; }}
                  onMouseOut={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = '#222'; }}>
                  <div style={{ color: 'var(--brand-primary)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 12 }}>{c.type}</div>
                  <h3 style={{ fontWeight: 700, fontSize: '1.2rem', margin: '0 0 12px' }}>{c.title}</h3>
                  {c.startTime && (
                    <p style={{ color: '#888', fontSize: '0.875rem', margin: '0 0 8px' }}>
                      {new Date(c.startTime).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </p>
                  )}
                  {c.instructor.name !== 'TBD' && <p style={{ color: '#666', fontSize: '0.85rem', margin: '0 0 16px' }}>with {c.instructor.name}</p>}
                  {c.price > 0 && <div style={{ color: 'var(--brand-primary)', fontWeight: 700, fontSize: '1.2rem' }}>${c.price}</div>}
                </div>
              ))}
            </div>
          )
        )}
      </div>
    </div>
  );
}
