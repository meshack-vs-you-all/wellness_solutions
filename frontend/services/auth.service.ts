import api from './api';
import type { User } from '../types/user.types';

interface LoginResponse {
  token: string;
}

// Note: The Django backend expects 'email' and 'password'.
const login = async (email: string, password: string): Promise<{ token: string; user: User }> => {
  const response = await api.post<{ token: string; user: User }>('/auth-token/', {
    email,
    password,
  });
  const { token, user } = response.data;
  localStorage.setItem('authToken', token);
  return { token, user };
};

// Register using the custom backend endpoint
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
    // Call the backend endpoint to invalidate the token
    await api.post('/auth/logout/');
  } catch (error) {
    // Even if the backend call fails, proceed with local logout
    console.error('Logout API call failed, but logging out locally.', error);
  } finally {
    // Always remove the token from local storage
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