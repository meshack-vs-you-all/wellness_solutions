import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import type { User } from '../types/user.types';
import { authService } from '../services/auth.service';

// Define localStorage keys and TTL
const CACHED_USER_KEY = 'cachedUser';
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Helper to store user in cache
  const cacheUser = useCallback((userData: User) => {
    const cacheEntry = {
      user: userData,
      timestamp: Date.now(),
    };
    localStorage.setItem(CACHED_USER_KEY, JSON.stringify(cacheEntry));
  }, []);

  // Helper to clear user from cache
  const clearUserCache = useCallback(() => {
    localStorage.removeItem(CACHED_USER_KEY);
  }, []);

  const initAuth = useCallback(async () => {
    setLoading(true);

    // 1. Check for auth token and fetch from backend (Primary)
    const token = localStorage.getItem('authToken');
    if (token) {
      try {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
        cacheUser(currentUser); 
        setLoading(false);
        return;
      } catch (error) {
        console.error('Failed to fetch user with stored token', error);
        localStorage.removeItem('authToken');
        clearUserCache();
        setUser(null);
      }
    }

    // 2. Fallback to cache ONLY if no token was found or fetch failed
    const cachedUserString = localStorage.getItem(CACHED_USER_KEY);
    if (cachedUserString) {
      try {
        const cachedEntry = JSON.parse(cachedUserString);
        if (cachedEntry && cachedEntry.user && cachedEntry.timestamp) {
          const now = Date.now();
          if (now - cachedEntry.timestamp < CACHE_TTL_MS) {
            setUser(cachedEntry.user);
          } else {
            clearUserCache();
          }
        }
      } catch (error) {
        clearUserCache();
      }
    } else {
      setUser(null);
    }
    setLoading(false);
  }, [cacheUser, clearUserCache]);


  useEffect(() => {
    initAuth();
  }, [initAuth]);

  const login = async (email: string, password: string) => {
    const { user: loggedInUser } = await authService.login(email, password);
    setUser(loggedInUser);
    cacheUser(loggedInUser); // Cache user on successful login
  };

  const register = async (name: string, email: string, password: string) => {
    const { user: newUser } = await authService.register(name, email, password);
    setUser(newUser);
    cacheUser(newUser); // Cache user on successful registration
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
    clearUserCache(); // Clear cached user on logout
  };

  const value = { user, loading, login, logout, register };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};