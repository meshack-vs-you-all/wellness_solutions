import { Link } from 'react-router-dom';
import { Reveal } from 'react-kino';
import { getPublicAssetUrl } from '../../config/runtime';

const PageHeader = ({ title }: { title: string }) => (
  <header style={{ padding: '20px 24px', borderBottom: '1px solid #1a1a1a', display: 'flex', justifyContent: 'space-between', alignItems: 'center', position: 'sticky', top: 0, background: 'rgba(18,18,18,0.8)', backdropFilter: 'blur(10px)', zIndex: 10 }}>
    <Link to="/" style={{ fontWeight: 800, fontSize: '1.1rem', color: '#fff', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 8 }}>
      <div style={{ width: 28, height: 28, background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', borderRadius: 7 }} />Wellness Solutions
    </Link>
    <Link to="/register" style={{ background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '10px 20px', borderRadius: 10, textDecoration: 'none', fontWeight: 700, fontSize: '0.9rem' }}>Get Started</Link>
  </header>
);

export function About() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <PageHeader title="About Us" />
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '80px 20px' }}>
        <Reveal animation="fade-up">
          <div style={{ color: 'var(--brand-primary)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 16 }}>Our Story</div>
          <h1 style={{ fontSize: 'clamp(2.5rem, 6vw, 4rem)', fontWeight: 800, letterSpacing: '-0.04em', margin: '0 0 40px', lineHeight: 1.1 }}>Movement is Medicine</h1>
        </Reveal>
        <Reveal animation="fade-up" delay={200}>
          <p style={{ fontSize: '1.2rem', lineHeight: 1.8, color: '#d4d4d8', marginBottom: 40 }}>
            Wellness Solutions was founded on a simple belief: that most people walk around in unnecessary pain because they've never been taught how to properly care for their bodies. Our founder, with over 15 years in professional sports medicine and movement therapy, set out to change that.
          </p>
          <p style={{ fontSize: '1.1rem', lineHeight: 1.8, color: '#888', marginBottom: 60 }}>
            We combine assisted stretching, functional fitness, and personalized wellness coaching into one studio experience. Whether you're a professional athlete, a weekend runner, or someone who sits at a desk all day — we have a program designed for you.
          </p>
        </Reveal>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 32, marginBottom: 80 }}>
          {[['500+', 'Happy Clients'], ['15+', 'Years Experience'], ['98%', 'Satisfaction Rate'], ['12', 'Expert Instructors']].map(([value, label]) => (
            <Reveal key={label} animation="fade-up">
              <div style={{ textAlign: 'center', padding: 28, background: 'var(--dark)', borderRadius: 20, border: '1px solid #222' }}>
                <div style={{ fontSize: '3rem', fontWeight: 800, color: 'var(--brand-primary)', letterSpacing: '-0.03em' }}>{value}</div>
                <div style={{ color: '#888', marginTop: 8 }}>{label}</div>
              </div>
            </Reveal>
          ))}
        </div>
        <Reveal animation="fade-up">
          <Link to="/register" style={{ display: 'inline-block', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '16px 40px', borderRadius: 12, textDecoration: 'none', fontWeight: 700, fontSize: '1rem' }}>
            Join Our Community →
          </Link>
        </Reveal>
      </div>
    </div>
  );
}

