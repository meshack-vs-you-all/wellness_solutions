import React, { useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { CheckCircle } from 'lucide-react';
import { Button } from '../../components/common/Button';

const PaymentSuccess: React.FC = () => {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');

  useEffect(() => {
    // Track purchase with Meta Pixel
    if (window.fbq) {
        window.fbq('track', 'Purchase', {
            currency: 'USD',
            // value: 99.00 // This would ideally come from the server or state
        });
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <CheckCircle className="h-16 w-16 text-success mb-4" />
      <h1 className="text-3xl font-bold mb-2">Payment Successful!</h1>
      <p className="text-neutral-600 dark:text-neutral-400 mb-8 max-w-md">
        Thank you for your purchase. Your payment has been processed successfully.
        {sessionId && <span className="block mt-2 text-xs">Session ID: {sessionId}</span>}
      </p>
      <div className="flex flex-col sm:flex-row gap-4">
        <Link to="/dashboard">
          <Button variant="default">Go to Dashboard</Button>
        </Link>
        <Link to="/schedule">
          <Button variant="outline">Book a Session</Button>
        </Link>
      </div>
    </div>
  );
};

export default PaymentSuccess;
