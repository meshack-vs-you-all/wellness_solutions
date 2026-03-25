import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard', { replace: true });
    } catch {
      setError('Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    width: '100%', padding: '14px 16px', background: 'var(--dark)', border: '1px solid #222',
    borderRadius: 12, color: '#fff', fontSize: '1rem', outline: 'none', boxSizing: 'border-box' as const,
    transition: 'border-color 0.2s'
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <div style={{ width: '100%', maxWidth: 440 }}>
        <Link to="/" style={{ textDecoration: 'none' }}>
          <div style={{ fontWeight: 800, fontSize: '1.4rem', display: 'flex', alignItems: 'center', gap: 10, marginBottom: 40, color: '#fff' }}>
            <div style={{ width: 36, height: 36, background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', borderRadius: 10 }} />
            Wellness Solutions
          </div>
        </Link>

        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, margin: '0 0 8px', letterSpacing: '-0.03em' }}>Welcome back</h1>
        <p style={{ color: '#888', marginBottom: 40 }}>Sign in to manage your sessions</p>

        {error && (
          <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 12, padding: '14px 16px', marginBottom: 24, color: '#fca5a5', fontSize: '0.95rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#888', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 }}>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" required style={inputStyle}
              onFocus={e => e.target.style.borderColor = 'var(--brand-primary)'}
              onBlur={e => e.target.style.borderColor = '#222'} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#888', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 }}>Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" required style={inputStyle}
              onFocus={e => e.target.style.borderColor = 'var(--brand-primary)'}
              onBlur={e => e.target.style.borderColor = '#222'} />
          </div>

          <button type="submit" disabled={loading} style={{
            padding: '16px', borderRadius: 12, background: loading ? 'rgba(15, 173, 182, 0.2)' : 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))',
            color: '#fff', fontWeight: 700, fontSize: '1rem', border: 'none', cursor: loading ? 'default' : 'pointer',
            marginTop: 8, transition: 'opacity 0.2s', opacity: loading ? 0.7 : 1,
          }}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: 32, color: '#888' }}>
          Don't have an account?{' '}
          <Link to="/register" style={{ color: 'var(--brand-primary)', textDecoration: 'none', fontWeight: 600 }}>Create one free →</Link>
        </p>
      </div>
    </div>
  );
}