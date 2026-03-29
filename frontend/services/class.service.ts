import api from './api';
import type { Class } from '../types/class.types';

const getClasses = async (): Promise<Class[]> => {
  const response = await api.get<Class[]>('/classes/');
  return response.data;
};

export const classService = {
  getClasses,
};
