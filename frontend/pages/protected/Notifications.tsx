import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { NavBar } from './Dashboard';
import api from '../../services/api';

interface Notification {
  id: string;
  type: 'reminder' | 'success' | 'info' | 'warning';
  title: string;
  message: string;
  read: boolean;
  createdAt: string;
}

const typeStyle = {
  reminder: { color: '#f59e0b', bg: 'rgba(245,158,11,0.1)', icon: '⏰' },
  success: { color: 'var(--brand-primary)', bg: 'rgba(15,173,182,0.1)', icon: '✅' },
  info: { color: '#3b82f6', bg: 'rgba(59,130,246,0.1)', icon: '💡' },
  warning: { color: 'var(--red)', bg: 'rgba(231,76,60,0.1)', icon: '⚠️' },
};

export default function Notifications() {
  const [notifs, setNotifs] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/notifications/').then(res => setNotifs(res.data))
      .catch(() => setNotifs([
        { id: '1', type: 'info', title: 'Welcome to Wellness Solutions!', message: 'Explore our classes and book your first session.', read: false, createdAt: new Date().toISOString() },
      ])).finally(() => setLoading(false));
  }, []);

  const markRead = (id: string) => {
    setNotifs(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  };

  const markAllRead = () => setNotifs(prev => prev.map(n => ({ ...n, read: true })));
  const unread = notifs.filter(n => !n.read).length;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 720, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 40 }}>
          <div>
            <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 6px' }}>Notifications</h1>
            <p style={{ color: '#888', margin: 0, fontSize: '0.95rem' }}>{unread > 0 ? `${unread} unread` : 'All caught up! 🎉'}</p>
          </div>
          {unread > 0 && (
            <button onClick={markAllRead} style={{ background: 'transparent', border: '1px solid #222', color: '#888', padding: '8px 18px', borderRadius: 10, cursor: 'pointer', fontSize: '0.9rem' }}>
              Mark all read
            </button>
          )}
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', color: '#555', padding: '60px 0' }}>Loading notifications...</div>
        ) : notifs.length === 0 ? (
          <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: '60px 40px', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: 16 }}>🔔</div>
            <p style={{ color: '#888' }}>No notifications yet.</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {notifs.map(n => {
              const style = typeStyle[n.type] || typeStyle.info;
              return (
                <div key={n.id} onClick={() => markRead(n.id)} style={{
                  background: n.read ? 'rgba(18,18,18,0.5)' : 'var(--dark)', border: `1px solid ${n.read ? '#1a1a1a' : '#222'}`,
                  borderRadius: 16, padding: '20px 24px', cursor: 'pointer', display: 'flex', gap: 16, alignItems: 'flex-start',
                  transition: 'background 0.2s',
                }}
                  onMouseOver={e => e.currentTarget.style.background = 'var(--dark)'}
                  onMouseOut={e => e.currentTarget.style.background = n.read ? 'rgba(18,18,18,0.5)' : 'var(--dark)'}>
                  <div style={{ width: 40, height: 40, flexShrink: 0, background: style.bg, borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem' }}>
                    {style.icon}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, flexWrap: 'wrap' }}>
                      <h3 style={{ margin: 0, fontWeight: 700, fontSize: '1rem', color: n.read ? '#888' : '#fff' }}>{n.title}</h3>
                      {!n.read && <div style={{ width: 8, height: 8, borderRadius: '50%', background: style.color, flexShrink: 0, marginTop: 4 }} />}
                    </div>
                    <p style={{ margin: '4px 0 0', color: n.read ? '#555' : '#a1a1aa', fontSize: '0.9rem', lineHeight: 1.5 }}>{n.message}</p>
                    <div style={{ color: '#444', fontSize: '0.8rem', marginTop: 8 }}>
                      {new Date(n.createdAt).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </div>
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
