// Use environment variable with fallback for backend base URL (without /api)
const API_BASE_URL = import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://localhost:8000';

// Static image paths from the Django backend
export const BACKEND_IMAGES = {
  // Logos
  LOGO: `${API_BASE_URL}/static/images/logo.png`,
  LOGO_WHITE: `${API_BASE_URL}/static/images/logo-white.png`,
  JPF_LOGO: `${API_BASE_URL}/static/images/tr_jpf_logo.png`,
  
  // Service Images
  STRETCH_THERAPY: `${API_BASE_URL}/static/images/wellness-therapy.jpg`,
  PERSONAL_TRAINING: `${API_BASE_URL}/static/images/personal-training.jpg`,
  TEAM_BUILDING: `${API_BASE_URL}/static/images/team-building.jpg`,
  WELLNESS: `${API_BASE_URL}/static/images/wellness.jpg`,
  NUTRITION: `${API_BASE_URL}/static/images/nutrition.jpg`,
  ERGONOMICS: `${API_BASE_URL}/static/images/ergonomics.jpg`,
  BIOMETRIC_TESTS: `${API_BASE_URL}/static/images/biometric-tests.jpg`,
  SERVICE_PLACEHOLDER: `${API_BASE_URL}/static/images/service-placeholder.jpg`,
  
  // Hero/About Images
  ABOUT_HERO: `${API_BASE_URL}/static/images/about-hero.jpg`,
  IMG_9748: `${API_BASE_URL}/static/images/IMG_9748.jpg`,
  HERO_IMAGE: `${API_BASE_URL}/static/images/0D0A0003.JPG`,
  
  // Team Images
  TEAM_1: `${API_BASE_URL}/static/images/team/team-1.jpg`,
  TEAM_2: `${API_BASE_URL}/static/images/team/team-2.jpg`,
  TEAM_3: `${API_BASE_URL}/static/images/team/team-3.jpg`,
  
  // Testimonial Images
  TESTIMONIAL_1: `${API_BASE_URL}/static/images/testimonial1.jpg`,
  TESTIMONIAL_2: `${API_BASE_URL}/static/images/testimonial2.jpg`,
  TESTIMONIAL_3: `${API_BASE_URL}/static/images/testimonial3.jpg`,
  
  // Icons
  DEFAULT_AVATAR: `${API_BASE_URL}/static/images/default-avatar.svg`,
  FINANCE_ICON: `${API_BASE_URL}/static/images/finance-icon.svg`,
  HEALTHCARE_ICON: `${API_BASE_URL}/static/images/healthcare-icon.svg`,
  INTERNATIONAL_ICON: `${API_BASE_URL}/static/images/international-icon.svg`,
  
  // Client Logos
  CLIENTS: {
    LOGO_1: `${API_BASE_URL}/static/images/clients/logo1.png`,
    LOGO_2: `${API_BASE_URL}/static/images/clients/logo2.png`,
    LOGO_3: `${API_BASE_URL}/static/images/clients/logo3.png`,
    LOGO_4: `${API_BASE_URL}/static/images/clients/logo4.png`,
    LOGO_5: `${API_BASE_URL}/static/images/clients/logo5.png`,
    LOGO_6: `${API_BASE_URL}/static/images/clients/logo6.png`,
    LOGO_7: `${API_BASE_URL}/static/images/clients/logo7.png`,
    LOGO_8: `${API_BASE_URL}/static/images/clients/logo8.png`,
    AON: `${API_BASE_URL}/static/images/clients/aon.png`,
    SWEDISH: `${API_BASE_URL}/static/images/clients/swedish.png`,
    KARURA: `${API_BASE_URL}/static/images/clients/karura.png`,
    WORLDBANK: `${API_BASE_URL}/static/images/clients/worldbank.svg`,
    GERTRUDES: `${API_BASE_URL}/static/images/clients/gertrudes.png`,
    TNS: `${API_BASE_URL}/static/images/clients/tns.png`,
    HEALTHCARE_ICON: `${API_BASE_URL}/static/images/clients/healthcare-icon.svg`,
    FINANCE_ICON: `${API_BASE_URL}/static/images/clients/finance-icon.svg`,
    PLACEHOLDER_LOGO: `${API_BASE_URL}/static/images/clients/placeholder-logo.png`,
  }
};

// Utility function to get backend image URL
export const getBackendImageUrl = (imagePath: string): string => {
  if (imagePath.startsWith('http')) {
    return imagePath;
  }
  return `${API_BASE_URL}/static/images/${imagePath}`;
};

// Utility function for media files (user uploads)
export const getMediaUrl = (mediaPath: string): string => {
  if (!mediaPath) return BACKEND_IMAGES.DEFAULT_AVATAR;
  if (mediaPath.startsWith('http')) {
    return mediaPath;
  }
  return `${API_BASE_URL}/media/${mediaPath}`;
};

// Service type to image mapping
export const SERVICE_IMAGES = {
  'wellness': BACKEND_IMAGES.STRETCH_THERAPY,
  'personal-training': BACKEND_IMAGES.PERSONAL_TRAINING,
  'team-building': BACKEND_IMAGES.TEAM_BUILDING,
  'wellness': BACKEND_IMAGES.WELLNESS,
  'nutrition': BACKEND_IMAGES.NUTRITION,
  'ergonomics': BACKEND_IMAGES.ERGONOMICS,
  'biometric': BACKEND_IMAGES.BIOMETRIC_TESTS,
  'default': BACKEND_IMAGES.SERVICE_PLACEHOLDER,
};

// Get service image by type
export const getServiceImage = (serviceType: string): string => {
  return SERVICE_IMAGES[serviceType as keyof typeof SERVICE_IMAGES] || SERVICE_IMAGES.default;
};
