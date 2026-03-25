import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const MetaIntegration: React.FC = () => {
  const location = useLocation();

  useEffect(() => {
    // Track PageView on route change
    if (window.fbq) {
      window.fbq('track', 'PageView');
    }

    // Dynamic Title and Meta tags based on route
    const updateMetaTags = () => {
      const path = location.pathname;
      let title = 'Wellness Solutions';
      let description = 'Elevate your wellness with professional stretching services.';

      if (path === '/') {
        title = 'Wellness Solutions - Home';
      } else if (path === '/services') {
        title = 'Our Services - Wellness Solutions';
        description = 'Explore our wide range of professional stretching and recovery services.';
      } else if (path === '/pricing') {
        title = 'Membership Pricing - Wellness Solutions';
        description = 'Choose the perfect membership plan for your fitness journey.';
      } else if (path === '/about') {
        title = 'About Us - Wellness Solutions';
      } else if (path === '/contact') {
        title = 'Contact Us - Wellness Solutions';
      }

      document.title = title;
      const metaDescription = document.querySelector('meta[name="description"]');
      if (metaDescription) {
        metaDescription.setAttribute('content', description);
      }

      // Update Open Graph tags
      const ogTitle = document.querySelector('meta[property="og:title"]');
      if (ogTitle) ogTitle.setAttribute('content', title);
      
      const ogDescription = document.querySelector('meta[property="og:description"]');
      if (ogDescription) ogDescription.setAttribute('content', description);
    };

    updateMetaTags();
  }, [location]);

  return null; // This component doesn't render anything
};

export default MetaIntegration;
