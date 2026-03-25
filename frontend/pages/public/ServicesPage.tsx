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
  type: string;
}

export default function ServicesPage() {
  const { user } = useAuth();
  const [services, setServices] = useState<ClassItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/classes/').then(res => {
      // De-duplicate by title
      const seen = new Set<string>();
      const unique = (res.data as ClassItem[]).filter(s => { if (seen.has(s.title)) return false; seen.add(s.title); return true; });
      setServices(unique);
    }).catch(() => {
      setServices([
        { id: 1, title: 'Assisted Stretching', description: 'One-on-one sessions with certified wellness practitioners to improve flexibility and reduce tension.', price: 85, type: 'wellness' },
        { id: 2, title: 'Wellness Programs', description: 'Group and solo classes for all experience levels focusing on core strength, balance, and mind-body connection.', price: 45, type: 'wellness' },
        { id: 3, title: 'Personal Training', description: 'Customized fitness sessions designed around your goals with certified personal trainers.', price: 120, type: 'training' },
        { id: 4, title: 'Corporate Wellness', description: 'On-site wellness programs to boost your team productivity and well-being.', price: 0, type: 'corporate' },
      ]);
    }).finally(() => setLoading(false));
  }, []);

  const images: Record<string, string> = { 
    stretch: `${api.defaults.baseURL?.replace('/api', '')}/static/images/personal-training.jpg`, 
    wellness: `${api.defaults.baseURL?.replace('/api', '')}/static/images/wellness.jpg`, 
    training: `${api.defaults.baseURL?.replace('/api', '')}/static/images/ergonomics.jpg`,
    corporate: `${api.defaults.baseURL?.replace('/api', '')}/static/images/team-building.jpg`
  };

  return (
    <div style={{ minHeight: '100vh', background: '#000', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <header style={{ padding: '20px 24px', borderBottom: '1px solid #111', display: 'flex', justifyContent: 'space-between', alignItems: 'center', position: 'sticky', top: 0, background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(10px)', zIndex: 10 }}>
        <Link to="/" style={{ fontWeight: 800, fontSize: '1.1rem', color: '#fff', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{ width: 28, height: 28, background: 'linear-gradient(135deg, #10b981, #047857)', borderRadius: 7 }} />Wellness Solutions
        </Link>
        <Link to={user ? '/booking' : '/register'} style={{ background: 'linear-gradient(135deg, #10b981, #047857)', color: '#fff', padding: '10px 20px', borderRadius: 10, textDecoration: 'none', fontWeight: 700, fontSize: '0.9rem' }}>
          {user ? 'Book Now' : 'Get Started'}
        </Link>
      </header>

      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '60px 20px' }}>
        <Reveal animation="fade-up">
          <div style={{ textAlign: 'center', marginBottom: 60 }}>
            <h1 style={{ fontSize: 'clamp(2rem, 5vw, 4rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 20px' }}>Our Services</h1>
            <p style={{ color: '#888', fontSize: '1.2rem', maxWidth: 600, margin: '0 auto' }}>Expert-led sessions designed to improve your mobility, strength, and overall well-being.</p>
          </div>
        </Reveal>

        {loading ? (
          <div style={{ textAlign: 'center', color: '#555', padding: '80px 0' }}>Loading services...</div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 28 }}>
            {services.map((s, i) => (
              <Reveal key={s.id} animation="fade-up" delay={i * 100}>
                <div style={{ background: 'linear-gradient(145deg, #111 0%, #0a0a0a 100%)', border: '1px solid #1a1a1a', borderRadius: 24, overflow: 'hidden', height: '100%', display: 'flex', flexDirection: 'column', transition: 'transform 0.3s, border-color 0.3s' }}
                  onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-6px)'; e.currentTarget.style.borderColor = '#222'; }}
                  onMouseOut={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = '#1a1a1a'; }}>
                  <div style={{ height: 240, background: `url(${images[s.type] || images.stretch}) center/cover`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  </div>
                  <div style={{ padding: 32, flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <div style={{ color: '#10b981', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 12 }}>
                      {s.price > 0 ? `From $${s.price}` : 'Contact for pricing'}
                    </div>
                    <h3 style={{ fontWeight: 800, fontSize: '1.5rem', margin: '0 0 16px', letterSpacing: '-0.02em' }}>{s.title}</h3>
                    <p style={{ color: '#888', lineHeight: 1.7, flex: 1, margin: '0 0 24px' }}>{s.description}</p>
                    <Link to={user ? '/booking' : '/register'} style={{ display: 'inline-block', background: 'linear-gradient(135deg, #10b981, #047857)', color: '#fff', padding: '12px 24px', borderRadius: 12, textDecoration: 'none', fontWeight: 700, textAlign: 'center' }}>
                      {user ? 'Book This Service' : 'Get Started →'}
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
