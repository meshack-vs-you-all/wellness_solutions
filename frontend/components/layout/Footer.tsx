
import React from 'react';
import { Link } from 'react-router-dom';
import { Facebook, Instagram, Twitter, Mail, Phone, MapPin } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-neutral-800 dark:bg-neutral-900 text-white mt-auto">
      <div className="container mx-auto px-4 py-8 sm:py-10">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
          {/* About */}
          <div>
            <h3 className="text-lg font-semibold mb-3">About Wellness Solutions</h3>
            <p className="text-sm text-gray-300">
              Your premier destination for stretching, wellness, and recovery services.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/services" className="text-gray-300 hover:text-secondary transition-colors">Services</Link></li>
              <li><Link to="/schedule" className="text-gray-300 hover:text-secondary transition-colors">Schedule</Link></li>
              <li><Link to="/pricing" className="text-gray-300 hover:text-secondary transition-colors">Pricing</Link></li>
              <li><Link to="/about" className="text-gray-300 hover:text-secondary transition-colors">About Us</Link></li>
              <li><Link to="/privacy" className="text-gray-300 hover:text-secondary transition-colors">Privacy Policy</Link></li>
              <li><Link to="/terms" className="text-gray-300 hover:text-secondary transition-colors">Terms of Service</Link></li>
              <li><Link to="/cookie-policy" className="text-gray-300 hover:text-secondary transition-colors">Cookie Policy</Link></li>
              <li><Link to="/refund-policy" className="text-gray-300 hover:text-secondary transition-colors">Refund Policy</Link></li>
              <li><Link to="/accessibility" className="text-gray-300 hover:text-secondary transition-colors">Accessibility</Link></li>
              <li>
                <a
                  href="https://eskuribarefoot.africa"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-secondary transition-colors"
                >
                  Eskuri Shop ↗
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Contact</h3>
            <ul className="space-y-2 text-sm text-gray-300">
              <li className="flex items-center gap-2">
                <Phone size={14} />
                <span>0701810285</span>
              </li>
              <li className="flex items-center gap-2">
                <Mail size={14} />
                <span>info@jpfwellnesssolutions.com</span>
              </li>
              <li className="flex items-start gap-2">
                <MapPin size={14} className="mt-0.5" />
                <span>Wellness Solutions Kenya Ltd<br />Nairobi, Kenya</span>
              </li>
            </ul>
          </div>

          {/* Social Links */}
          <div>
            <h3 className="text-lg font-semibold mb-3">Follow Us</h3>
            <div className="flex space-x-3">
              <a href="#" className="text-gray-300 hover:text-secondary transition-colors" aria-label="Facebook">
                <Facebook size={20} />
              </a>
              <a href="#" className="text-gray-300 hover:text-secondary transition-colors" aria-label="Instagram">
                <Instagram size={20} />
              </a>
              <a href="#" className="text-gray-300 hover:text-secondary transition-colors" aria-label="Twitter">
                <Twitter size={20} />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-6 sm:mt-8 pt-6 text-center text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} Wellness Solutions. Empowering Kenyan Wellness since 2013.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;