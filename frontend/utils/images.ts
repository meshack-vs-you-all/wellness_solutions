import { getPublicAssetUrl, joinUrl, runtimeConfig } from '../config/runtime';

// Static image paths from the configured asset host
export const BACKEND_IMAGES = {
  // Logos
  LOGO: getPublicAssetUrl('logo.png'),
  LOGO_WHITE: getPublicAssetUrl('logo-white.png'),
  JPF_LOGO: getPublicAssetUrl('tr_jpf_logo.png'),
  
  // Service Images
  STRETCH_THERAPY: getPublicAssetUrl('stretch-therapy.jpg'),
  PERSONAL_TRAINING: getPublicAssetUrl('personal-training.jpg'),
  TEAM_BUILDING: getPublicAssetUrl('team-building.jpg'),
  WELLNESS: getPublicAssetUrl('wellness.jpg'),
  NUTRITION: getPublicAssetUrl('nutrition.jpg'),
  ERGONOMICS: getPublicAssetUrl('ergonomics.jpg'),
  BIOMETRIC_TESTS: getPublicAssetUrl('biometric-tests.jpg'),
  SERVICE_PLACEHOLDER: getPublicAssetUrl('service-placeholder.jpg'),
  
  // Hero/About Images
  ABOUT_HERO: getPublicAssetUrl('about-hero.jpg'),
  IMG_9748: getPublicAssetUrl('IMG_9748.jpg'),
  HERO_IMAGE: getPublicAssetUrl('0D0A0003.JPG'),
  
  // Team Images
  TEAM_1: getPublicAssetUrl('team/team-1.jpg'),
  TEAM_2: getPublicAssetUrl('team/team-2.jpg'),
  TEAM_3: getPublicAssetUrl('team/team-3.jpg'),
  
  // Testimonial Images
  TESTIMONIAL_1: getPublicAssetUrl('testimonial1.jpg'),
  TESTIMONIAL_2: getPublicAssetUrl('testimonial2.jpg'),
  TESTIMONIAL_3: getPublicAssetUrl('testimonial3.jpg'),
  
  // Icons
  DEFAULT_AVATAR: getPublicAssetUrl('default-avatar.svg'),
  FINANCE_ICON: getPublicAssetUrl('finance-icon.svg'),
  HEALTHCARE_ICON: getPublicAssetUrl('healthcare-icon.svg'),
  INTERNATIONAL_ICON: getPublicAssetUrl('international-icon.svg'),
  
  // Client Logos
  CLIENTS: {
    LOGO_1: getPublicAssetUrl('clients/logo1.png'),
    LOGO_2: getPublicAssetUrl('clients/logo2.png'),
    LOGO_3: getPublicAssetUrl('clients/logo3.png'),
    LOGO_4: getPublicAssetUrl('clients/logo4.png'),
    LOGO_5: getPublicAssetUrl('clients/logo5.png'),
    LOGO_6: getPublicAssetUrl('clients/logo6.png'),
    LOGO_7: getPublicAssetUrl('clients/logo7.png'),
    LOGO_8: getPublicAssetUrl('clients/logo8.png'),
    AON: getPublicAssetUrl('clients/aon.png'),
    SWEDISH: getPublicAssetUrl('clients/swedish.png'),
    KARURA: getPublicAssetUrl('clients/karura.png'),
    WORLDBANK: getPublicAssetUrl('clients/worldbank.svg'),
    GERTRUDES: getPublicAssetUrl('clients/gertrudes.png'),
    TNS: getPublicAssetUrl('clients/tns.png'),
    HEALTHCARE_ICON: getPublicAssetUrl('clients/healthcare-icon.svg'),
    FINANCE_ICON: getPublicAssetUrl('clients/finance-icon.svg'),
    PLACEHOLDER_LOGO: getPublicAssetUrl('clients/placeholder-logo.png'),
  }
};

// Utility function to get an image URL from the configured asset host.
export const getBackendImageUrl = (imagePath: string): string => {
  if (imagePath.startsWith('http')) {
    return imagePath;
  }
  return getPublicAssetUrl(imagePath);
};

// Utility function for media files (user uploads).
export const getMediaUrl = (mediaPath: string): string => {
  if (!mediaPath) return BACKEND_IMAGES.DEFAULT_AVATAR;
  if (mediaPath.startsWith('http')) {
    return mediaPath;
  }
  if (!runtimeConfig.mediaBaseUrl) {
    return getPublicAssetUrl(mediaPath.replace(/^\/+/g, ''));
  }

  return joinUrl(runtimeConfig.mediaBaseUrl, mediaPath);
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
