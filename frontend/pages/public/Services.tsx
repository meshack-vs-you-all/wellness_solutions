
import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '../../components/common/Card';
import { BACKEND_IMAGES } from '../../utils/images';
import { Zap, Heart, Shield, Briefcase, Ruler, Activity, CheckSquare, Dumbbell, Apple, AlertTriangle, HelpCircle } from 'lucide-react';
import api from '../../services/api';

interface ServiceItem {
  id: number | string;
  title: string;
  description: string;
  price: number;
  type: string;
}

const getIcon = (title: string) => {
  const t = title.toLowerCase();
  if (t.includes('wellness')) return <Zap className="h-10 w-10 text-primary" />;
  if (t.includes('postural')) return <Ruler className="h-10 w-10 text-primary" />;
  if (t.includes('foot') || t.includes('pressure')) return <Activity className="h-10 w-10 text-primary" />;
  if (t.includes('ergonomic')) return <CheckSquare className="h-10 w-10 text-primary" />;
  if (t.includes('exercise') || t.includes('training')) return <Dumbbell className="h-10 w-10 text-primary" />;
  if (t.includes('nutrition')) return <Apple className="h-10 w-10 text-primary" />;
  if (t.includes('workshop') || t.includes('injury')) return <AlertTriangle className="h-10 w-10 text-primary" />;
  if (t.includes('wellness')) return <Heart className="h-10 w-10 text-primary" />;
  return <HelpCircle className="h-10 w-10 text-primary" />;
};

const getImage = (title: string) => {
  const t = title.toLowerCase();
  if (t.includes('wellness')) return BACKEND_IMAGES.STRETCH_THERAPY;
  if (t.includes('training')) return BACKEND_IMAGES.PERSONAL_TRAINING;
  if (t.includes('ergonomic')) return BACKEND_IMAGES.ERGONOMICS;
  if (t.includes('workshop')) return BACKEND_IMAGES.TEAM_BUILDING;
  return BACKEND_IMAGES.WELLNESS;
};

const Services: React.FC = () => {
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/classes/')
      .then(res => {
        // De-duplicate by title
        const seen = new Set();
        const unique = (res.data as ServiceItem[]).filter(s => {
          if (seen.has(s.title)) return false;
          seen.add(s.title);
          return true;
        });
        setServices(unique);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="py-8 sm:py-12 px-2 sm:px-0">
      <div className="text-center mb-8 sm:mb-12">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-neutral-800 dark:text-white tracking-tight">Our Services</h1>
        <p className="mt-4 text-base sm:text-lg text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto px-4 sm:px-0">
          We provide a range of services designed to help you move better, feel better, and live better.
        </p>
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 md:gap-8">
          {services.map((service, index) => (
            <Card key={index} className="flex flex-col sm:flex-row overflow-hidden transition-shadow hover:shadow-xl">
              <img src={getImage(service.title)} alt={service.title} className="w-full sm:w-1/3 h-48 sm:h-auto object-cover" />
              <div className="flex flex-col justify-center">
                  <CardContent>
                      <div className="mb-3 sm:mb-4">{getIcon(service.title)}</div>
                      <h3 className="text-xl sm:text-2xl font-bold mb-2 sm:mb-3">{service.title}</h3>
                      <p className="text-sm sm:text-base text-neutral-600 dark:text-neutral-300">{service.description}</p>
                  </CardContent>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Services;

export default Services;
