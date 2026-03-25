import api from './api';
import type { Class } from '../types/class.types';

// NOTE: Endpoint '/api/classes/' is an assumption. Adjust if your backend uses a different one.
const getClasses = async (): Promise<Class[]> => {
  const response = await api.get<Class[]>('/api/classes/');
  return response.data;
};

export const classService = {
  getClasses,
};
