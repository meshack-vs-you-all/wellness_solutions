import React from 'react';
import { Card, CardContent } from '../../components/common/Card';
import { BACKEND_IMAGES } from '../../utils/images';

const About: React.FC = () => {
  return (
    <div className="py-12 px-4">
      <div className="text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-extrabold text-neutral-800 dark:text-white tracking-tight">About Wellness Solutions</h1>
        <p className="mt-4 text-lg text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto">
          Founded in 2013 as <strong>Wellness Solutions Kenya Ltd</strong>, we are your partner in flexibility, recovery, and holistic wellness.
        </p>
      </div>

      <div className="max-w-5xl mx-auto space-y-12">
        {/* Our Philosophy Section */}
        <Card className="overflow-hidden">
          <div className="md:flex">
            <div className="md:flex-shrink-0">
              <img className="h-48 w-full object-cover md:w-48" src={BACKEND_IMAGES.ABOUT_HERO} alt="Studio ambiance" />
            </div>
            <div className="p-8">
              <h2 className="text-2xl font-bold text-primary dark:text-primary-light mb-3">Our Philosophy</h2>
              <p className="text-neutral-600 dark:text-neutral-300">
                At Wellness Solutions, we address the root causes of physical and nutritional imbalances through personalized interventions and comprehensive wellness programs. We believe that true fitness extends beyond strength and endurance—it's about mobility, balance, and a harmonious connection between physical and nutritional health. Our goal is to empower individuals and organizations to achieve healthier, more fulfilling lives.
              </p>
            </div>
          </div>
        </Card>

        {/* Core Services Section */}
        <div className="py-12 border-t border-neutral-200 dark:border-neutral-800">
          <h2 className="text-3xl font-bold text-center mb-12">Core Services</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { title: "Postural Analysis", desc: "Detailed assessment of body alignment to identify imbalances." },
              { title: "Foot Pressure Analysis", desc: "Scientific analysis of weight distribution and gait." },
              { title: "Ergonomics Assessments", desc: "Optimizing workspaces for health and productivity." },
              { title: "Corrective Exercise Therapy", desc: "Targeted movements to restore functional mobility." },
              { title: "Nutritional Guidance", desc: "Science-based approaches to fuel vitality and health." },
              { title: "Injury Prevention Workshops", desc: "Educational sessions to reduce physical risks at work and home." }
            ].map((service, i) => (
              <Card key={i} className="p-6">
                <h3 className="text-lg font-bold text-primary mb-2">{service.title}</h3>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">{service.desc}</p>
              </Card>
            ))}
          </div>
        </div>

        {/* Our Team Section */}
        <div>
          <h2 className="text-3xl font-bold text-center mb-8">Meet Our Team</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="text-center">
              <img className="w-32 h-32 rounded-full mx-auto mt-6 object-cover" src={BACKEND_IMAGES.TEAM_1} alt="Team member" />
              <CardContent>
                <h3 className="text-xl font-semibold">Jessica Pace</h3>
                <p className="text-primary dark:text-primary-light">Lead Wellness Practitioner</p>
                <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-2">Certified in Fascial Stretch Therapy and a 500-hour registered yoga teacher.</p>
              </CardContent>
            </Card>
            <Card className="text-center">
              <img className="w-32 h-32 rounded-full mx-auto mt-6 object-cover" src={BACKEND_IMAGES.TEAM_2} alt="Team member" />
              <CardContent>
                <h3 className="text-xl font-semibold">David Chen</h3>
                <p className="text-primary dark:text-primary-light">Pilates & Recovery Specialist</p>
                <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-2">Specializes in post-rehabilitation conditioning and athletic performance.</p>
              </CardContent>
            </Card>
            <Card className="text-center">
              <img className="w-32 h-32 rounded-full mx-auto mt-6 object-cover" src={BACKEND_IMAGES.TEAM_3} alt="Team member" />
              <CardContent>
                <h3 className="text-xl font-semibold">Maria Rodriguez</h3>
                <p className="text-primary dark:text-primary-light">Yoga Instructor</p>
                <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-2">Passionate about guiding students through mindful movement and breathwork.</p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Our Mission Section */}
        <div className="py-12">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-neutral-900 dark:text-white sm:text-4xl">Our Mission</h2>
            <p className="mt-4 text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              To revolutionize workplace wellness by delivering innovative, impactful, and customized health solutions that empower individuals and organizations to thrive.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center p-6 bg-primary/10 border border-primary/20 dark:bg-primary/5 dark:border-primary/10">
              <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-lg bg-primary/20 text-primary mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 dark:text-white">Proven Cost Reduction</h3>
              <p className="mt-2 text-neutral-600 dark:text-neutral-400">Expertise in reducing healthcare costs for organizations through preventive wellness programs and ergonomic solutions.</p>
            </Card>
            <Card className="text-center p-6 bg-primary/10 border border-primary/20 dark:bg-primary/5 dark:border-primary/10">
              <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-lg bg-primary/20 text-primary mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 dark:text-white">Enhanced Productivity</h3>
              <p className="mt-2 text-neutral-600 dark:text-neutral-400">Tailored solutions that boost productivity and employee morale through improved workplace wellness.</p>
            </Card>
            <Card className="text-center p-6 bg-primary/10 border border-primary/20 dark:bg-primary/5 dark:border-primary/10">
              <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-lg bg-primary/20 text-primary mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 dark:text-white">Strong Partnerships</h3>
              <p className="mt-2 text-neutral-600 dark:text-neutral-400">Established partnerships with leading health and wellness organizations to provide comprehensive solutions.</p>
            </Card>
          </div>
        </div>

        {/* Our Values Section */}
        <div className="py-12 border-t border-neutral-200 dark:border-neutral-800">
          <h2 className="text-3xl font-bold text-center text-neutral-900 dark:text-white mb-12">Our Values</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center p-6">
              <div className="mx-auto w-12 h-12 bg-primary rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 dark:text-white">Innovation</h3>
              <p className="mt-2 text-neutral-600 dark:text-neutral-400">Continuously seeking new and better ways to improve workplace wellness through cutting-edge solutions.</p>
            </Card>
            <Card className="text-center p-6">
              <div className="mx-auto w-12 h-12 bg-primary rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 dark:text-white">Excellence</h3>
              <p className="mt-2 text-neutral-600 dark:text-neutral-400">Delivering the highest quality services and products that exceed our clients' expectations.</p>
            </Card>
            <Card className="text-center p-6">
              <div className="mx-auto w-12 h-12 bg-primary rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 dark:text-white">Integrity</h3>
              <p className="mt-2 text-neutral-600 dark:text-neutral-400">Maintaining the highest ethical standards in all our business relationships and practices.</p>
            </Card>
          </div>
        </div>

      </div>
    </div>
  );
};

export default About;