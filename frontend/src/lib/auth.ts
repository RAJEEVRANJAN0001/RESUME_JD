/**
 * Authentication utilities for managing JWT tokens and user state.
 */

const TOKEN_KEY = 'auth_token';

export const setAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
};

export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
};

export const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
  }
};

export const clearToken = removeAuthToken; // Alias for consistency

export const isAuthenticated = (): boolean => {
  return !!getAuthToken();
};
