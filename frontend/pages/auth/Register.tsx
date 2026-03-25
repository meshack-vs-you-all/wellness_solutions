import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (password !== confirm) { setError('Passwords do not match.'); return; }
    if (password.length < 8) { setError('Password must be at least 8 characters.'); return; }
    setLoading(true);
    try {
      await register(name, email, password);
      navigate('/dashboard', { replace: true });
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error;
      setError(msg || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    width: '100%', padding: '14px 16px', background: 'var(--dark)', border: '1px solid #222',
    borderRadius: 12, color: '#fff', fontSize: '1rem', outline: 'none', boxSizing: 'border-box' as const, transition: 'border-color 0.2s',
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

        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, margin: '0 0 8px', letterSpacing: '-0.03em' }}>Create account</h1>
        <p style={{ color: '#888', marginBottom: 40 }}>Start your wellness journey today</p>

        {error && (
          <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 12, padding: '14px 16px', marginBottom: 24, color: '#fca5a5', fontSize: '0.95rem' }}>{error}</div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {[
            { label: 'Full Name', type: 'text', val: name, set: setName, placeholder: 'Jane Smith' },
            { label: 'Email', type: 'email', val: email, set: setEmail, placeholder: 'you@example.com' },
            { label: 'Password', type: 'password', val: password, set: setPassword, placeholder: '8+ characters' },
            { label: 'Confirm Password', type: 'password', val: confirm, set: setConfirm, placeholder: 'Repeat password' },
          ].map(({ label, type, val, set, placeholder }) => (
            <div key={label}>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#888', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 }}>{label}</label>
              <input type={type} value={val} onChange={e => set(e.target.value)} placeholder={placeholder} required style={inputStyle}
                onFocus={e => e.target.style.borderColor = 'var(--brand-primary)'}
                onBlur={e => e.target.style.borderColor = '#222'} />
            </div>
          ))}

          <button type="submit" disabled={loading} style={{
            padding: 16, borderRadius: 12, background: loading ? 'rgba(15, 173, 182, 0.2)' : 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))',
            color: '#fff', fontWeight: 700, fontSize: '1rem', border: 'none', cursor: loading ? 'default' : 'pointer',
            marginTop: 8, opacity: loading ? 0.7 : 1,
          }}>
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: 32, color: '#888' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: 'var(--brand-primary)', textDecoration: 'none', fontWeight: 600 }}>Sign in →</Link>
        </p>
      </div>
    </div>
  );
}