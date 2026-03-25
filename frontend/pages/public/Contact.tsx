import React from 'react';
import { Button } from '../../components/common/Button';
import { Card, CardContent } from '../../components/common/Card';
import { Phone, Mail, MapPin } from 'lucide-react';

const Contact: React.FC = () => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert("Thank you for your message! We will get back to you shortly.");
  }
  return (
    <div className="py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-extrabold text-neutral-800 dark:text-white tracking-tight">Get In Touch</h1>
        <p className="mt-4 text-lg text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto">
          We're here to answer any questions you may have. Reach out to us and we'll respond as soon as we can.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
        {/* Contact Form */}
        <Card>
          <CardContent>
            <h2 className="text-2xl font-bold mb-6">Send us a Message</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Full Name</label>
                <input type="text" id="name" required className="mt-1 block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:border-neutral-600" />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Email Address</label>
                <input type="email" id="email" required className="mt-1 block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:border-neutral-600" />
              </div>
              <div>
                <label htmlFor="message" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Message</label>
                <textarea id="message" rows={4} required className="mt-1 block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:border-neutral-600"></textarea>
              </div>
              <div>
                <Button type="submit" className="w-full">Send Message</Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Contact Info */}
        <div className="space-y-8">
            <Card>
                <CardContent>
                    <h2 className="text-2xl font-bold mb-4">Contact Information</h2>
                    <div className="space-y-4 text-neutral-700 dark:text-neutral-300">
                        <div className="flex items-start">
                            <MapPin className="h-6 w-6 text-primary dark:text-primary-light mr-4 mt-1 flex-shrink-0" />
                            <span>123 Wellness Avenue, Suite 100, Healthville, ST 54321</span>
                        </div>
                        <div className="flex items-center">
                            <Phone className="h-6 w-6 text-primary dark:text-primary-light mr-4" />
                            <span>(123) 456-7890</span>
                        </div>
                        <div className="flex items-center">
                            <Mail className="h-6 w-6 text-primary dark:text-primary-light mr-4" />
                            <span>hello@jpfwellnesssolutions.com</span>
                        </div>
                    </div>
                </CardContent>
            </Card>
            <Card>
                <CardContent>
                     <h2 className="text-2xl font-bold mb-4">Hours of Operation</h2>
                     <ul className="space-y-2 text-neutral-700 dark:text-neutral-300">
                        <li><strong>Monday - Friday:</strong> 6:00 AM - 9:00 PM</li>
                        <li><strong>Saturday:</strong> 8:00 AM - 6:00 PM</li>
                        <li><strong>Sunday:</strong> 9:00 AM - 4:00 PM</li>
                     </ul>
                </CardContent>
            </Card>
        </div>
      </div>
    </div>
  );
};

export default Contact;