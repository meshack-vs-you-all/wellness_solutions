import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Reveal } from 'react-kino';
import api from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';

interface ClassItem {
  id: number | string;
  title: string;
  description: string;
  price: number;
  startTime: string | null;
  instructor: { name: string };
  type: string;
  location: { name: string };
}

export default function SchedulePage() {
  const { user } = useAuth();
  const [classes, setClasses] = useState<ClassItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    api.get('/classes/').then(res => setClasses(res.data)).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const types = ['all', ...Array.from(new Set(classes.map(c => c.type)))];
  const filtered = filter === 'all' ? classes : classes.filter(c => c.type === filter);

  return (
    <div style={{ minHeight: '100vh', background: '#000', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <header style={{ padding: '20px 24px', borderBottom: '1px solid #111', display: 'flex', justifyContent: 'space-between', alignItems: 'center', position: 'sticky', top: 0, background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(10px)', zIndex: 10 }}>
        <Link to="/" style={{ fontWeight: 800, fontSize: '1.1rem', color: '#fff', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{ width: 28, height: 28, background: 'linear-gradient(135deg, #10b981, #047857)', borderRadius: 7 }} />Wellness Solutions
        </Link>
        <Link to={user ? '/booking' : '/register'} style={{ background: 'linear-gradient(135deg, #10b981, #047857)', color: '#fff', padding: '10px 20px', borderRadius: 10, textDecoration: 'none', fontWeight: 700, fontSize: '0.9rem' }}>
          {user ? 'Book a Session' : 'Get Started'}
        </Link>
      </header>

      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '60px 20px' }}>
        <Reveal animation="fade-up">
          <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 20px' }}>Class Schedule</h1>
          <p style={{ color: '#888', marginBottom: 40, fontSize: '1.1rem' }}>Browse all upcoming sessions and book your spot.</p>
        </Reveal>

        {/* Type filter */}
        <div style={{ display: 'flex', gap: 10, marginBottom: 40, flexWrap: 'wrap' }}>
          {types.map(t => (
            <button key={t} onClick={() => setFilter(t)} style={{
              padding: '8px 20px', borderRadius: 99, border: '1px solid', fontSize: '0.9rem', fontWeight: 600, cursor: 'pointer', textTransform: 'capitalize',
              borderColor: filter === t ? '#10b981' : '#222',
              background: filter === t ? 'rgba(16,185,129,0.1)' : 'transparent',
              color: filter === t ? '#10b981' : '#888',
            }}>{t}</button>
          ))}
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', color: '#555', padding: '80px 0' }}>Loading sessions...</div>
        ) : filtered.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#555', padding: '80px 0' }}>No sessions found for this category.</div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 24 }}>
            {filtered.map((c, i) => (
              <Reveal key={c.id} animation="fade-up" delay={i * 80}>
                <div style={{ background: '#111', border: '1px solid #1a1a1a', borderRadius: 20, padding: 28, height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <div style={{ color: '#10b981', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 12 }}>{c.type}</div>
                  <h3 style={{ fontWeight: 700, fontSize: '1.2rem', margin: '0 0 12px' }}>{c.title}</h3>
                  {c.startTime && (
                    <div style={{ color: '#888', fontSize: '0.9rem', marginBottom: 8 }}>
                      📅 {new Date(c.startTime).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </div>
                  )}
                  {c.instructor.name !== 'TBD' && <div style={{ color: '#666', fontSize: '0.85rem', marginBottom: 8 }}>👤 {c.instructor.name}</div>}
                  <div style={{ color: '#666', fontSize: '0.85rem', marginBottom: 16 }}>📍 {c.location.name}</div>
                  <p style={{ color: '#888', fontSize: '0.9rem', lineHeight: 1.6, flex: 1, margin: '0 0 20px' }}>{c.description}</p>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    {c.price > 0 ? <span style={{ color: '#10b981', fontWeight: 700, fontSize: '1.1rem' }}>${c.price}</span> : <span />}
                    <Link to={user ? '/booking' : '/register'} style={{ background: 'linear-gradient(135deg, #10b981, #047857)', color: '#fff', padding: '8px 18px', borderRadius: 10, textDecoration: 'none', fontWeight: 700, fontSize: '0.85rem' }}>
                      {user ? 'Book' : 'Sign Up'}
                    </Link>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
