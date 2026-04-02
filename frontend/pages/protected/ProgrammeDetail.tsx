import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Reveal } from 'react-kino';
import { NavBar } from './Dashboard';

type Programme = {
  id: string;
  title: string;
  durationWeeks: number;
  overview: string;
  lessons: { id: string; title: string; durationMin: number }[];
};

const PROGRAMME_BY_ID: Record<string, Programme> = {
  'posture-reset': {
    id: 'posture-reset',
    title: 'Posture Reset',
    durationWeeks: 12,
    overview: 'A structured corrective plan to improve posture, alignment, and daily movement quality.',
    lessons: [
      { id: 'week1', title: 'Assessment + Baseline Flow', durationMin: 25 },
      { id: 'week2', title: 'Core Support & Stability', durationMin: 30 },
      { id: 'week3', title: 'Upper Back Mobility', durationMin: 22 },
    ],
  },
  'pain-relief': {
    id: 'pain-relief',
    title: 'Pain Relief',
    durationWeeks: 10,
    overview: 'Targeted movement and recovery to reduce discomfort and build resilient mobility.',
    lessons: [
      { id: 'week1', title: 'Relief Routine (Foundation)', durationMin: 20 },
      { id: 'week2', title: 'Mobility + Myofascial Release', durationMin: 28 },
      { id: 'week3', title: 'Recovery Build (Breathing + Stretch)', durationMin: 24 },
    ],
  },
  'strong-feet': {
    id: 'strong-feet',
    title: 'Strong Feet & Movement',
    durationWeeks: 8,
    overview: 'Strength and mobility for athletes and rehab clients focused on foot stability and kinetic chain control.',
    lessons: [
      { id: 'week1', title: 'Foot Stability + Tension Reset', durationMin: 24 },
      { id: 'week2', title: 'Knee + Hip Alignment Drills', durationMin: 32 },
      { id: 'week3', title: 'Power Steps + Mobility', durationMin: 26 },
    ],
  },
};

export default function ProgrammeDetail() {
  const { id } = useParams<{ id: string }>();
  const programmeId = id ?? '';
  const programme = PROGRAMME_BY_ID[programmeId];

  const [completedLessonIds, setCompletedLessonIds] = useState<string[]>([]);

  const progress = useMemo(() => {
    if (!programme) return 0;
    if (programme.lessons.length === 0) return 0;
    const done = programme.lessons.filter((l) => completedLessonIds.includes(l.id)).length;
    return done / programme.lessons.length;
  }, [completedLessonIds, programme]);

  if (!programme) {
    return (
      <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
        <NavBar />
        <div style={{ maxWidth: 900, margin: '0 auto', padding: '48px 20px' }}>
          <h1 style={{ fontSize: '2rem', fontWeight: 900, margin: '0 0 10px' }}>Programme not found</h1>
          <Link to="/programmes" style={{ color: 'var(--brand-primary)', textDecoration: 'none', fontWeight: 900 }}>← Back to Programmes</Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <NavBar />
      <div style={{ maxWidth: 980, margin: '0 auto', padding: '48px 20px' }}>
        <Reveal animation="fade-up">
          <div style={{ marginBottom: 18 }}>
            <Link to="/programmes" style={{ color: '#a1a1aa', textDecoration: 'none', fontWeight: 700 }}>
              ← Programmes
            </Link>
          </div>
          <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.7rem)', fontWeight: 950, letterSpacing: '-0.03em', margin: '0 0 10px' }}>
            {programme.title}
          </h1>
          <p style={{ color: '#888', fontSize: '1.05rem', margin: 0, lineHeight: 1.7 }}>{programme.overview}</p>
        </Reveal>

        <div style={{ marginTop: 26, background: 'var(--dark)', border: '1px solid #222', borderRadius: 24, padding: 22 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12 }}>
            <div>
              <div style={{ color: 'var(--brand-primary)', fontWeight: 900, letterSpacing: 2, textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: 6 }}>
                Progress
              </div>
              <div style={{ fontSize: '1.25rem', fontWeight: 900 }}>
                {(progress * 100).toFixed(0)}% complete
              </div>
            </div>
            <div style={{ minWidth: 220, flex: '1 1 220px' }}>
              <div style={{ width: '100%', height: 12, background: 'rgba(255,255,255,0.08)', borderRadius: 999, overflow: 'hidden', border: '1px solid rgba(255,255,255,0.10)' }}>
                <div style={{ width: `${progress * 100}%`, height: '100%', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))' }} />
              </div>
              <div style={{ color: '#888', fontSize: '0.9rem', marginTop: 8 }}>
                Placeholder progress for API wiring.
              </div>
            </div>
          </div>
        </div>

        <div style={{ marginTop: 22, display: 'grid', gridTemplateColumns: '1fr', gap: 14 }}>
          {programme.lessons.map((lesson, i) => {
            const done = completedLessonIds.includes(lesson.id);
            return (
              <Reveal key={lesson.id} animation="fade-up" delay={i * 90}>
                <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: 18, display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
                  <div>
                    <div style={{ fontWeight: 900, fontSize: '1.08rem', marginBottom: 6 }}>{lesson.title}</div>
                    <div style={{ color: '#888', fontSize: '0.92rem' }}>{lesson.durationMin} min</div>
                  </div>
                  <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                    <button
                      onClick={() => setCompletedLessonIds((prev) => (done ? prev.filter((x) => x !== lesson.id) : [...prev, lesson.id]))}
                      style={{ background: done ? 'rgba(16,185,129,0.18)' : 'rgba(255,255,255,0.06)', border: `1px solid ${done ? 'rgba(16,185,129,0.35)' : 'rgba(255,255,255,0.12)'}`, color: done ? '#34d399' : '#cbd5e1', padding: '10px 14px', borderRadius: 14, cursor: 'pointer', fontWeight: 900 }}
                    >
                      {done ? 'Mark incomplete' : 'Mark complete'}
                    </button>
                    <Link
                      to="/booking"
                      style={{ background: 'rgba(15,173,182,0.10)', border: '1px solid rgba(15,173,182,0.2)', color: 'var(--brand-primary)', padding: '10px 14px', borderRadius: 14, textDecoration: 'none', fontWeight: 900 }}
                    >
                      Book session
                    </Link>
                  </div>
                </div>
              </Reveal>
            );
          })}
        </div>
      </div>
    </div>
  );
}

