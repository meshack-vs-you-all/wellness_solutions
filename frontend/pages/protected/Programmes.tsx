import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { Reveal } from 'react-kino';
import { NavBar } from './Dashboard';

type Programme = {
  id: string;
  title: string;
  subtitle: string;
  durationWeeks: number;
  includes: string[];
  accent: 'teal' | 'blue' | 'purple' | 'amber';
};

const PROGRAMMES: Programme[] = [
  {
    id: 'posture-reset',
    title: 'Posture Reset',
    subtitle: 'Correct your alignment with structured sessions over 8–12 weeks.',
    durationWeeks: 12,
    includes: ['Posture & foot assessment', 'Corrective exercise therapy', 'Homework between sessions'],
    accent: 'teal',
  },
  {
    id: 'pain-relief',
    title: 'Pain Relief',
    subtitle: 'Back, knee, and neck relief through targeted movement and recovery.',
    durationWeeks: 10,
    includes: ['Myofascial release (where applicable)', 'Symptom-focused programme', 'Recovery plan'],
    accent: 'blue',
  },
  {
    id: 'strong-feet',
    title: 'Strong Feet & Movement',
    subtitle: 'For athletes and rehab clients: stability, mobility, and performance.',
    durationWeeks: 8,
    includes: ['Foot scanning integration (later)', 'Strength + mobility progression', 'Session tracking'],
    accent: 'purple',
  },
];

const accentToBg = (accent: Programme['accent']) => {
  switch (accent) {
    case 'teal':
      return 'linear-gradient(135deg, rgba(15,173,182,0.18), rgba(15,173,182,0.02))';
    case 'blue':
      return 'linear-gradient(135deg, rgba(59,130,246,0.18), rgba(59,130,246,0.02))';
    case 'purple':
      return 'linear-gradient(135deg, rgba(139,92,246,0.18), rgba(139,92,246,0.02))';
    case 'amber':
      return 'linear-gradient(135deg, rgba(245,158,11,0.18), rgba(245,158,11,0.02))';
  }
};

export default function Programmes() {
  const totalIncludesCount = useMemo(() => PROGRAMMES.reduce((acc, p) => acc + p.includes.length, 0), []);

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '48px 20px' }}>
        <Reveal animation="fade-up">
          <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.6rem)', fontWeight: 900, letterSpacing: '-0.03em', margin: '0 0 10px' }}>
            Programmes
          </h1>
          <p style={{ color: '#888', fontSize: '1.05rem', margin: 0 }}>
            Structured programmes designed for corrective outcomes.
          </p>
        </Reveal>

        <div style={{ marginTop: 20, marginBottom: 28, display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <span style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.12)', color: '#cbd5e1', borderRadius: 12, padding: '8px 12px', fontWeight: 800, fontSize: '0.92rem' }}>
            {PROGRAMMES.length} programmes
          </span>
          <span style={{ background: 'rgba(15,173,182,0.10)', border: '1px solid rgba(15,173,182,0.20)', color: 'var(--brand-primary)', borderRadius: 12, padding: '8px 12px', fontWeight: 800, fontSize: '0.92rem' }}>
            {totalIncludesCount} included elements
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20 }}>
          {PROGRAMMES.map((p, i) => (
            <Reveal key={p.id} animation="fade-up" delay={i * 120}>
              <div style={{ background: accentToBg(p.accent), border: '1px solid rgba(255,255,255,0.12)', borderRadius: 24, padding: 22, minHeight: 260 }}>
                <div style={{ color: 'var(--brand-primary)', fontWeight: 900, letterSpacing: 2, textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: 12 }}>
                  {p.durationWeeks}-week plan
                </div>
                <div style={{ fontSize: '1.6rem', fontWeight: 900, marginBottom: 8 }}>{p.title}</div>
                <div style={{ color: '#a1a1aa', lineHeight: 1.7, marginBottom: 14 }}>{p.subtitle}</div>

                <div style={{ marginBottom: 18 }}>
                  {p.includes.slice(0, 3).map((inc) => (
                    <div key={inc} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
                      <span style={{ width: 10, height: 10, borderRadius: 99, background: 'var(--brand-accent)' }} />
                      <span style={{ color: '#cbd5e1', fontSize: '0.95rem' }}>{inc}</span>
                    </div>
                  ))}
                </div>

                <Link
                  to={`/programmes/${p.id}`}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '100%',
                    background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))',
                    color: '#fff',
                    padding: '14px 16px',
                    borderRadius: 14,
                    textDecoration: 'none',
                    fontWeight: 950,
                    border: 'none',
                  }}
                >
                  View Programme →
                </Link>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </div>
  );
}