export function Blog() {
  const articles = [
    {
      title: "5 Assisted Stretches for Runner's Knee",
      excerpt: "If you are pounding the pavement, your IT band and quads are taking the brunt of it. Discover the top 5 stretches our clinical therapists use to alleviate runner's knee.",
      category: "Injury Recovery",
      date: "Oct 12, 2026",
      readTime: "4 min read",
      slug: "stretches-for-runners-knee",
      img: getPublicAssetUrl('personal-training.jpg')
    },
    {
      title: "Why Mobility Matters as You Age",
      excerpt: "Loss of flexibility isn't an inevitable part of aging, it's a symptom of disuse. Learn how making assisted stretching a weekly habit can keep you active into your 80s.",
      category: "Wellness",
      date: "Oct 05, 2026",
      readTime: "6 min read",
      slug: "flexibility-beats-aging",
      img: getPublicAssetUrl('wellness.jpg')
    },
    {
      title: "The Ultimate Post-Workout Recovery Routine",
      excerpt: "Don't just hit the showers. Spending 10 minutes cooling down with these specific deep stretches will flush lactic acid and accelerate your muscle recovery.",
      category: "Fitness",
      date: "Sep 28, 2026",
      readTime: "5 min read",
      slug: "morning-stretch-routine",
      img: getPublicAssetUrl('ergonomics.jpg')
    },
    {
      title: "Corporate Wellness: Reducing Desk Slouch",
      excerpt: "Sitting for 8 hours a day destroys your posture. We've compiled the ultimate guide for ergonomic stretching you can do without leaving the office.",
      category: "Corporate",
      date: "Sep 15, 2026",
      readTime: "7 min read",
      slug: "corporate-wellness-roi",
      img: getPublicAssetUrl('team-building.jpg')
    }
  ];

  return (
    <div style={{ backgroundColor: "var(--soft-dark)", color: "#fff", minHeight: "100vh", fontFamily: "system-ui, -apple-system, sans-serif" }}>
      <Progress type="bar" position="top" color="var(--brand-primary)" />

      {/* Header */}
      <header style={{ padding: "16px 24px", display: "flex", justifyContent: "center", borderBottom: "1px solid #1a1a1a", position: "sticky", top: 0, background: "rgba(18,18,18,0.8)", backdropFilter: "blur(10px)", zIndex: 10 }}>
        <Link to="/" style={{ textDecoration: "none" }}>
          <div style={{ fontWeight: 800, fontSize: "1.2rem", letterSpacing: "-0.02em", color: "#fff", display: "flex", alignItems: "center", gap: "12px" }}>
            <div style={{ width: "32px", height: "32px", background: "linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))", borderRadius: "8px" }}></div>
            Wellness Solutions
          </div>
        </Link>
      </header>

      {/* Blog Index */}
      <main style={{ padding: "60px 20px", display: "flex", flexDirection: "column", alignItems: "center" }}>

        <div style={{ maxWidth: "1200px", width: "100%" }}>
          <div style={{ textAlign: "center", marginBottom: "60px" }}>
            <Reveal animation="fade-up">
              <h1 style={{ fontSize: "clamp(2.5rem, 6vw, 4rem)", fontWeight: 800, letterSpacing: "-0.03em", margin: "0 0 16px" }}>The Recovery Room</h1>
              <p style={{ color: "#a1a1aa", fontSize: "1.2rem", maxWidth: "600px", margin: "0 auto" }}>Expert insights on mobility, injury prevention, and building a stronger, more resilient body.</p>
            </Reveal>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "32px" }}>
            {articles.map((article, i) => (
              <Reveal key={i} animation="fade-up" delay={i * 100}>
                <Link to={`/blog/${article.slug}`} style={{ textDecoration: "none" }}>
                  <div style={{
                    background: "var(--dark)",
                    borderRadius: "24px",
                    border: "1px solid #222",
                    overflow: "hidden",
                    display: "flex",
                    flexDirection: "column",
                    height: "100%",
                    cursor: "pointer",
                    transition: "transform 0.3s ease, border-color 0.3s ease"
                  }}
                    onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-5px)'; e.currentTarget.style.borderColor = '#444'; }}
                    onMouseOut={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = '#222'; }}
                  >
                    <div style={{ height: "240px", background: `url(${article.img}) center/cover` }}></div>
                    <div style={{ padding: "32px", display: "flex", flexDirection: "column", flex: 1 }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", fontSize: "0.9rem" }}>
                        <span style={{ color: "var(--brand-primary)", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1px" }}>{article.category}</span>
                        <span style={{ color: "#666" }}>{article.readTime}</span>
                      </div>
                      <h2 style={{ fontSize: "1.5rem", fontWeight: 700, margin: "0 0 16px", color: "#fff", lineHeight: 1.3 }}>{article.title}</h2>
                      <p style={{ color: "#a1a1aa", margin: "0 0 24px", lineHeight: 1.6, flex: 1 }}>{article.excerpt}</p>
                      <div style={{ color: "#666", fontSize: "0.9rem", borderTop: "1px solid #222", paddingTop: "16px" }}>
                        {article.date} · Written by JPF Therapists
                      </div>
                    </div>
                  </div>
                </Link>
              </Reveal>
            ))}
          </div>

        </div>
      </main>
    </div>
  );
}

