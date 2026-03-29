import axios from 'axios';
import { runtimeConfig } from '../config/runtime';

const API_BASE_URL = runtimeConfig.apiBaseUrl;
const API_TIMEOUT = runtimeConfig.apiTimeout;

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Send any stored auth token when available.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    const wpRestNonce = runtimeConfig.wpRestNonce;

    if (token) {
      config.headers.Authorization = `${runtimeConfig.authScheme} ${token}`;
    }

    if (wpRestNonce) {
      config.headers['X-WP-Nonce'] = wpRestNonce;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
