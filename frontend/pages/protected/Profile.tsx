import { useState } from 'react';
import { NavBar } from './Dashboard';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

export default function Profile() {
  const { user } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [phone, setPhone] = useState(user?.phone || '');
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccess(false);
    setError('');
    try {
      await api.patch('/users/me/update/', { name, phone });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 4000);
    } catch {
      setError('Failed to save changes. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleSyncCalendar = () => {
    const token = localStorage.getItem('authToken');
    window.open(`${api.defaults.baseURL?.replace('/api', '')}/api/calendar/export/?token=${token}`, '_blank');
  };

  const inputStyle = {
    width: '100%', padding: '14px 16px', background: '#111', border: '1px solid #222',
    borderRadius: 12, color: '#fff', fontSize: '1rem', outline: 'none', boxSizing: 'border-box' as const, transition: 'border-color 0.2s',
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 640, margin: '0 auto', padding: '48px 20px' }}>
        <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 40px' }}>Account Settings</h1>

        {/* Avatar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 20, marginBottom: 40 }}>
          <div style={{ width: 72, height: 72, borderRadius: 36, background: 'linear-gradient(135deg, var(--brand-primary), #3b82f6)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem', fontWeight: 800 }}>
            {(user?.name || user?.email || 'U').charAt(0).toUpperCase()}
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: '1.2rem' }}>{user?.name || 'Account'}</div>
            <div style={{ color: '#888' }}>{user?.email}</div>
            <div style={{ color: 'var(--brand-primary)', fontSize: '0.85rem', marginTop: 4 }}>
              {user?.role === 'admin' ? '👑 Admin' : user?.role === 'instructor' ? '🏋️ Instructor' : '🌱 Member'}
            </div>
          </div>
        </div>

        {success && (
          <div style={{ background: 'rgba(15,173,182,0.1)', border: '1px solid rgba(15,173,182,0.3)', borderRadius: 12, padding: '14px 16px', marginBottom: 24, color: 'var(--brand-primary)' }}>
            ✓ Changes saved successfully!
          </div>
        )}
        {error && (
          <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 12, padding: '14px 16px', marginBottom: 24, color: '#fca5a5' }}>{error}</div>
        )}

        <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div>
            <label style={{ display: 'block', color: '#888', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>Full Name</label>
            <input value={name} onChange={e => setName(e.target.value)} style={inputStyle} placeholder="Your name"
              onFocus={e => e.target.style.borderColor = 'var(--brand-primary)'} onBlur={e => e.target.style.borderColor = '#222'} />
          </div>
          <div>
            <label style={{ display: 'block', color: '#888', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>Email Address</label>
            <input value={user?.email || ''} disabled style={{ ...inputStyle, color: '#555', cursor: 'not-allowed' }} />
            <div style={{ color: '#555', fontSize: '0.8rem', marginTop: 6 }}>Email cannot be changed here</div>
          </div>
          <div>
            <label style={{ display: 'block', color: '#888', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>Phone Number</label>
            <input value={phone} onChange={e => setPhone(e.target.value)} style={inputStyle} placeholder="+1 (555) 000-0000"
              onFocus={e => e.target.style.borderColor = 'var(--brand-primary)'} onBlur={e => e.target.style.borderColor = '#222'} />
          </div>
          <button type="submit" disabled={saving} style={{
            padding: '16px', borderRadius: 12, background: saving ? 'rgba(15,173,182,0.3)' : 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))',
            color: '#fff', fontWeight: 700, border: 'none', cursor: saving ? 'default' : 'pointer', fontSize: '1rem', opacity: saving ? 0.7 : 1, marginTop: 8,
          }}>
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </form>

        <div style={{ marginTop: 48, padding: '32px', background: 'var(--dark)', border: '1px solid #222', borderRadius: 24 }}>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: 12 }}>Calendar Integration</h3>
          <p style={{ color: '#888', fontSize: '0.9rem', marginBottom: 24, lineHeight: 1.6 }}>
            Sync your wellness sessions with your personal calendar (Google, Apple, or Outlook).
          </p>
          <button onClick={handleSyncCalendar} style={{ width: '100%', padding: '14px', borderRadius: 12, background: 'rgba(59,130,246,0.1)', color: '#3b82f6', border: '1px solid rgba(59,130,246,0.2)', cursor: 'pointer', fontWeight: 600 }}>
            📅 Sync to External Calendar (iCal)
          </button>
        </div>
      </div>
    </div>
  );
}
