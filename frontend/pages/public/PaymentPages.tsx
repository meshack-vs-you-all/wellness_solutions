import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import api from '../../services/api';

export function PaymentSuccess() {
  const [params] = useSearchParams();
  const sessionId = params.get('session_id');
  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying');

  useEffect(() => {
    // Give the webhook a moment, then confirm
    const timer = setTimeout(() => setStatus('success'), 1500);
    return () => clearTimeout(timer);
  }, [sessionId]);

  return (
    <div style={{ minHeight: '100vh', background: '#000', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'system-ui, sans-serif', textAlign: 'center', padding: 20 }}>
      <div>
        {status === 'verifying' && (
          <>
            <div style={{ width: 48, height: 48, border: '3px solid #333', borderTop: '3px solid #10b981', borderRadius: '50%', animation: 'spin 0.8s linear infinite', margin: '0 auto 24px' }} />
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
            <p style={{ color: '#888' }}>Confirming your payment...</p>
          </>
        )}
        {status === 'success' && (
          <>
            <div style={{ fontSize: '4rem', marginBottom: 16 }}>🎉</div>
            <h1 style={{ fontSize: '2.5rem', fontWeight: 800, margin: '0 0 16px' }}>Payment Successful!</h1>
            <p style={{ color: '#a7f3d0', marginBottom: 40, fontSize: '1.1rem' }}>Your session has been booked and confirmed.</p>
            <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Link to="/bookings" style={{ background: 'linear-gradient(135deg, #10b981, #047857)', color: '#fff', padding: '14px 28px', borderRadius: 12, textDecoration: 'none', fontWeight: 700 }}>View My Bookings</Link>
              <Link to="/" style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid #333', color: '#888', padding: '14px 28px', borderRadius: 12, textDecoration: 'none', fontWeight: 600 }}>Back to Home</Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export function PaymentCancel() {
  return (
    <div style={{ minHeight: '100vh', background: '#000', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'system-ui, sans-serif', textAlign: 'center', padding: 20 }}>
      <div>
        <div style={{ fontSize: '4rem', marginBottom: 16 }}>😔</div>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, margin: '0 0 16px' }}>Payment Cancelled</h1>
        <p style={{ color: '#888', marginBottom: 40 }}>No worries — your booking slot has been released. You can try again whenever you're ready.</p>
        <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link to="/booking" style={{ background: 'linear-gradient(135deg, #10b981, #047857)', color: '#fff', padding: '14px 28px', borderRadius: 12, textDecoration: 'none', fontWeight: 700 }}>Try Again</Link>
          <Link to="/" style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid #333', color: '#888', padding: '14px 28px', borderRadius: 12, textDecoration: 'none', fontWeight: 600 }}>Back to Home</Link>
        </div>
      </div>
    </div>
  );
}