import { useParams } from 'react-router-dom';

export function BlogPost() {
  const { slug } = useParams<{ slug: string }>();

  // Dummy data resolution based on slug
  const postInfo = {
    'stretches-for-runners-knee': { title: "5 Assisted Stretches for Runner's Knee", date: "March 8, 2026", tag: "Recovery" },
    'flexibility-beats-aging': { title: "Why Flexibility Training Beats Aging", date: "March 3, 2026", tag: "Wellness" },
    'corporate-wellness-roi': { title: "The Corporate Wellness ROI: A Real Study", date: "February 24, 2026", tag: "Corporate" },
    'morning-stretch-routine': { title: "Morning Stretch Routine in 10 Minutes", date: "February 18, 2026", tag: "Routine" },
  }[slug || ''] || { title: "Article Not Found", date: "", tag: "" };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <PageHeader title="Article" />
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '80px 20px' }}>
        <Reveal animation="fade-up">
          <Link to="/blog" style={{ color: 'var(--brand-primary)', textDecoration: 'none', fontWeight: 600, marginBottom: 24, display: 'inline-block' }}>← Back to Blog</Link>
          <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
            {postInfo.tag && <span style={{ background: 'rgba(15,173,182,0.1)', color: 'var(--brand-primary)', padding: '4px 12px', borderRadius: 99, fontSize: '0.8rem', fontWeight: 600 }}>{postInfo.tag}</span>}
            <span style={{ color: '#555', fontSize: '0.9rem', display: 'flex', alignItems: 'center' }}>{postInfo.date}</span>
          </div>
          <h1 style={{ fontSize: 'clamp(2.5rem, 5vw, 3.5rem)', fontWeight: 800, letterSpacing: '-0.04em', margin: '0 0 32px', lineHeight: 1.1 }}>
            {postInfo.title}
          </h1>
        </Reveal>

        {postInfo.title !== "Article Not Found" ? (
          <Reveal animation="fade-up" delay={200}>
            <div style={{ padding: '60px 0', borderTop: '1px solid #111' }}>
              <p style={{ fontSize: '1.2rem', lineHeight: 1.8, color: '#d4d4d8', marginBottom: 32 }}>
                Placeholder content for <strong>{postInfo.title}</strong>. In a fully connected application, this dynamic route (`/blog/:slug`) would fetch the markdown or rich text payload from the CMS/API layer.
              </p>
              <h3 style={{ fontSize: '1.5rem', fontWeight: 700, margin: '40px 0 16px' }}>The Science Behind It</h3>
              <p style={{ fontSize: '1.1rem', lineHeight: 1.8, color: '#888', marginBottom: 24 }}>
                Research shows that consistent assisted stretching significantly improves circulation and reduces myofascial tension. Our expert therapists employ techniques that not only relieve immediate pain but also construct a long-term framework for musculoskeletal health.
              </p>
              <h3 style={{ fontSize: '1.5rem', fontWeight: 700, margin: '40px 0 16px' }}>What You Can Do Today</h3>
              <p style={{ fontSize: '1.1rem', lineHeight: 1.8, color: '#888', marginBottom: 24 }}>
                Start by incorporating 5-10 minutes of active recovery into your morning. A few deep stretches targeting the hips, hamstrings, and thoracic spine will make a noticeable difference in your posture and energy levels throughout the day.
              </p>
              <div style={{ marginTop: 60, padding: 32, background: 'linear-gradient(145deg, var(--dark), var(--soft-dark))', borderRadius: 16, border: '1px solid #222' }}>
                <h4 style={{ margin: '0 0 12px', fontSize: '1.2rem' }}>Ready to experience it yourself?</h4>
                <p style={{ color: '#888', marginBottom: 24 }}>Book a 1-on-1 session with our lead therapists today.</p>
                <Link to="/register" style={{ display: 'inline-block', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '12px 24px', borderRadius: 8, textDecoration: 'none', fontWeight: 700 }}>Book a Session</Link>
              </div>
            </div>
          </Reveal>
        ) : (
          <p style={{ color: '#888', fontSize: '1.2rem' }}>Sorry, the article you are looking for does not exist.</p>
        )}
      </div>
    </div>
  );
}

