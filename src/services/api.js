import axios from 'axios';
import { logout } from './authService';
import { getCookie } from './cookies';

// export const API_URL = import.meta.env.VITE_API_URL;
export const API_URL = 'https://jtd-qa.nhm.ac.uk/api/';

export const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
  xsrfCookieName: 'csrf_access_token',
  xsrfHeaderName: 'X-CSRF-TOKEN',
});

// Add a request interceptor to inject CSRF token into header
api.interceptors.request.use((config) => {
  // Only set the CSRF header if it’s not already set manually
  if (!config.headers['X-CSRF-TOKEN']) {
    const csrfToken = getCookie('csrf_access_token');
    if (csrfToken) {
      config.headers['X-CSRF-TOKEN'] = csrfToken;
    }
  }
  return config;
});

// //Adds interceptor for refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    //Log user out when token expires
    if (
      error.response?.status === 401 &&
      error.response.data.msg.includes('Token has expired')
    ) {
      console.error('Token expried, logging out');
      // Call a logout function
      logout();
    }
    return Promise.reject(error);
  },
);

export default api;
