import axios from 'axios';
import { logout } from './authService';
import { getCookie } from './cookies';

let api_client = null;

export function initApi() {
  if (!window.APP_CONFIG) {
    throw new Error('APP_CONFIG is not loaded yet');
  }

  if (!api_client) {
    api_client = axios.create({
      baseURL: window.APP_CONFIG.API_URL,
      timeout: 10000,
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      },
      xsrfCookieName: 'csrf_access_token',
      xsrfHeaderName: 'X-CSRF-TOKEN',
    });
    // Add a request interceptor to inject CSRF token into header
    api_client.interceptors.request.use((config) => {
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
    api_client.interceptors.response.use(
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
  }

  return api_client;
}

export function getApi() {
  if (!api_client) {
    throw new Error('API client not initialized. Call initApi() first.');
  }
  return api_client;
}
