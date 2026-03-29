"use client";
import { Kino, StickyHeader, Scene, Reveal, CompareSlider, Marquee, TextReveal, ScrollTransform, Progress } from 'react-kino';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useEffect, useState } from 'react';
import api from '../../services/api';
import { getPublicAssetUrl } from '../../config/runtime';

interface ServiceItem {
  id: number | string;
  title: string;
  description: string;
  price: number;
  type: string;
}

const btnPrimary = { background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '10px 20px', borderRadius: 99, fontWeight: 600, textDecoration: 'none', border: 'none', cursor: 'pointer', display: 'inline-block', textAlign: 'center' as const };
const btnSecondary = { background: 'rgba(255,255,255,0.08)', color: '#fff', padding: '10px 20px', borderRadius: 99, fontWeight: 600, textDecoration: 'none', border: '1px solid rgba(255,255,255,0.15)', cursor: 'pointer', display: 'inline-block', textAlign: 'center' as const, backdropFilter: 'blur(8px)' };

export default function Landing() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [services, setServices] = useState<ServiceItem[]>([]);

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
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '16px 24px', alignItems: 'center', maxWidth: '1400px', margin: '0 auto' }}>
            <Link to="/" style={{ fontWeight: 800, fontSize: 'clamp(1rem, 3vw, 1.2rem)', letterSpacing: '-0.02em', color: '#fff', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ width: '32px', height: '32px', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', borderRadius: '8px' }}></div>
              Wellness Solutions
            </Link>
            <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
              {user ? (
                <>
                  <Link to="/dashboard" style={btnSecondary}>Dashboard</Link>
                  <Link to="/booking" style={{ ...btnPrimary, background: '#fff', color: '#000' }}>Book a Session</Link>
                </>
              ) : (
                <>
                  <Link to="/login" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '0.9rem', padding: '10px' }}>Log In</Link>
                  <Link to="/register" style={{ ...btnPrimary, background: '#fff', color: '#000' }}>Book a Session</Link>
                </>
              )}
            </div>
          </div>
        </StickyHeader>

        {/* Hero Section */}
        <Scene duration="100vh" pin={false}>
          <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: '20px', background: `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.8)), url(${getPublicAssetUrl('stretch-therapy.jpg')}) center/cover` }}>
            <Reveal animation="fade-up" delay={200}>
              <h1 style={{ fontSize: 'clamp(2.5rem, 8vw, 6rem)', margin: 0, fontWeight: 800, letterSpacing: '-0.04em', lineHeight: 1.1, background: 'linear-gradient(180deg, #fff 0%, #d4d4d8 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', maxWidth: '900px' }}>
                Rejuvenate Your Body,<br />Restore Your Mind
              </h1>
            </Reveal>
            <Reveal animation="fade" delay={600}>
              <p style={{ fontSize: 'clamp(1rem, 3vw, 1.5rem)', color: '#e4e4e7', marginTop: '32px', maxWidth: '700px', lineHeight: 1.6, fontWeight: 500, textShadow: '0 2px 10px rgba(0,0,0,0.5)' }}>
                Welcome to Wellness Solutions, your sanctuary for assisted stretching, functional fitness, and complete wellness.
              </p>
            </Reveal>
          </div>
        </Scene>

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
              <Reveal animation="zoom-in" delay={200}>
                <div style={{ width: '100%', aspectRatio: '4/3', borderRadius: '24px', background: `url(${getPublicAssetUrl('team-building.jpg')}) center/cover`, boxShadow: '0 20px 60px rgba(0,0,0,0.5)', border: '1px solid #222' }}></div>
              </Reveal>
            </div>
          </div>
        </section>

        {/* Services Section */}
        <Scene duration="250vh" pin={true}>
          {(progress) => (
            <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#111', position: 'relative', overflow: 'hidden' }}>
              <div className="services-container" style={{ maxWidth: '1300px', width: '100%', padding: '20px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '32px', position: 'relative', zIndex: 2, maxHeight: '100vh', overflowY: 'auto', scrollbarWidth: 'none', msOverflowStyle: 'none' }}>
                <style dangerouslySetInnerHTML={{
                  __html: `
                  .services-container::-webkit-scrollbar { display: none; }
                  @media (max-width: 768px) { .services-container { padding-top: 120px !important; padding-bottom: 80px !important; } }
                `}} />
                <div style={{ gridColumn: '1 / -1', textAlign: 'center', margin: '40px 0 20px' }}>
                  <Reveal progress={progress} at={0.05} animation="fade-up">
                    <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 800, margin: 0, letterSpacing: '-0.03em' }}>Our Services</h2>
                  </Reveal>
                </div>

                {[
                  { title: "Postural & Foot Analysis", desc: "Precision assessment of body alignment and gait to identify the root causes of physical imbalance, discomfort, and movement inefficiency.", at: 0.15, img: getPublicAssetUrl('personal-training.jpg') },
                  { title: "Corrective Exercise Therapy", desc: "Targeted, personalized movement programs that restore functional mobility, correct structural imbalances, and reduce chronic tension and pain.", at: 0.35, img: getPublicAssetUrl('wellness.jpg') },
                  { title: "Injury Prevention & Wellness", desc: "Educational workshops and comprehensive programs covering ergonomics, nutritional guidance, and injury prevention for individuals and organizations.", at: 0.55, img: getPublicAssetUrl('ergonomics.jpg') }
                ].map((service, i) => (
                  <Reveal key={i} progress={progress} at={service.at} animation="fade-up">
                    <div
                      onClick={() => navigate('/services')}
                      style={{ background: 'linear-gradient(145deg, #1a1a1a 0%, #0a0a0a 100%)', borderRadius: '24px', border: '1px solid #222', height: '100%', overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,0.5)', display: 'flex', flexDirection: 'column', cursor: 'pointer', transition: 'transform 0.3s' }}
                      onMouseOver={e => e.currentTarget.style.transform = 'scale(1.02)'}
                      onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
                    >
                      <div style={{ height: '240px', width: '100%', background: `url(${service.img}) center/cover` }}></div>
                      <div style={{ padding: '36px', display: 'flex', flexDirection: 'column', flex: 1 }}>
                        <h3 style={{ fontSize: '1.75rem', marginBottom: '16px', fontWeight: 700, color: '#fff', letterSpacing: '-0.02em' }}>{service.title}</h3>
                        <p style={{ color: '#a1a1aa', lineHeight: 1.6, fontSize: '1.1rem', margin: '0 0 24px', flex: 1 }}>{service.desc}</p>
                        <div style={{ color: 'var(--brand-primary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: 8 }}>View Details →</div>
                      </div>
                    </div>
                  </Reveal>
                ))}
              </div>
            </div>
          )}
        </Scene>

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

        {/* Before / After Comparison */}
        <Scene duration="150vh" pin={true}>
          {(progress) => (
            <section style={{ height: '100vh', padding: '40px 20px', background: '#000', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
              <div style={{ textAlign: 'center', marginBottom: '40px', maxWidth: '700px' }}>
                <Reveal progress={progress} at={0.05} animation="fade-up">
                  <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: 0 }}>See the Difference</h2>
                </Reveal>
                <Reveal progress={progress} at={0.1} animation="fade-up">
                  <p style={{ color: '#a1a1aa', fontSize: 'clamp(1rem, 3vw, 1.25rem)', marginTop: '16px', lineHeight: 1.6 }}>
                    Our clients experience noticeable improvements in their posture, flexibility, and overall mobility after just one session.
                  </p>
                </Reveal>
              </div>

              <Reveal progress={progress} at={0.15} animation="zoom-in">
                <div style={{ width: '100%', minWidth: '300px', maxWidth: '1000px', aspectRatio: '16/9', minHeight: '300px', borderRadius: '24px', overflow: 'hidden', border: '1px solid #222', boxShadow: '0 20px 80px rgba(0,0,0,0.8)' }}>
                  <CompareSlider
                    scrollDriven={true}
                    progress={Math.max(0, Math.min(1, (progress - 0.2) * 1.5))}
                    before={
                      <div style={{ width: '100%', height: '100%', background: 'linear-gradient(135deg, #1e1e1e 0%, #000 100%)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px', textAlign: 'center' }}>
                        <div style={{ fontSize: 'clamp(2.5rem, 6vw, 4rem)', marginBottom: '16px', opacity: 0.5 }}>😫</div>
                        <h3 style={{ fontSize: 'clamp(1.5rem, 4vw, 2.5rem)', color: '#fff', margin: 0, fontWeight: 700 }}>Before Therapy</h3>
                        <ul style={{ color: '#a1a1aa', fontSize: 'clamp(0.9rem, 2vw, 1.2rem)', marginTop: '24px', listStyle: 'none', padding: 0, lineHeight: 2, fontWeight: 500 }}>
                          <li><span style={{ color: '#ef4444', marginRight: '12px' }}>✕</span> Limited mobility</li>
                          <li><span style={{ color: '#ef4444', marginRight: '12px' }}>✕</span> Poor posture</li>
                          <li><span style={{ color: '#ef4444', marginRight: '12px' }}>✕</span> Chronic tension</li>
                        </ul>
                      </div>
                    }
                    after={
                      <div style={{ width: '100%', height: '100%', background: 'linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px', textAlign: 'center' }}>
                        <div style={{ fontSize: 'clamp(2.5rem, 6vw, 4rem)', marginBottom: '16px' }}>😎</div>
                        <h3 style={{ fontSize: 'clamp(1.5rem, 4vw, 2.5rem)', color: '#fff', margin: 0, fontWeight: 700 }}>After Therapy</h3>
                        <ul style={{ color: '#fff', fontSize: 'clamp(0.9rem, 2vw, 1.2rem)', marginTop: '24px', listStyle: 'none', padding: 0, lineHeight: 2, fontWeight: 500 }}>
                          <li><span style={{ color: 'var(--brand-accent)', marginRight: '12px' }}>✓</span> Improved flexibility</li>
                          <li><span style={{ color: 'var(--brand-accent)', marginRight: '12px' }}>✓</span> Better posture</li>
                          <li><span style={{ color: 'var(--brand-accent)', marginRight: '12px' }}>✓</span> Reduced tension</li>
                        </ul>
                      </div>
                    }
                  />
                </div>
              </Reveal>
            </section>
          )}
        </Scene>

        {/* Partners Marquee */}
        <section style={{ padding: '80px 0', background: '#050505', overflow: 'hidden', borderTop: '1px solid #111' }}>
          <Reveal animation="fade-up">
            <h2 style={{ fontSize: 'clamp(1.5rem, 3vw, 2.5rem)', fontWeight: 700, color: '#888', textAlign: 'center', marginBottom: '40px', letterSpacing: '-0.03em', padding: '0 20px' }}>
              Organizations We've Worked With
            </h2>
          </Reveal>

          <Marquee speed={30} gap={32}>
            {[
              "Elite Runners Club", "TechCorp Wellness", "City Police Department",
              "National Gymnastics Team", "Local Fire Station", "University Athletics",
              "Corporate Finance Group", "Regional Hospital Staff"
            ].map((text, i) => (
              <div key={i} style={{ padding: '20px 40px', fontSize: 'clamp(1.2rem, 3vw, 1.75rem)', fontWeight: 800, color: '#333', textTransform: 'uppercase', letterSpacing: '1px', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: '16px' }}>
                <div style={{ width: '24px', height: '24px', borderRadius: '12px', background: '#222' }}></div>
                {text}
              </div>
            ))}
          </Marquee>
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
              <Link to="/register" style={{ ...btnPrimary, padding: '18px 48px', fontSize: '1.1rem' }}>Book Your First Session</Link>
              <Link to="/services" style={{ ...btnSecondary, padding: '18px 48px', fontSize: '1.1rem' }}>View All Programs</Link>
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
                <Link to="/privacy" style={{ color: '#444', textDecoration: 'none', fontSize: '0.9rem' }}>Terms</Link>
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
