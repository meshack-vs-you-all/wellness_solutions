import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { NavBar } from './Dashboard';
import { Reveal } from 'react-kino';

const tierCopy: Record<string, { title: string; description: string; bullets: string[]; cta: { label: string; to: string } }> = {
  basic: {
    title: 'Basic Virtual',
    description: 'Get started with app-based corrective programmes and a monthly check-in.',
    bullets: ['Virtual corrective programmes', 'Monthly check-in', 'Video library access'],
    cta: { label: 'Explore Programmes', to: '/programmes' },
  },
  premium: {
    title: 'Premium Hybrid',
    description: 'A hybrid plan with weekly in-person sessions and monthly reassessment.',
    bullets: ['Weekly sessions', 'Monthly reassessment', 'Progress tracking', 'Priority booking'],
    cta: { label: 'View Programmes', to: '/programmes' },
  },
  unlimited: {
    title: 'Elite Concierge',
    description: 'Fully personalised support for committed rehabilitation and long-term recovery.',
    bullets: ['Fully personalised programme', 'Priority scheduling', 'Trainer access'],
    cta: { label: 'Book Now', to: '/booking' },
  },
  none: {
    title: 'No Active Plan',
    description: 'Choose a membership to unlock your programmes and progress tracking.',
    bullets: ['Access limited until purchase', 'Upgrade anytime'],
    cta: { label: 'Find a Plan', to: '/pricing' },
  },
};

export default function Membership() {
  const { user } = useAuth();

  const membershipKey = (user?.membershipType ?? 'none') as string;
  const copy = tierCopy[membershipKey] ?? tierCopy.none;

  const expiryText = useMemo(() => {
    if (!user?.membershipExpiry) return 'N/A';
    const dt = new Date(user.membershipExpiry);
    if (Number.isNaN(dt.getTime())) return 'N/A';
    return dt.toLocaleDateString();
  }, [user?.membershipExpiry]);

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 980, margin: '0 auto', padding: '48px 20px' }}>
        <Reveal animation="fade-up">
          <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.6rem)', fontWeight: 900, letterSpacing: '-0.03em', margin: '0 0 10px' }}>
            Membership
          </h1>
          <p style={{ color: '#888', fontSize: '1.05rem', margin: 0 }}>
            Your plan details, access, and next steps.
          </p>
        </Reveal>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginTop: 30 }}>
          <Reveal animation="fade-up" delay={150}>
            <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: 26 }}>
              <div style={{ color: 'var(--brand-primary)', fontWeight: 800, textTransform: 'uppercase', letterSpacing: 2, fontSize: '0.9rem', marginBottom: 10 }}>
                Current Tier
              </div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, marginBottom: 8 }}>{copy.title}</div>
              <div style={{ color: '#888', lineHeight: 1.7, marginBottom: 18 }}>{copy.description}</div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 10 }}>
                {copy.bullets.map((b) => (
                  <div key={b} style={{ display: 'flex', alignItems: 'center', gap: 10, color: '#cbd5e1' }}>
                    <span style={{ width: 10, height: 10, borderRadius: 99, background: 'var(--brand-accent)' }} />
                    <span style={{ fontSize: '0.98rem' }}>{b}</span>
                  </div>
                ))}
              </div>
            </div>
          </Reveal>

          <Reveal animation="fade-up" delay={250}>
            <div style={{ background: 'linear-gradient(135deg, rgba(15,173,182,0.12), var(--dark))', border: '1px solid rgba(15,173,182,0.25)', borderRadius: 24, padding: 26, height: '100%' }}>
              <div style={{ color: '#d4d4d8', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: 10 }}>
                Access Status
              </div>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, marginBottom: 18 }}>
                <span style={{ background: 'rgba(15,173,182,0.1)', border: '1px solid rgba(15,173,182,0.2)', color: 'var(--brand-primary)', borderRadius: 12, padding: '8px 12px', fontWeight: 800, fontSize: '0.92rem' }}>
                  {user?.membershipType !== 'none' ? 'Active' : 'Inactive'}
                </span>
                <span style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.12)', color: '#cbd5e1', borderRadius: 12, padding: '8px 12px', fontWeight: 700, fontSize: '0.92rem' }}>
                  Expires: {expiryText}
                </span>
              </div>

              <p style={{ color: '#888', lineHeight: 1.7, marginBottom: 20 }}>
                This UI is API-ready. Later we can swap these fields to match the real membership entitlement model from your custom backend.
              </p>

              <Link to={copy.cta.to} style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '100%', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '14px 18px', borderRadius: 14, textDecoration: 'none', fontWeight: 900, border: 'none' }}>
                {copy.cta.label}
              </Link>

              <div style={{ marginTop: 14, background: '#0a0a0a', border: '1px solid #222', borderRadius: 16, padding: 16 }}>
                <div style={{ color: '#e4e4e7', fontWeight: 900, marginBottom: 8 }}>Need help?</div>
                <div style={{ color: '#888', fontSize: '0.95rem', lineHeight: 1.6 }}>
                  Contact support and include your booking reference or email.
                </div>
                <Link to="/contact" style={{ color: 'var(--brand-primary)', textDecoration: 'none', fontWeight: 800, display: 'inline-block', marginTop: 10 }}>
                  Go to Support →
                </Link>
              </div>
            </div>
          </Reveal>
        </div>
      </div>
    </div>
  );
}

