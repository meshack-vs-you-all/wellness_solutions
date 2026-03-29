export type AppMode = 'standalone' | 'wordpress';
export type RouterMode = 'browser' | 'hash';
export type AuthScheme = 'Bearer' | 'Token';

export interface WellnessSolutionsRuntimeConfig {
  appMode: AppMode;
  routerMode: RouterMode;
  appBasePath: string;
  apiBaseUrl: string;
  apiTimeout: number;
  publicAssetBaseUrl: string;
  mediaBaseUrl: string;
  authScheme: AuthScheme;
  wpRestNonce?: string;
  siteUrl?: string;
  themeUrl?: string;
}

declare global {
  interface Window {
    WellnessSolutionsConfig?: Partial<WellnessSolutionsRuntimeConfig>;
    fbq?: (...args: unknown[]) => void;
  }
}

const windowConfig =
  typeof window !== 'undefined' ? window.WellnessSolutionsConfig ?? {} : {};

const envAppMode =
  (import.meta.env.VITE_APP_MODE as AppMode | undefined) ?? 'standalone';
const appMode = (windowConfig.appMode ?? envAppMode) as AppMode;

const normalizeBasePath = (value?: string): string => {
  if (!value || value === '/') {
    return '/';
  }

  return `/${value.replace(/^\/+|\/+$/g, '')}`;
};

const normalizeUrlBase = (value?: string): string => {
  if (!value) {
    return '';
  }

  if (value === '.') {
    return '.';
  }

  return value.replace(/\/+$/g, '');
};

const defaultApiBaseUrl =
  appMode === 'wordpress'
    ? '/wp-json/wellness-solutions/v1'
    : 'http://localhost:8000/api';

export const runtimeConfig: WellnessSolutionsRuntimeConfig = {
  appMode,
  routerMode: (windowConfig.routerMode ??
    import.meta.env.VITE_ROUTER_MODE ??
    (appMode === 'wordpress' ? 'hash' : 'browser')) as RouterMode,
  appBasePath: normalizeBasePath(
    windowConfig.appBasePath ?? import.meta.env.VITE_APP_BASE_PATH ?? '/',
  ),
  apiBaseUrl: normalizeUrlBase(
    windowConfig.apiBaseUrl ?? import.meta.env.VITE_API_URL ?? defaultApiBaseUrl,
  ),
  apiTimeout: Number(
    windowConfig.apiTimeout ?? import.meta.env.VITE_API_TIMEOUT ?? 30000,
  ),
  publicAssetBaseUrl: normalizeUrlBase(
    windowConfig.publicAssetBaseUrl ??
      import.meta.env.VITE_PUBLIC_ASSET_BASE_URL ??
      (import.meta.env.BASE_URL === './' ? '.' : import.meta.env.BASE_URL ?? ''),
  ),
  mediaBaseUrl: normalizeUrlBase(
    windowConfig.mediaBaseUrl ?? import.meta.env.VITE_MEDIA_BASE_URL ?? '',
  ),
  authScheme: (windowConfig.authScheme ??
    import.meta.env.VITE_AUTH_SCHEME ??
    (appMode === 'wordpress' ? 'Bearer' : 'Token')) as AuthScheme,
  wpRestNonce: windowConfig.wpRestNonce,
  siteUrl: windowConfig.siteUrl,
  themeUrl: windowConfig.themeUrl,
};

export const joinUrl = (base: string, path: string): string => {
  const cleanPath = path.replace(/^\/+/g, '');

  if (!base) {
    return `/${cleanPath}`;
  }

  if (base === '.') {
    return `./${cleanPath}`;
  }

  return `${base}/${cleanPath}`;
};

export const getPublicAssetUrl = (assetPath: string): string =>
  joinUrl(runtimeConfig.publicAssetBaseUrl, assetPath);

export const getApiEndpointUrl = (path: string): string =>
  joinUrl(runtimeConfig.apiBaseUrl, path);
