"use client";
import { Kino, StickyHeader, Scene, Reveal, Marquee } from 'react-kino';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useEffect, useState } from 'react';
import api from '../../services/api';
import { getPublicAssetUrl } from '../../config/runtime';
import { Container } from '../../components/ui/Container';
import { SectionHeading } from '../../components/ui/SectionHeading';
import { SurfaceCard } from '../../components/ui/SurfaceCard';
import { ButtonLink } from '../../components/ui/ButtonLink';
import { KinoReveal } from '../../components/ui/KinoReveal';

interface ServiceItem {
  id: number | string;
  title: string;
  description: string;
  price: number;
  type: string;
}

export default function Landing() {
  const { user } = useAuth();
  const [services, setServices] = useState<ServiceItem[]>([]);
  const calEmbedUrl =
    (typeof window !== 'undefined' &&
      (window.WellnessSolutionsConfig as any)?.calEmbedUrl) ||
    // Replace this with your Cal.com embed URL when wiring the production config.
    'https://cal.com/';

  useEffect(() => {
    api.get('/classes/').then(res => {
      // De-duplicate by title for the landing display
      const seen = new Set();
      const unique = (res.data as ServiceItem[]).filter(s => {
        if (seen.has(s.title)) return false;
        seen.add(s.title);
        return true;
      });
      setServices(unique.slice(0, 3));
    }).catch(() => {
      // Fallback static services if API unavailable
      setServices([
        { id: 1, title: 'Assisted Stretching', description: 'One-on-one sessions with certified wellness practitioners to improve flexibility and reduce tension.', price: 85, type: 'wellness' },
        { id: 2, title: 'Wellness Programs', description: 'Group classes for all experience levels focusing on core strength, balance, and mind-body connection.', price: 45, type: 'wellness' },
        { id: 3, title: 'Personal Training', description: 'Personalized fitness sessions with certified trainers to achieve specific fitness goals.', price: 100, type: 'training' }
      ]);
    });
  }, []);

  return (
    <div style={{ backgroundColor: '#000', color: '#fff', minHeight: '100vh', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <Kino>
        <StickyHeader threshold={50} blur background="rgba(0,0,0,0.7)">
          <Container maxWidth={1400} style={{ padding: '14px 0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 14 }}>
              <Link to="/" style={{ fontWeight: 900, fontSize: 'clamp(1rem, 3vw, 1.15rem)', letterSpacing: '-0.03em', color: '#fff', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: 32, height: 32, background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', borderRadius: 10 }} />
                Wellness Solutions
              </Link>
              <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                {user ? (
                  <>
                    <ButtonLink to="/dashboard" variant="ghost">Dashboard</ButtonLink>
                    <ButtonLink to="/booking" variant="accent">Book a Session</ButtonLink>
                  </>
                ) : (
                  <>
                    <ButtonLink to="/login" variant="ghost">Log In</ButtonLink>
                    <ButtonLink to="/register" variant="accent">Book a Session</ButtonLink>
                  </>
                )}
              </div>
            </div>
          </Container>
        </StickyHeader>

        {/* Hero Section */}
        <Scene duration="100vh" pin={false}>
          <div
            style={{
              minHeight: '100vh',
              display: 'flex',
              alignItems: 'center',
              background: `radial-gradient(1200px 600px at 20% 20%, rgba(15,173,182,0.22), rgba(0,0,0,0) 55%), linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.86)), url(${getPublicAssetUrl('stretch-therapy.jpg')}) center/cover`,
              borderBottom: '1px solid #111',
            }}
          >
            <Container maxWidth={1240} style={{ padding: '120px 0 64px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: 28, alignItems: 'center' }}>
                <div>
                  <KinoReveal animation="fade-up" delay={120}>
                    <div style={{ color: '#d4d4d8', fontWeight: 800, letterSpacing: 1.2, textTransform: 'uppercase', fontSize: '0.82rem', marginBottom: 14 }}>
                      Corrective therapy • Assisted stretching • Functional movement
                    </div>
                  </KinoReveal>
                  <KinoReveal animation="fade-up" delay={220}>
                    <h1 style={{ fontSize: 'clamp(2.4rem, 6.8vw, 4.8rem)', margin: 0, fontWeight: 950, letterSpacing: '-0.05em', lineHeight: 1.02, maxWidth: 780 }}>
                      Transform your pain and inactivity to success and vitality
                    </h1>
                  </KinoReveal>
                  <KinoReveal animation="fade" delay={420}>
                    <p style={{ fontSize: 'clamp(1rem, 2.4vw, 1.25rem)', color: '#e4e4e7', marginTop: 18, lineHeight: 1.7, fontWeight: 520, maxWidth: 700 }}>
                      Premium, guided programmes for posture, mobility, and long-term performance. Assessment first, then a plan you can repeat and track.
                    </p>
                  </KinoReveal>

                  <KinoReveal animation="fade-up" delay={520}>
                    <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginTop: 22 }}>
                      <ButtonLink to="/booking" variant="accent">Book an Assessment</ButtonLink>
                      <ButtonLink to="/programmes" variant="secondary">Explore Programmes</ButtonLink>
                      <ButtonLink to="/corporate" variant="ghost">Corporate Wellness</ButtonLink>
                    </div>
                  </KinoReveal>

                  <KinoReveal animation="fade" delay={640}>
                    <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap', marginTop: 22, color: '#a1a1aa', fontSize: '0.95rem' }}>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 10 }}>
                        <span style={{ width: 8, height: 8, borderRadius: 99, background: 'var(--brand-accent)', boxShadow: '0 0 0 6px rgba(15,173,182,0.12)' }} />
                        Evidence-led methodology
                      </span>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 10 }}>
                        <span style={{ width: 8, height: 8, borderRadius: 99, background: '#fff', opacity: 0.9, boxShadow: '0 0 0 6px rgba(255,255,255,0.08)' }} />
                        Premium studio + corporate delivery
                      </span>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 10 }}>
                        <span style={{ width: 8, height: 8, borderRadius: 99, background: '#fbbf24', boxShadow: '0 0 0 6px rgba(251,191,36,0.12)' }} />
                        Trackable progress
                      </span>
                    </div>
                  </KinoReveal>
                </div>

                <KinoReveal animation="scale" delay={260}>
                  <SurfaceCard variant="glass" style={{ padding: 22 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, alignItems: 'baseline' }}>
                      <div style={{ fontWeight: 950, letterSpacing: '-0.03em', fontSize: '1.1rem' }}>What you get first</div>
                      <div style={{ color: '#a1a1aa', fontSize: '0.92rem' }}>~45–60 mins</div>
                    </div>
                    <div style={{ marginTop: 12, display: 'grid', gap: 10 }}>
                      {[
                        { t: 'Baseline assessment', d: 'Posture + mobility priorities.' },
                        { t: 'Corrective session', d: 'Immediate relief + targeted work.' },
                        { t: 'Programme plan', d: 'Repeatable routine for momentum.' },
                        { t: 'Next-step booking', d: 'Keep progress consistent.' },
                      ].map((row) => (
                        <div key={row.t} style={{ display: 'flex', gap: 12, padding: 12, borderRadius: 18, border: '1px solid rgba(255,255,255,0.10)', background: 'rgba(0,0,0,0.28)' }}>
                          <div style={{ width: 10, height: 10, borderRadius: 99, background: 'var(--brand-primary)', boxShadow: '0 0 0 6px rgba(15,173,182,0.10)', marginTop: 6 }} />
                          <div>
                            <div style={{ fontWeight: 900, color: '#e4e4e7' }}>{row.t}</div>
                            <div style={{ color: '#a1a1aa', fontSize: '0.95rem', lineHeight: 1.5 }}>{row.d}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div style={{ marginTop: 14, display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                      <ButtonLink to="/booking" variant="accent">Pick a Time</ButtonLink>
                      <ButtonLink to="/contact" variant="secondary">Ask a Question</ButtonLink>
                    </div>
                  </SurfaceCard>
                </KinoReveal>
              </div>
            </Container>
          </div>
        </Scene>

        {/* Trust strip */}
        <section style={{ padding: '22px 0', background: '#050505', borderBottom: '1px solid #111' }}>
          <Container maxWidth={1240}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 18, flexWrap: 'wrap' }}>
              <div style={{ color: '#a1a1aa', fontWeight: 800, letterSpacing: '-0.02em' }}>
                Trusted by teams and institutions
              </div>
              <div style={{ flex: '1 1 520px', minWidth: 280 }}>
                <Marquee speed={32} gap={28}>
                  {['Antarc Furniture', 'The Swedish Embassy', 'Farm Africa', 'Gertrude’s', 'AON', 'The Sweet December Scene'].map((name) => (
                    <span key={name} style={{ color: '#d4d4d8', fontWeight: 850, letterSpacing: '-0.02em', whiteSpace: 'nowrap' }}>
                      {name}
                    </span>
                  ))}
                </Marquee>
              </div>
              <div style={{ display: 'flex', gap: 14, color: '#a1a1aa', fontSize: '0.95rem', flexWrap: 'wrap' }}>
                <span>Secure checkout</span>
                <span>•</span>
                <span>Responsive booking</span>
                <span>•</span>
                <span>Clear outcomes</span>
              </div>
            </div>
          </Container>
        </section>

        {/* Corporate Wellness */}
        <section style={{ padding: '140px 20px', background: '#050505', display: 'flex', justifyContent: 'center', borderTop: '1px solid #1a1a1a' }}>
          <div style={{ maxWidth: '1300px', width: '100%', display: 'flex', flexWrap: 'wrap', gap: '60px', alignItems: 'center' }}>
            <div style={{ flex: '1 1 400px', maxWidth: '100%' }}>
              <Reveal animation="fade-up">
                <div style={{ color: 'var(--brand-primary)', fontWeight: 700, letterSpacing: '2px', textTransform: 'uppercase', marginBottom: '16px' }}>For Teams & Businesses</div>
                <h2 style={{ fontSize: 'clamp(2.5rem, 5vw, 4rem)', fontWeight: 800, margin: '0 0 24px', letterSpacing: '-0.03em', lineHeight: 1.1 }}>
                  Corporate Wellness Programs
                </h2>
              </Reveal>
              <Reveal animation="fade-up" delay={200}>
                <p style={{ color: '#a1a1aa', fontSize: '1.2rem', lineHeight: 1.6, marginBottom: '40px', maxWidth: '500px' }}>
                  Boost your team's productivity and well-being with our tailored corporate stretching and wellness programs. We bring our certified therapists directly to your office, or host your team at our premium studio.
                </p>
                <Link to="/corporate" style={{ display: 'inline-block', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '16px 36px', borderRadius: '99px', fontWeight: 600, textDecoration: 'none', transition: 'transform 0.2s, opacity 0.2s', fontSize: '1.1rem' }}
                  onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.opacity = '0.9'; }}
                  onMouseOut={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.opacity = '1'; }}>
                  Explore Corporate Rates
                </Link>
              </Reveal>
            </div>
            <div style={{ flex: '1 1 400px', maxWidth: '100%', position: 'relative' }}>
              <Reveal animation="scale" delay={200}>
                <div style={{ width: '100%', aspectRatio: '4/3', borderRadius: '24px', background: `url(${getPublicAssetUrl('team-building.jpg')}) center/cover`, boxShadow: '0 20px 60px rgba(0,0,0,0.5)', border: '1px solid #222' }}></div>
              </Reveal>
            </div>
          </div>
        </section>

        {/* Book Your Next Presentation */}
        <section style={{ padding: '90px 20px', background: '#070707', borderTop: '1px solid #111' }}>
          <div style={{ maxWidth: '1300px', margin: '0 auto', padding: '0 20px', display: 'flex', flexWrap: 'wrap', gap: '28px', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ flex: '1 1 520px' }}>
              <Reveal animation="fade-up">
                <div style={{ color: 'var(--brand-primary)', fontWeight: 700, letterSpacing: '2px', textTransform: 'uppercase', marginBottom: '14px', fontSize: '0.9rem' }}>
                  Book Your Next Presentation
                </div>
                <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.6rem)', fontWeight: 900, letterSpacing: '-0.04em', margin: '0 0 20px', lineHeight: 1.05 }}>
                  Wellness that moves people in real time
                </h2>
                <p style={{ color: '#a1a1aa', fontSize: '1.1rem', lineHeight: 1.7, marginBottom: '28px', maxWidth: 580 }}>
                  Need a corporate session, staff wellness briefing, or a client-facing presentation? Tell us your audience and we will propose a ready-to-deliver plan.
                </p>
              </Reveal>

              <Reveal animation="fade-up" delay={200}>
                <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
                  <ButtonLink to="/corporate" variant="accent">Request a Corporate Session →</ButtonLink>
                  <ButtonLink to="/contact" variant="secondary">Ask a Question</ButtonLink>
                </div>
              </Reveal>
            </div>

            <div style={{ flex: '1 1 420px', minWidth: 280 }}>
              <Reveal animation="scale" delay={200}>
                <div style={{ borderRadius: 24, border: '1px solid #222', background: '#0a0a0a', padding: 26, boxShadow: '0 20px 80px rgba(0,0,0,0.6)' }}>
                  <div style={{ color: '#d4d4d8', fontWeight: 800, letterSpacing: '-0.02em', fontSize: '1.2rem', marginBottom: 12 }}>
                    What we include
                  </div>
                  {[
                    'Custom stretching flow for your audience',
                    'On-site or virtual delivery options',
                    'Q&A + posture takeaways',
                    'Follow-up recommendations',
                  ].map((line) => (
                    <div key={line} style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10, color: '#a1a1aa' }}>
                      <span style={{ width: 10, height: 10, borderRadius: 99, background: 'var(--brand-accent)', boxShadow: '0 0 0 6px rgba(15,173,182,0.08)' }} />
                      <span style={{ fontSize: '0.98rem', lineHeight: 1.5 }}>{line}</span>
                    </div>
                  ))}
                </div>
              </Reveal>
            </div>
          </div>
        </section>

        {/* Featured outcomes / services (non-pinned) */}
        <section style={{ padding: '110px 0', background: '#0a0a0a', borderTop: '1px solid #111' }}>
          <Container maxWidth={1240}>
            <KinoReveal>
              <SectionHeading
                eyebrow="What we solve"
                title="Relief, alignment, and repeatable momentum."
                subtitle="No generic routines. We start with assessment, identify movement constraints, then build a programme you can execute consistently."
                align="center"
              />
            </KinoReveal>

            <div className="home-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: 16, marginTop: 34 }}>
              {[
                {
                  t: 'Posture & Foot Analysis',
                  d: 'Identify root causes and movement inefficiencies with a clear baseline.',
                },
                {
                  t: 'Corrective Therapy',
                  d: 'Targeted work to restore mobility, reduce tension, and improve control.',
                },
                {
                  t: 'Performance Programmes',
                  d: 'Repeatable routines and progress markers—built for consistency.',
                },
              ].map((card) => (
                <div key={card.t} style={{ gridColumn: 'span 4' }}>
                  <KinoReveal animation="fade-up">
                    <SurfaceCard variant="dark" style={{ height: '100%', padding: 24 }}>
                      <div style={{ fontWeight: 950, letterSpacing: '-0.03em', fontSize: '1.3rem' }}>{card.t}</div>
                      <div style={{ color: '#a1a1aa', marginTop: 10, lineHeight: 1.7 }}>{card.d}</div>
                      <div style={{ marginTop: 16, display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                        <ButtonLink to="/booking" variant="accent">Start with Assessment</ButtonLink>
                        <ButtonLink to="/services" variant="ghost">View Services</ButtonLink>
                      </div>
                    </SurfaceCard>
                  </KinoReveal>
                </div>
              ))}
            </div>
            <style dangerouslySetInnerHTML={{ __html: `@media (max-width: 960px){ .home-grid > div { grid-column: span 12 !important; } }` }} />
          </Container>
        </section>

        {/* Eskuri Shop Section */}
        <section style={{ padding: '120px 20px', background: '#0a0a0a', display: 'flex', justifyContent: 'center', borderTop: '1px solid #1a1a1a' }}>
          <div style={{ maxWidth: '1300px', width: '100%' }}>
            <div style={{ textAlign: 'center', marginBottom: '60px' }}>
              <Reveal animation="fade-up">
                <div style={{ color: 'var(--brand-primary)', fontWeight: 700, letterSpacing: '2px', textTransform: 'uppercase', marginBottom: '16px', fontSize: '0.85rem' }}>Eskuri by Wellness Solutions Kenya</div>
                <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: 0 }}>Move Naturally. Live Better.</h2>
              </Reveal>
              <Reveal animation="fade-up" delay={200}>
                <p style={{ color: '#888', fontSize: '1.2rem', marginTop: '16px', maxWidth: '640px', margin: '16px auto 0', lineHeight: 1.6 }}>
                  Naturally crafted barefoot footwear designed for freedom of movement, comfort, and an active lifestyle.
                </p>
              </Reveal>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px' }}>
              {[
                { name: "White Eskuri Barefoot Shoes", subtitle: "With Yellow Accents", url: "https://eskuribarefoot.africa/products/white-eskuri-barefoot-shoes", img: getPublicAssetUrl('personal-training.jpg'), tag: "Featured" },
                { name: "Black Eskuri Barefoot Shoes", subtitle: "With White Accents", url: "https://eskuribarefoot.africa/products/black-eskuri-barefoot-shoes-with-white-accents", img: getPublicAssetUrl('wellness.jpg') },
                { name: "Moonlight Blue", subtitle: "With White Accents", url: "https://eskuribarefoot.africa/products/moonlight-blue-with-white-accents", img: getPublicAssetUrl('biometric-tests.jpg'), tag: "New" },
                { name: "Khaki / Beige", subtitle: "Eskuri Barefoot Shoes", url: "https://eskuribarefoot.africa/products/khaki-beige-bare-foot-shoes", img: getPublicAssetUrl('stretch-therapy.jpg') }
              ].map((item, i) => (
                <Reveal key={i} animation="fade-up" delay={i * 100}>
                  <div style={{ position: 'relative', borderRadius: '24px', overflow: 'hidden', border: '1px solid #222', height: '400px', background: `url(${item.img}) center/cover`, display: 'flex', flexDirection: 'column', justifyContent: 'flex-end' }}>
                    <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, var(--soft-dark) 0%, rgba(0,0,0,0) 65%)' }}></div>
                    {item.tag && (
                      <div style={{ position: 'absolute', top: '20px', right: '20px', background: 'var(--brand-accent)', color: '#000', padding: '6px 12px', borderRadius: '99px', fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px', backdropFilter: 'blur(4px)' }}>
                        {item.tag}
                      </div>
                    )}
                    <div style={{ position: 'relative', zIndex: 2, padding: '32px' }}>
                      <div style={{ fontSize: '0.8rem', color: 'var(--brand-primary)', fontWeight: 600, letterSpacing: '1px', textTransform: 'uppercase', marginBottom: '6px' }}>Eskuri</div>
                      <h3 style={{ fontSize: '1.4rem', fontWeight: 700, margin: '0 0 4px', color: '#fff' }}>{item.name}</h3>
                      <div style={{ fontSize: '0.9rem', color: '#a1a1aa', marginBottom: '20px' }}>{item.subtitle}</div>
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ display: 'inline-block', padding: '10px 24px', borderRadius: '99px', background: 'rgba(255,255,255,0.1)', color: '#fff', fontWeight: 600, textDecoration: 'none', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.2)', transition: 'all 0.2s', fontSize: '0.95rem' }}
                        onMouseOver={e => { (e.currentTarget as HTMLAnchorElement).style.background = '#fff'; (e.currentTarget as HTMLAnchorElement).style.color = '#000'; }}
                        onMouseOut={e => { (e.currentTarget as HTMLAnchorElement).style.background = 'rgba(255,255,255,0.1)'; (e.currentTarget as HTMLAnchorElement).style.color = '#fff'; }}
                      >
                        Shop Now ↗
                      </a>
                    </div>
                  </div>
                </Reveal>
              ))}
            </div>

            {/* Section-level CTA */}
            <Reveal animation="fade-up" delay={400}>
              <div style={{ textAlign: 'center', marginTop: '52px' }}>
                <a
                  href="https://eskuribarefoot.africa/collections/all"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '16px 40px', borderRadius: '99px', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', fontWeight: 700, textDecoration: 'none', fontSize: '1.05rem', letterSpacing: '-0.01em', transition: 'opacity 0.2s, transform 0.2s' }}
                  onMouseOver={e => { (e.currentTarget as HTMLAnchorElement).style.opacity = '0.88'; (e.currentTarget as HTMLAnchorElement).style.transform = 'translateY(-2px)'; }}
                  onMouseOut={e => { (e.currentTarget as HTMLAnchorElement).style.opacity = '1'; (e.currentTarget as HTMLAnchorElement).style.transform = 'translateY(0)'; }}
                >
                  Explore All Styles at eskuribarefoot.africa ↗
                </a>
              </div>
            </Reveal>
          </div>
        </section>

        {/* Premium Results + Calendar */}
        <Scene duration="120vh" pin={false}>
          {() => (
            <section
              style={{
                padding: '110px 0',
                background: '#000',
                borderTop: '1px solid #111',
              }}
            >
              <Container maxWidth={1240}>
                <KinoReveal>
                  <SectionHeading
                    eyebrow="How results happen"
                    title="See the difference across sessions."
                    subtitle="We combine assessment, targeted therapy, and a repeatable plan—then keep the experience frictionless with premium booking."
                    align="center"
                  />
                </KinoReveal>

                <div
                  style={{
                    width: '100%',
                    display: 'grid',
                    gridTemplateColumns: '1.05fr 0.95fr',
                    gap: 20,
                    alignItems: 'stretch',
                    marginTop: 34,
                  }}
                >
                  <KinoReveal animation="fade-up">
                    <div
                      style={{
                        background: 'linear-gradient(135deg, rgba(15,173,182,0.16) 0%, rgba(0,0,0,0) 55%), #0a0a0a',
                        border: '1px solid #222',
                        borderRadius: 28,
                        padding: 26,
                        boxShadow: '0 30px 90px rgba(0,0,0,0.7)',
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'space-between',
                        gap: 18,
                      }}
                    >
                    <div>
                      <div style={{ color: 'var(--brand-primary)', fontWeight: 900, letterSpacing: 2, textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: 10 }}>
                        What makes it premium
                      </div>
                      <div style={{ fontSize: '2rem', fontWeight: 950, marginBottom: 10, letterSpacing: '-0.03em' }}>
                        Clinical clarity. Real progress.
                      </div>
                      <div style={{ color: '#a1a1aa', lineHeight: 1.7, fontSize: '1.05rem', marginBottom: 14 }}>
                        We design programmes around your body—then you track your improvement across sessions.
                      </div>

                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                        {[
                          { label: 'Assessment first', value: 'Personalised baseline' },
                          { label: 'Guided sessions', value: 'Corrective therapy' },
                          { label: 'Programme plan', value: 'Repeatable routines' },
                          { label: 'Next bookings', value: 'Keep momentum' },
                        ].map((item) => (
                          <div
                            key={item.label}
                            style={{
                              background: 'rgba(255,255,255,0.04)',
                              border: '1px solid rgba(255,255,255,0.08)',
                              borderRadius: 20,
                              padding: 14,
                            }}
                          >
                            <div style={{ color: '#d4d4d8', fontWeight: 900, fontSize: '0.95rem', marginBottom: 6 }}>
                              {item.label}
                            </div>
                            <div style={{ color: '#a1a1aa', fontSize: '0.92rem', lineHeight: 1.5 }}>
                              {item.value}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                      <ButtonLink to="/booking" variant="accent">Book an Assessment →</ButtonLink>
                      <ButtonLink to="/programmes" variant="secondary">View Programmes</ButtonLink>
                    </div>
                  </div>
                  </KinoReveal>

                  <KinoReveal animation="fade-up" delay={150}>
                  <div
                    style={{
                      background: 'rgba(255,255,255,0.03)',
                      border: '1px solid #222',
                      borderRadius: 28,
                      padding: 20,
                      height: '100%',
                      boxShadow: '0 30px 90px rgba(0,0,0,0.55)',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: 14,
                    }}
                  >
                    <div>
                      <div style={{ color: '#d4d4d8', fontWeight: 900, fontSize: '1.05rem', marginBottom: 6 }}>
                        Pick your time
                      </div>
                      <div style={{ color: '#a1a1aa', lineHeight: 1.6 }}>
                        Use the calendar below to schedule an assessment or session.
                      </div>
                    </div>

                    <div style={{ flex: 1, minHeight: 340, borderRadius: 20, overflow: 'hidden', border: '1px solid rgba(255,255,255,0.10)', background: '#050505' }}>
                      <iframe
                        title="Cal.com booking calendar"
                        src={calEmbedUrl}
                        style={{ width: '100%', height: '100%', border: 0, background: '#050505' }}
                        loading="lazy"
                        referrerPolicy="no-referrer-when-downgrade"
                      />
                    </div>

                    <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                      <ButtonLink to="/booking" variant="ghost" style={{ flex: '1 1 180px', justifyContent: 'center' as const }}>
                        Open Booking Page →
                      </ButtonLink>
                      <a
                        href={calEmbedUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          background: 'rgba(255,255,255,0.06)',
                          border: '1px solid rgba(255,255,255,0.14)',
                          color: '#fff',
                          padding: '12px 14px',
                          borderRadius: 14,
                          textDecoration: 'none',
                          fontWeight: 900,
                          flex: '1 1 180px',
                        }}
                      >
                        Launch Calendar ↗
                      </a>
                    </div>
                  </div>
                  </KinoReveal>
                </div>
                <style dangerouslySetInnerHTML={{ __html: `@media (max-width: 980px){ .premium-grid { grid-template-columns: 1fr !important; } }` }} />
              </Container>
            </section>
          )}
        </Scene>

        {/* Method + proof artifact + FAQ */}
        <section style={{ padding: '110px 0', background: '#050505', borderTop: '1px solid #111' }}>
          <Container maxWidth={1240}>
            <KinoReveal>
              <SectionHeading
                eyebrow="Methodology"
                title="A simple system that compounds."
                subtitle="You’re not buying a session—you’re buying a repeatable process that makes your body more capable over time."
              />
            </KinoReveal>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: 16, marginTop: 28 }}>
              {[
                { n: '01', t: 'Assess', d: 'Posture, mobility, and constraints—so the plan is specific.' },
                { n: '02', t: 'Correct', d: 'Targeted therapy to remove pain drivers and restore range.' },
                { n: '03', t: 'Build', d: 'Strength + movement patterns to keep the gains.' },
                { n: '04', t: 'Track', d: 'Progress markers so improvement is visible, not assumed.' },
              ].map((s) => (
                <div key={s.n} style={{ gridColumn: 'span 3' }}>
                  <KinoReveal animation="fade-up">
                    <SurfaceCard variant="glass" style={{ height: '100%', padding: 22 }}>
                      <div style={{ color: '#a1a1aa', fontWeight: 900, letterSpacing: 1.2 }}>{s.n}</div>
                      <div style={{ fontWeight: 950, fontSize: '1.25rem', letterSpacing: '-0.03em', marginTop: 10 }}>{s.t}</div>
                      <div style={{ color: '#a1a1aa', marginTop: 10, lineHeight: 1.7 }}>{s.d}</div>
                    </SurfaceCard>
                  </KinoReveal>
                </div>
              ))}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1.05fr 0.95fr', gap: 16, marginTop: 24, alignItems: 'stretch' }}>
              <KinoReveal animation="fade-up">
                <SurfaceCard variant="dark" style={{ padding: 26, height: '100%' }}>
                  <div style={{ color: 'var(--brand-primary)', fontWeight: 950, letterSpacing: 2, textTransform: 'uppercase', fontSize: '0.85rem' }}>
                    Proof artifact (preview)
                  </div>
                  <div style={{ fontWeight: 950, letterSpacing: '-0.04em', fontSize: '1.9rem', marginTop: 10 }}>
                    Your programme summary, simplified.
                  </div>
                  <div style={{ color: '#a1a1aa', lineHeight: 1.7, marginTop: 12 }}>
                    We turn your assessment into a clear plan: what to fix, what to strengthen, what to avoid, and what “better” looks like.
                  </div>
                  <div style={{ marginTop: 18, display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                    <ButtonLink to="/booking" variant="accent">Get your baseline →</ButtonLink>
                    <ButtonLink to="/contact" variant="secondary">Ask about your situation</ButtonLink>
                  </div>
                </SurfaceCard>
              </KinoReveal>

              <KinoReveal animation="fade-up" delay={120}>
                <SurfaceCard variant="glass" style={{ padding: 22, height: '100%' }}>
                  <div style={{ fontWeight: 950, letterSpacing: '-0.03em', fontSize: '1.2rem' }}>
                    Common questions
                  </div>
                  <div style={{ marginTop: 12, display: 'grid', gap: 10 }}>
                    {[
                      { q: 'Do I need to be “fit” to start?', a: 'No. We tailor intensity to your baseline and progress safely.' },
                      { q: 'Is this just stretching?', a: 'No. We combine assessment, therapy, and corrective movement.' },
                      { q: 'How soon do people feel change?', a: 'Many feel relief early—durable change comes from consistency.' },
                      { q: 'Can you support teams?', a: 'Yes—on-site or hosted sessions with a repeatable plan.' },
                    ].map((row) => (
                      <div key={row.q} style={{ borderRadius: 18, border: '1px solid rgba(255,255,255,0.10)', background: 'rgba(0,0,0,0.25)', padding: 14 }}>
                        <div style={{ color: '#e4e4e7', fontWeight: 900 }}>{row.q}</div>
                        <div style={{ color: '#a1a1aa', marginTop: 6, lineHeight: 1.6 }}>{row.a}</div>
                      </div>
                    ))}
                  </div>
                </SurfaceCard>
              </KinoReveal>
            </div>
          </Container>
        </section>

        {/* Static Testimonials */}
        <section style={{ padding: '120px 20px', background: '#0a0a0a', display: 'flex', justifyContent: 'center', borderTop: '1px solid #111', borderBottom: '1px solid #111' }}>
          <div style={{ maxWidth: '1300px', width: '100%' }}>
            <div style={{ textAlign: 'center', marginBottom: '60px' }}>
              <Reveal animation="fade-up">
                <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: 0 }}>Real Client Results</h2>
              </Reveal>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
              {[
                { quote: "Wellness Solutions has been a game-changer for my chronic back pain. The instructors are knowledgeable and the atmosphere is so welcoming!", author: "Alex Johnson", role: "Member since 2022" },
                { quote: "As a marathon runner, proper recovery is essential. Their assisted stretch therapy has significantly reduced my injury rate and improved my race times.", author: "Sarah Jenkins", role: "Competitive Athlete" },
                { quote: "I sit at a desk for 10 hours a day. Taking their wellness programs has completely fixed my posture and reduced my daily tension headaches.", author: "Michael Chen", role: "Software Engineer" }
              ].map((t, i) => (
                <Reveal key={i} animation="fade-up" delay={i * 150}>
                  <div style={{ background: 'var(--dark)', padding: '40px', borderRadius: '24px', border: '1px solid #222', height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <div style={{ color: 'var(--brand-primary)', fontSize: '2rem', marginBottom: '16px', lineHeight: 1 }}>"</div>
                    <p style={{ fontSize: '1.1rem', lineHeight: 1.6, color: '#e4e4e7', flex: 1, margin: '0 0 24px' }}>{t.quote}</p>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                      <div style={{ width: '48px', height: '48px', borderRadius: '24px', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '1.2rem' }}>
                        {t.author.charAt(0)}
                      </div>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{t.author}</div>
                        <div style={{ color: '#888', fontSize: '0.9rem' }}>{t.role}</div>
                      </div>
                    </div>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* Final CTA Section */}
        <section style={{ padding: '100px 20px', background: 'linear-gradient(180deg, #0a0a0a 0%, #000 100%)', textAlign: 'center', borderTop: '1px solid #111' }}>
          <Reveal animation="fade-up">
            <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 800, marginBottom: '24px' }}>Ready to feel your best?</h2>
            <p style={{ color: '#888', fontSize: '1.25rem', maxWidth: '600px', margin: '0 auto 40px', lineHeight: 1.6 }}>Join hundreds of clients who have transformed their mobility and eliminated pain.</p>
            <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <ButtonLink to="/booking" variant="accent" style={{ padding: '18px 40px', fontSize: '1.05rem', fontWeight: 950 }}>Book Your First Session</ButtonLink>
              <ButtonLink to="/programmes" variant="secondary" style={{ padding: '18px 40px', fontSize: '1.05rem', fontWeight: 950 }}>View Programmes</ButtonLink>
            </div>
          </Reveal>
        </section>

        {/* Footer */}
        <footer style={{ padding: '80px 20px 40px', background: '#000', borderTop: '1px solid #1a1a1a' }}>
          <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '60px', marginBottom: '60px' }}>
              <div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div style={{ width: '32px', height: '32px', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', borderRadius: '8px' }}></div>
                  Wellness Solutions
                </div>
                <p style={{ color: '#888', lineHeight: 1.6, marginBottom: '24px' }}>
                  Premium assisted stretching and functional recovery studio. We help you move better, live longer, and perform at your peak.
                </p>
                <div style={{ display: 'flex', gap: '12px' }}>
                  {['Instagram', 'Twitter', 'Facebook'].map(s => (
                    <div key={s} style={{ width: '40px', height: '40px', borderRadius: '20px', background: '#111', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', border: '1px solid #222' }}>{s[0]}</div>
                  ))}
                </div>
              </div>

              <div>
                <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '24px', textTransform: 'uppercase', letterSpacing: '1px' }}>Quick Links</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {["About Us", "Services", "Shop", "Blog", "Contact", "Corporate"].map(l => (
                    <Link key={l} to={`/${l.toLowerCase().replace(' ', '')}`} style={{ color: '#666', textDecoration: 'none', transition: 'color 0.2s' }} onMouseOver={e => e.currentTarget.style.color = '#fff'} onMouseOut={e => e.currentTarget.style.color = '#666'}>{l}</Link>
                  ))}
                </div>
              </div>

              <div style={{ gridColumn: 'span 2' }}>
                <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '24px', textTransform: 'uppercase', letterSpacing: '1px' }}>Stay Updated</h4>
                <p style={{ color: '#888', marginBottom: '20px' }}>Subscribe to our wellness newsletter for mobility tips and studio updates.</p>
                <div style={{ display: 'flex', gap: '10px', background: '#111', padding: '6px', borderRadius: '14px', border: '1px solid #222' }}>
                  <input type="email" placeholder="your@email.com" style={{ flex: 1, background: 'transparent', border: 'none', padding: '12px 16px', color: '#fff', outline: 'none' }} />
                  <button onClick={() => alert('Thanks for subscribing!')} style={{ background: '#fff', color: '#000', border: 'none', padding: '12px 24px', borderRadius: '10px', fontWeight: 700, cursor: 'pointer' }}>Join</button>
                </div>
              </div>
            </div>

            <div style={{ borderTop: '1px solid #111', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px', paddingTop: '40px' }}>
              <p style={{ color: '#444', margin: 0, fontSize: '0.9rem' }}>© 2026 Wellness Solutions. All rights reserved.</p>
              <div style={{ display: 'flex', gap: '24px' }}>
                <Link to="/privacy" style={{ color: '#444', textDecoration: 'none', fontSize: '0.9rem' }}>Privacy</Link>
                  <Link to="/terms" style={{ color: '#444', textDecoration: 'none', fontSize: '0.9rem' }}>Terms</Link>
                <Link to="/contact" style={{ color: '#444', textDecoration: 'none', fontSize: '0.9rem' }}>Support</Link>
              </div>
            </div>
            <div style={{ textAlign: 'center', marginTop: '24px', paddingTop: '20px', borderTop: '1px solid #0d0d0d' }}>
              <p style={{ color: '#2a2a2a', margin: 0, fontSize: '0.8rem', letterSpacing: '0.02em' }}>
                Wellness Solutions is a product of{' '}
                <a href="https://eskuribarefoot.africa" target="_blank" rel="noopener noreferrer" style={{ color: '#2a2a2a', textDecoration: 'underline', textUnderlineOffset: '3px' }}>Wellness Solutions Kenya</a>
              </p>
            </div>
          </div>
        </footer>

      </Kino>
    </div>
  );
}