export function Privacy() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <PageHeader title="Privacy Policy" />
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '80px 20px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>Privacy Policy</h1>
        <p style={{ color: '#888', marginBottom: 48 }}>Last updated: March 2026</p>
        {[
          { title: 'Information We Collect', text: 'We collect information you provide directly to us, such as your name, email address, payment information, and any health or fitness details you choose to share. We also collect usage data and device information.' },
          { title: 'How We Use Your Information', text: 'We use the information we collect to provide and improve our services, process transactions, communicate with you, and personalize your experience. We do not sell your personal data to third parties.' },
          { title: 'Data Security', text: 'We take reasonable measures to protect your personal information from unauthorized access, alteration, or disclosure. All payment information is encrypted using industry-standard SSL technology.' },
          { title: 'Cookies', text: 'We use cookies and similar technologies to improve your experience and analyze usage patterns. You can control cookie settings through your browser preferences.' },
          { title: 'Your Rights', text: 'You may request access to, correction of, or deletion of your personal information at any time by contacting us at privacy@jpfwellnesssolutions.com.' },
          { title: 'Contact Us', text: 'For questions about this Privacy Policy, please contact us at privacy@jpfwellnesssolutions.com or visit our studio in person.' },
        ].map(({ title, text }) => (
          <div key={title} style={{ marginBottom: 40 }}>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: 12, color: '#e4e4e7' }}>{title}</h2>
            <p style={{ color: '#888', lineHeight: 1.8 }}>{text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export function Contact() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <PageHeader title="Contact" />
      <div style={{ maxWidth: 700, margin: '0 auto', padding: '80px 20px', textAlign: 'center' }}>
        <Reveal animation="fade-up">
          <h1 style={{ fontSize: 'clamp(2.5rem, 6vw, 4rem)', fontWeight: 800, letterSpacing: '-0.04em', margin: '0 0 20px' }}>Get in Touch</h1>
          <p style={{ color: '#888', fontSize: '1.1rem', marginBottom: 60 }}>We'd love to hear from you. Reach out and a team member will respond within 24 hours.</p>
        </Reveal>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 24, marginBottom: 60 }}>
          {[['📧', 'Email', 'hello@jpfwellnesssolutions.com'], ['📞', 'Phone', '+1 (555) JPF-FLEX'], ['📍', 'Location', '123 Wellness Ave, Nairobi']].map(([icon, label, value]) => (
            <Reveal key={label} animation="fade-up">
              <div style={{ background: 'var(--dark)', border: '1px solid #222', borderRadius: 20, padding: 28 }}>
                <div style={{ fontSize: '2rem', marginBottom: 12 }}>{icon}</div>
                <div style={{ color: '#888', fontSize: '0.85rem', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 }}>{label}</div>
                <div style={{ fontWeight: 600 }}>{value}</div>
              </div>
            </Reveal>
          ))}
        </div>
        <Reveal animation="fade-up"><Link to="/register" style={{ display: 'inline-block', background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))', color: '#fff', padding: '16px 40px', borderRadius: 12, textDecoration: 'none', fontWeight: 700 }}>Book a Session Instead →</Link></Reveal>
      </div>
    </div>
  );
}

