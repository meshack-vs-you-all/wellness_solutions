import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';

interface Trainer {
  id: number;
  name: string;
  bio: string;
  specializations: string[];
  location: string;
  rating: number;
  sessionCount: number;
  availableSlots: { id: number; startTime: string; endTime: string }[];
}

const FALLBACK_TRAINERS: Trainer[] = [
  { id: 1, name: 'Jpeter Fitness', bio: 'Lead wellness practitioner with 8+ years of experience in sports rehabilitation and assisted flexibility.', specializations: ['Assisted Stretching', 'Sports Rehab', 'Flexibility Training'], location: 'JPF Studio Nairobi', rating: 5.0, sessionCount: 340, availableSlots: [] },
  { id: 2, name: 'Coach Amara', bio: 'Certified yoga instructor and wellness coach specializing in mindfulness-based movement therapy.', specializations: ['Yoga', 'Pranayama', 'Mindfulness'], location: 'JPF Studio Nairobi', rating: 4.8, sessionCount: 210, availableSlots: [] },
  { id: 3, name: 'Dr. Wanjiku M.', bio: 'Physiotherapist specialized in injury recovery and functional movement screening.', specializations: ['Physiotherapy', 'Injury Recovery', 'Postural Correction'], location: 'JPF Studio Westlands', rating: 4.9, sessionCount: 180, availableSlots: [] },
];

