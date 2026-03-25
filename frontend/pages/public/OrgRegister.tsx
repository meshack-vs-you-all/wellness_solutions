import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../services/api';

interface OrgForm {
  orgName: string;
  contactName: string;
  email: string;
  phone: string;
  employees: string;
  program: string;
}

const PROGRAMS = [
  { id: 'basic', label: 'Basic Wellness', desc: '4 sessions/month per employee', price: 'from KES 5,000/emp/mo' },
  { id: 'standard', label: 'Standard Program', desc: '8 sessions/month + workshops', price: 'from KES 8,000/emp/mo' },
  { id: 'premium', label: 'Premium Corporate', desc: 'Unlimited sessions + dedicated coach', price: 'from KES 15,000/emp/mo' },
];

export default function OrgRegister() {
  const navigate = useNavigate();
  const [form, setForm] = useState<OrgForm>({ orgName: '', contactName: '', email: '', phone: '', employees: '', program: '' });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); setError('');
    try {
      const res = await api.post('/organizations/register/', form);
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (success) return (
    <div style={{ minHeight: '100vh', background: '#000', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'system-ui, sans-serif', textAlign: 'center', padding: 20 }}>
      <div>
        <div style={{ fontSize: '4rem', marginBottom: 16 }}>🎉</div>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, margin: '0 0 16px' }}>You're Registered!</h1>
        <p style={{ color: '#a7f3d0', marginBottom: 8 }}>Welcome to JPF Corporate Wellness, <strong>{form.orgName}</strong>.</p>
        <p style={{ color: '#888', marginBottom: 40 }}>Our team will reach out within 24 hours to schedule your onboarding. Temporary password: <code style={{ background: '#111', padding: '2px 8px', borderRadius: 6, color: '#10b981' }}>TempPass123!</code></p>
        <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link to="/login" style={{ background: 'linear-gradient(135deg, #10b981, #047857)', color: '#fff', padding: '14px 28px', borderRadius: 12, textDecoration: 'none', fontWeight: 700 }}>Access Your Account</Link>
          <Link to="/" style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid #333', color: '#888', padding: '14px 28px', borderRadius: 12, textDecoration: 'none' }}>Back Home</Link>
        </div>
      </div>
    </div>
  );

  return (
    <div style={{ minHeight: '100vh', background: '#000', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <nav style={{ borderBottom: '1px solid #111', padding: '16px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ color: '#10b981', textDecoration: 'none', fontWeight: 700, fontSize: '1.1rem' }}>Wellness Solutions</Link>
        <Link to="/login" style={{ color: '#888', textDecoration: 'none', fontSize: '0.9rem' }}>Already registered? Log In</Link>
      </nav>

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 20px' }}>
        <div style={{ textAlign: 'center', marginBottom: 60 }}>
          <div style={{ display: 'inline-block', background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.2)', color: '#10b981', borderRadius: 99, padding: '6px 20px', fontSize: '0.85rem', fontWeight: 600, marginBottom: 20 }}>💼 Corporate Wellness</div>
          <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 800, letterSpacing: '-0.04em', margin: '0 0 16px' }}>
            Invest in Your <span style={{ color: '#10b981' }}>Team's Wellbeing</span>
          </h1>
          <p style={{ color: '#888', fontSize: '1.1rem', maxWidth: 600, margin: '0 auto' }}>
            Corporate wellness programs designed to reduce burnout, boost productivity, and keep your team performing at their peak.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 48, alignItems: 'start' }}>
          {/* Programs */}
          <div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: 24 }}>Our Programs</h2>
            {PROGRAMS.map(p => (
              <div key={p.id} onClick={() => setForm(prev => ({ ...prev, program: p.id }))} style={{
                background: form.program === p.id ? 'rgba(16,185,129,0.08)' : '#111',
                border: `1px solid ${form.program === p.id ? 'rgba(16,185,129,0.3)' : '#1a1a1a'}`,
                borderRadius: 16, padding: '20px 24px', marginBottom: 14, cursor: 'pointer', transition: 'all 0.2s',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
                  <h3 style={{ fontWeight: 700, margin: 0, color: form.program === p.id ? '#10b981' : '#fff' }}>{p.label}</h3>
                  {form.program === p.id && <span style={{ color: '#10b981', fontWeight: 700 }}>✓</span>}
                </div>
                <div style={{ color: '#888', fontSize: '0.9rem', marginBottom: 6 }}>{p.desc}</div>
                <div style={{ color: '#10b981', fontWeight: 600, fontSize: '0.85rem' }}>{p.price}</div>
              </div>
            ))}
            <div style={{ marginTop: 32, background: '#111', border: '1px solid #1a1a1a', borderRadius: 16, padding: '20px 24px' }}>
              <h3 style={{ margin: '0 0 12px', fontWeight: 700 }}>All programs include</h3>
              {['Certified wellness practitioners', 'Real-time booking management', 'Monthly wellness reports', 'Priority scheduling', 'Flexible group or 1-on-1 sessions'].map(f => (
                <div key={f} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8, color: '#888', fontSize: '0.9rem' }}>
                  <span style={{ color: '#10b981' }}>✓</span> {f}
                </div>
              ))}
            </div>
          </div>

          {/* Form */}
          <div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: 24 }}>Register Your Organization</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
              {[
                { key: 'orgName', label: 'Organization Name', placeholder: 'Acme Corp Ltd', required: true },
                { key: 'contactName', label: 'Contact Person', placeholder: 'Your full name', required: true },
                { key: 'email', label: 'Work Email', placeholder: 'you@company.com', required: true, type: 'email' },
                { key: 'phone', label: 'Phone Number', placeholder: '+254 700 000 000' },
                { key: 'employees', label: 'Number of Employees', placeholder: 'e.g. 50–100' },
              ].map(({ key, label, placeholder, required, type }) => (
                <div key={key}>
                  <label style={{ display: 'block', color: '#888', fontSize: '0.85rem', marginBottom: 8, fontWeight: 500 }}>{label}{required && ' *'}</label>
                  <input required={required} type={type || 'text'} value={form[key as keyof OrgForm]} onChange={e => setForm(prev => ({ ...prev, [key]: e.target.value }))} placeholder={placeholder}
                    style={{ width: '100%', background: '#111', border: '1px solid #222', color: '#fff', padding: '13px 16px', borderRadius: 12, fontSize: '1rem', outline: 'none', boxSizing: 'border-box' }} />
                </div>
              ))}

              {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)', color: '#ef4444', padding: '12px 16px', borderRadius: 10, fontSize: '0.9rem' }}>{error}</div>}

              <button type="submit" disabled={loading} style={{
                background: loading ? '#1a1a1a' : 'linear-gradient(135deg, #10b981, #047857)', color: loading ? '#555' : '#fff',
                padding: '16px', border: 'none', borderRadius: 14, cursor: loading ? 'not-allowed' : 'pointer', fontWeight: 700, fontSize: '1rem', marginTop: 8,
              }}>
                {loading ? 'Registering...' : 'Register Organization'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
