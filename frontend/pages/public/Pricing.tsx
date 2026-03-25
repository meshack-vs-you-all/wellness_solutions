
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../../components/common/Button';
import { Card, CardContent, CardHeader } from '../../components/common/Card';
import { Check, Loader2 } from 'lucide-react';
import { paymentService } from '../../services/payment.service';
import { useAuth } from '../../contexts/AuthContext';

const pricingTiers = [
  {
    id: 1, // Assumed ID in database
    name: 'Basic',
    price: '$99',
    frequency: '/month',
    description: 'Perfect for getting started and building a consistent routine.',
    features: [
      '4 Classes per Month',
      'Access to Open Stretch Areas',
      'Online Booking',
    ],
    isMostPopular: false,
  },
  {
    id: 2, // Assumed ID in database
    name: 'Premium',
    price: '$149',
    frequency: '/month',
    description: 'Our most popular plan for those committed to their wellness journey.',
    features: [
      '8 Classes per Month',
      '1 Assisted Wellness Session',
      'Free Towel Service',
      'Advanced Booking Privileges',
    ],
    isMostPopular: true,
  },
  {
    id: 3, // Assumed ID in database
    name: 'Unlimited',
    price: '$199',
    frequency: '/month',
    description: 'For the dedicated athlete who wants it all.',
    features: [
      'Unlimited Classes',
      '4 Assisted Wellness Sessions',
      'Full Recovery Suite Access',
      'Bring a Friend Pass (1/mo)',
    ],
    isMostPopular: false,
  },
];

const Pricing: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loadingTier, setLoadingTier] = useState<number | null>(null);

  const handlePurchase = async (tier: typeof pricingTiers[0]) => {
    if (!user) {
        navigate('/login');
        return;
    }

    setLoadingTier(tier.id);
    try {
        // Track initiate checkout with Meta Pixel
        if (window.fbq) {
            window.fbq('track', 'InitiateCheckout', {
                content_name: tier.name,
                currency: 'USD',
                value: parseFloat(tier.price.replace('$', ''))
            });
        }

        const { checkout_url } = await paymentService.createCheckoutSession('package', tier.id);
        window.location.href = checkout_url;
    } catch (error) {
        console.error('Payment Error:', error);
        alert('Could not initiate payment. Please try again.');
        setLoadingTier(null);
    }
  };

  return (
    <div className="py-8 sm:py-12 px-2 sm:px-0">
      <div className="text-center mb-8 sm:mb-12">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-neutral-800 dark:text-white tracking-tight">Find Your Perfect Plan</h1>
        <p className="mt-4 text-base sm:text-lg text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto px-4 sm:px-0">
          Choose a membership that fits your lifestyle and goals. All plans are flexible and can be cancelled anytime.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8 items-start">
        {pricingTiers.map((tier) => (
          <Card key={tier.name} className={`flex flex-col h-full ${tier.isMostPopular ? 'border-2 border-primary shadow-2xl transform lg:scale-105' : ''}`}>
             {tier.isMostPopular && (
              <div className="bg-primary text-white text-center py-1 font-bold text-sm rounded-t-xl">
                Most Popular
              </div>
            )}
            <CardHeader className="text-center">
              <h3 className="text-xl sm:text-2xl font-bold">{tier.name}</h3>
              <p className="mt-2 text-sm sm:text-base text-neutral-500 dark:text-neutral-400">{tier.description}</p>
            </CardHeader>
            <CardContent className="flex-grow">
              <div className="text-center mb-4 sm:mb-6">
                <span className="text-3xl sm:text-4xl lg:text-5xl font-extrabold">{tier.price}</span>
                <span className="text-lg sm:text-xl text-neutral-500 dark:text-neutral-400">{tier.frequency}</span>
              </div>
              <ul className="space-y-3 sm:space-y-4">
                {tier.features.map((feature, index) => (
                  <li key={index} className="flex items-center">
                    <Check className="h-4 sm:h-5 w-4 sm:w-5 text-success mr-2 sm:mr-3 flex-shrink-0" />
                    <span className="text-sm sm:text-base">{feature}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
            <div className="p-6 mt-auto">
              <Button 
                className="w-full" 
                variant={tier.isMostPopular ? 'default' : 'outline'}
                onClick={() => handlePurchase(tier)}
                disabled={loadingTier === tier.id}
              >
                {loadingTier === tier.id ? (
                    <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Processing...
                    </>
                ) : (
                    'Get Started'
                )}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Pricing;