export function Terms() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <PageHeader title="Terms of Service" />
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '80px 20px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>Terms of Service</h1>
        <p style={{ color: '#888', marginBottom: 48 }}>Last updated: March 2026</p>

        {[
          { title: 'Use of Services', text: 'Wellness Solutions provides wellness, stretching, and fitness programs. You agree to follow staff instructions and to use services responsibly.' },
          { title: 'Health Disclaimer', text: 'Our services are not a substitute for medical advice. Consult a healthcare professional before starting any programme, especially if you have injuries or conditions.' },
          { title: 'Payments & Subscriptions', text: 'All payments are processed through third-party payment providers. Subscription access and entitlements may depend on successful payment confirmation.' },
          { title: 'Bookings & Cancellations', text: 'Bookings are subject to availability. Cancellation rules may apply and may vary by programme or event type.' },
          { title: 'Intellectual Property', text: 'Content delivered through programmes (including video libraries and materials) is for member use only.' },
          { title: 'Limitation of Liability', text: 'To the maximum extent permitted by law, Wellness Solutions is not liable for indirect or consequential damages.' },
          { title: 'Changes to Terms', text: 'We may update these Terms periodically. Continued use of services indicates acceptance of updated terms.' },
        ].map(({ title, text }) => (
          <div key={title} style={{ marginBottom: 40 }}>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: 12, color: '#e4e4e7' }}>{title}</h2>
            <p style={{ color: '#888', lineHeight: 1.8 }}>{text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export function RefundPolicy() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <PageHeader title="Refund Policy" />
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '80px 20px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>Refund Policy</h1>
        <p style={{ color: '#888', marginBottom: 48 }}>Last updated: March 2026</p>

        <div style={{ marginBottom: 40 }}>
          <p style={{ color: '#888', lineHeight: 1.8 }}>
            Refunds depend on the payment method, programme type, and timing of cancellations. Where applicable, we will follow the refund capabilities of our payment processor and programme delivery partners.
          </p>
        </div>

        {[
          { title: 'Memberships', text: 'Membership refunds are handled according to the membership product rules and payment provider confirmations.' },
          { title: 'One-Off Sessions', text: 'Individual booking refunds may be offered if cancelled within the applicable cancellation window.' },
          { title: 'Chargebacks', text: 'Chargebacks should be avoided where possible. If a dispute occurs, we will work with the payment provider to reconcile access and delivery.' },
          { title: 'Contact', text: 'For refund requests, contact our support team and include your booking or order reference.' },
        ].map(({ title, text }) => (
          <div key={title} style={{ marginBottom: 40 }}>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: 12, color: '#e4e4e7' }}>{title}</h2>
            <p style={{ color: '#888', lineHeight: 1.8 }}>{text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export function CookiePolicy() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <PageHeader title="Cookie Policy" />
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '80px 20px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>Cookie Policy</h1>
        <p style={{ color: '#888', marginBottom: 48 }}>Last updated: March 2026</p>

        {[
          { title: 'What Are Cookies?', text: 'Cookies are small text files stored on your device to help websites function and remember preferences.' },
          { title: 'How We Use Cookies', text: 'We may use cookies for essential site functionality, analytics, and marketing performance.' },
          { title: 'Third-Party Cookies', text: 'If you use embedded services (such as booking widgets and analytics), those providers may set their own cookies.' },
          { title: 'Your Choices', text: 'You can manage cookies through your browser settings. Disabling cookies may affect certain website features.' },
          { title: 'Contact', text: 'If you have questions about cookies, contact our support team.' },
        ].map(({ title, text }) => (
          <div key={title} style={{ marginBottom: 40 }}>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: 12, color: '#e4e4e7' }}>{title}</h2>
            <p style={{ color: '#888', lineHeight: 1.8 }}>{text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export function AccessibilityPolicy() {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--soft-dark)', color: '#fff', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <PageHeader title="Accessibility" />
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '80px 20px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 8px' }}>Accessibility Statement</h1>
        <p style={{ color: '#888', marginBottom: 48 }}>Last updated: March 2026</p>

        {[
          { title: 'Our Commitment', text: 'Wellness Solutions is committed to making our website accessible to everyone, including people with disabilities.' },
          { title: 'Ongoing Efforts', text: 'We continuously improve our accessibility practices, test with assistive technologies, and address issues as they are reported.' },
          { title: 'Reporting Accessibility Issues', text: 'If you experience an accessibility barrier, contact us and we will respond to your request.' },
        ].map(({ title, text }) => (
          <div key={title} style={{ marginBottom: 40 }}>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: 12, color: '#e4e4e7' }}>{title}</h2>
            <p style={{ color: '#888', lineHeight: 1.8 }}>{text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
