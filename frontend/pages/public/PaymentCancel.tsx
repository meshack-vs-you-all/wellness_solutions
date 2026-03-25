import React from 'react';
import { Link } from 'react-router-dom';
import { XCircle } from 'lucide-react';
import { Button } from '../../components/common/Button';

const PaymentCancel: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <XCircle className="h-16 w-16 text-neutral-400 mb-4" />
      <h1 className="text-3xl font-bold mb-2">Payment Cancelled</h1>
      <p className="text-neutral-600 dark:text-neutral-400 mb-8 max-w-md">
        Your payment process was cancelled. No charges were made.
      </p>
      <div className="flex flex-col sm:flex-row gap-4">
        <Link to="/pricing">
          <Button variant="default">Try Again</Button>
        </Link>
        <Link to="/">
          <Button variant="outline">Return Home</Button>
        </Link>
      </div>
    </div>
  );
};

export default PaymentCancel;
