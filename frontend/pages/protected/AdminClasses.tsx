import { useState, useEffect } from 'react';
import { NavBar } from './Dashboard';
import api from '../../services/api';

interface TimeSlot {
  id: number;
  startTime: string;
  endTime: string;
  isBooked: boolean;
}

interface Class {
  id: number;
  title: string;
  instructor: { name: string };
  location: string;
  price: number;
  slots: TimeSlot[];
}

export default function AdminClasses() {
  const [classes, setClasses] = useState<Class[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.get('/classes/').then(res => {
      try {
        const flatData = res.data || [];
        const grouped: Record<string, Class> = {};

        flatData.forEach((item: any) => {
          if (!item) return;
          const title = item.title || 'Untitled Service';
          const instructorName = item.instructor?.name || 'TBD';
          const key = `${title}-${instructorName}`;

          if (!grouped[key]) {
            grouped[key] = {
              id: item.id || Math.random(),
              title: title,
              instructor: { id: item.instructor?.id || null, name: instructorName },
              location: item.location?.name || 'Main Studio',
              price: item.price || 85,
              slots: []
            };
          }
          if (item.startTime && item.endTime) {
            grouped[key].slots.push({
              id: item.id,
              startTime: item.startTime,
              endTime: item.endTime,
              isBooked: (item.enrolledCount || 0) >= (item.capacity || 1)
            });
          }
        });

        setClasses(Object.values(grouped));
      } catch (err) {
        console.error("Grouping error:", err);
      }
    }).catch(err => {
      console.error("API error:", err);
    }).finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ marginBottom: 40 }}>
          <div style={{ color: 'var(--brand-primary)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 8 }}>Admin Panel</div>
          <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.8rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>Class Master Schedule</h1>
          <p style={{ color: '#888', margin: 0 }}>Track all scheduled services, sessions, and time slots across all locations.</p>
        </div>

        {loading ? <div style={{ color: '#555', padding: '80px 0', textAlign: 'center' }}>Loading schedule...</div> : classes.length === 0 ? (
          <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: '80px 40px', textAlign: 'center' }}>
            <div style={{ fontSize: '3.5rem', marginBottom: 20 }}>📆</div>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#fff', marginBottom: 12 }}>No Active Classes Found</h3>
            <p style={{ color: '#888', maxWidth: 500, margin: '0 auto', lineHeight: 1.6 }}>
              There are currently no classes scheduled in the system. Ensure instructors have active working hours and sessions created.
            </p>
            <button onClick={() => window.location.reload()} style={{ marginTop: 24, background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', border: 'none', padding: '12px 24px', borderRadius: 10, cursor: 'pointer', fontWeight: 700 }}>
              🔄 Refresh Master Schedule
            </button>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: 24 }}>
            {classes.map(c => (
              <div key={c.id} style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: 24 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                  <div>
                    <h3 style={{ margin: '0 0 4px', fontSize: '1.2rem', fontWeight: 700 }}>{c.title}</h3>
                    <div style={{ color: '#888', fontSize: '0.85rem' }}>Instructor: <span style={{ color: '#fff' }}>{c.instructor.name}</span></div>
                    <div style={{ color: '#888', fontSize: '0.85rem' }}>Location: <span style={{ color: '#fff' }}>{c.location}</span></div>
                  </div>
                  <div style={{ background: 'rgba(15,173,182,0.1)', color: 'var(--brand-primary)', padding: '6px 12px', borderRadius: 8, fontWeight: 700, fontSize: '0.9rem' }}>
                    ${c.price}
                  </div>
                </div>

                <div style={{ borderTop: '1px solid #1a1a1a', paddingTop: 16 }}>
                  <div style={{ color: '#555', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 12 }}>Time Slots</div>
                  {c.slots && c.slots.length > 0 ? c.slots.map(slot => (
                    <div key={slot.id} style={{
                      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                      background: slot.isBooked ? 'rgba(231,76,60,0.1)' : 'rgba(15,173,182,0.05)',
                      border: `1px solid ${slot.isBooked ? 'rgba(231,76,60,0.2)' : 'rgba(15,173,182,0.2)'}`,
                      padding: '10px 14px', borderRadius: 10, marginBottom: 8, fontSize: '0.9rem',
                    }}>
                      <div style={{ color: slot.isBooked ? 'var(--red)' : 'var(--brand-primary)', fontWeight: 600 }}>
                        {new Date(slot.startTime).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                      </div>
                      <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: slot.isBooked ? 'var(--red)' : 'var(--brand-primary)' }}>
                        {slot.isBooked ? 'Booked' : 'Available'}
                      </span>
                    </div>
                  )) : (
                    <div style={{ color: '#555', fontSize: '0.85rem' }}>No time slots scheduled for this service.</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