export default function Trainers() {
  const [trainers, setTrainers] = useState<Trainer[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Trainer | null>(null);

  useEffect(() => {
    api.get('/trainers/availability/').then(res => {
      setTrainers(res.data.length > 0 ? res.data : FALLBACK_TRAINERS);
    }).catch(() => setTrainers(FALLBACK_TRAINERS)).finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ minHeight: '100vh', background: '#000', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      {/* Simple nav */}
      <nav style={{ borderBottom: '1px solid #111', padding: '16px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ color: '#10b981', textDecoration: 'none', fontWeight: 700, fontSize: '1.1rem' }}>Wellness Solutions</Link>
        <div style={{ display: 'flex', gap: 20 }}>
          <Link to="/schedule" style={{ color: '#888', textDecoration: 'none', fontSize: '0.9rem' }}>Schedule</Link>
          <Link to="/booking" style={{ background: 'linear-gradient(135deg, #10b981, #047857)', color: '#fff', padding: '8px 18px', borderRadius: 10, textDecoration: 'none', fontWeight: 700, fontSize: '0.9rem' }}>Book Session</Link>
        </div>
      </nav>

      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ marginBottom: 48, textAlign: 'center' }}>
          <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 800, letterSpacing: '-0.04em', margin: '0 0 16px' }}>
            Meet Our <span style={{ color: '#10b981' }}>Trainers</span>
          </h1>
          <p style={{ color: '#888', fontSize: '1.1rem', maxWidth: 600, margin: '0 auto' }}>
            Expert therapists and wellness coaches dedicated to your body's transformation.
          </p>
        </div>

        {/* AI Matchmaker Widget */}
        <div style={{ background: 'linear-gradient(135deg, #111, #0a0a0a)', border: '1px solid #1a1a1a', borderRadius: 24, padding: '32px', marginBottom: 48, maxWidth: 800, margin: '0 auto 48px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
            <span style={{ fontSize: '1.5rem' }}>✨</span>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 700, margin: 0 }}>AI Therapist Match</h2>
          </div>
          <p style={{ color: '#888', marginBottom: 20, fontSize: '0.95rem' }}>Describe your aches, goals, or tension points, and our AI will find the perfect therapist and stretch package for you.</p>
          <form onSubmit={async (e) => {
            e.preventDefault();
            const input = e.currentTarget.querySelector('input');
            const btn = e.currentTarget.querySelector('button');
            const resultDiv = document.getElementById('ai-match-result');
            if (!input?.value) return;
            
            const oldText = btn!.innerHTML;
            btn!.innerHTML = 'Analyzing...';
            try {
              const res = await api.post('/ai/match/', { query: input.value });
              resultDiv!.style.display = 'block';
              resultDiv!.innerHTML = `
                <div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); padding: 20px; border-radius: 16px; margin-top: 20px;">
                  <div style="color: #10b981; font-weight: 700; margin-bottom: 8px;">Recommended for you: ${res.data.service}</div>
                  <div style="font-weight: 600; margin-bottom: 12px; color: #fff;">With ${res.data.trainer}</div>
                  <div style="color: #a1a1aa; font-size: 0.9rem; line-height: 1.5;">${res.data.reason}</div>
                  <a href="/booking" style="display: inline-block; margin-top: 16px; background: #10b981; color: #fff; text-decoration: none; padding: 8px 20px; border-radius: 8px; font-weight: 600; font-size: 0.9rem;">Book Now</a>
                </div>
              `;
            } catch {
              resultDiv!.style.display = 'block';
              resultDiv!.innerHTML = '<div style="color: #ef4444; margin-top: 16px; font-size: 0.9rem;">Please enter a more descriptive query.</div>';
            } finally {
              btn!.innerHTML = oldText;
            }
          }} style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <input type="text" placeholder="E.g., My lower back hurts from sitting at a desk all day..." style={{ flex: 1, minWidth: 280, background: '#000', border: '1px solid #333', color: '#fff', padding: '14px 20px', borderRadius: 12, outline: 'none', fontSize: '1rem' }} />
            <button type="submit" style={{ background: '#fff', color: '#000', border: 'none', padding: '0 24px', borderRadius: 12, fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 8 }}>
              Find Match
            </button>
          </form>
          <div id="ai-match-result" style={{ display: 'none' }}></div>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', color: '#555', padding: '80px 0' }}>Loading trainers...</div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 28 }}>
            {trainers.map(trainer => (
              <div key={trainer.id} style={{
                background: '#111', border: '1px solid #1a1a1a', borderRadius: 24, overflow: 'hidden',
                transition: 'all 0.25s', cursor: 'pointer',
              }}
                onClick={() => setSelected(selected?.id === trainer.id ? null : trainer)}
                onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.borderColor = '#222'; }}
                onMouseOut={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = '#1a1a1a'; }}>
                {/* Avatar */}
                <div style={{ height: 120, background: `linear-gradient(135deg, #10b98122, #000)`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <div style={{ width: 72, height: 72, borderRadius: '50%', background: 'linear-gradient(135deg, #10b981, #047857)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.8rem', fontWeight: 800 }}>
                    {trainer.name.charAt(0)}
                  </div>
                </div>
                <div style={{ padding: 24 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                    <div>
                      <h3 style={{ fontWeight: 700, fontSize: '1.2rem', margin: '0 0 4px' }}>{trainer.name}</h3>
                      <div style={{ color: '#888', fontSize: '0.85rem' }}>📍 {trainer.location}</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ color: '#f59e0b', fontWeight: 700 }}>⭐ {trainer.rating}</div>
                      <div style={{ color: '#555', fontSize: '0.8rem' }}>{trainer.sessionCount} sessions</div>
                    </div>
                  </div>
                  <p style={{ color: '#888', fontSize: '0.9rem', lineHeight: 1.6, margin: '0 0 16px' }}>{trainer.bio}</p>
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 20 }}>
                    {trainer.specializations.slice(0, 3).map(s => (
                      <span key={s} style={{ background: 'rgba(16,185,129,0.1)', color: '#10b981', border: '1px solid rgba(16,185,129,0.2)', padding: '3px 10px', borderRadius: 99, fontSize: '0.75rem', fontWeight: 600 }}>{s}</span>
                    ))}
                  </div>

                  {trainer.availableSlots.length > 0 && selected?.id === trainer.id && (
                    <div style={{ marginBottom: 16 }}>
                      <div style={{ color: '#555', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 10 }}>Available Slots</div>
                      {trainer.availableSlots.map(slot => (
                        <div key={slot.id} style={{ background: '#0a0a0a', borderRadius: 10, padding: '10px 14px', marginBottom: 6, fontSize: '0.85rem', color: '#a1a1aa' }}>
                          {new Date(slot.startTime).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                        </div>
                      ))}
                    </div>
                  )}

                  <Link to="/booking" style={{
                    display: 'block', textAlign: 'center', background: 'linear-gradient(135deg, #10b981, #047857)',
                    color: '#fff', padding: '12px', borderRadius: 12, textDecoration: 'none', fontWeight: 700, fontSize: '0.95rem',
                  }}>Book with {trainer.name.split(' ')[0]}</Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
