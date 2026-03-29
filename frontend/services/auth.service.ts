import api from './api';
import type { User } from '../types/user.types';

interface LoginResponse {
  token: string;
}

// These endpoints are legacy placeholders until WordPress auth routes are defined.
const login = async (email: string, password: string): Promise<{ token: string; user: User }> => {
  const response = await api.post<{ token: string; user: User }>('/auth-token/', {
    email,
    password,
  });
  const { token, user } = response.data;
  localStorage.setItem('authToken', token);
  return { token, user };
};

const register = async (name: string, email: string, password: string): Promise<{ token: string; user: User }> => {
  const response = await api.post<{ token: string; user: User }>('/auth/register/', {
    name,
    email,
    password,
  });
  const { token, user } = response.data;
  localStorage.setItem('authToken', token);
  return { token, user };
};

const logout = async (): Promise<void> => {
  try {
    // Attempt server-side logout when supported.
    await api.post('/auth/logout/');
  } catch (error) {
    // Local logout should still succeed even if the API call fails.
    console.error('Logout API call failed, but logging out locally.', error);
  } finally {
    localStorage.removeItem('authToken');
  }
};

const getCurrentUser = async (): Promise<User> => {
  const response = await api.get<User>('/users/me/');
  return response.data;
};

export const authService = {
  login,
  register,
  logout,
  getCurrentUser,
};
