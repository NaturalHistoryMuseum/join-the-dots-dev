import { getApi } from '@/services/api';
import { ref } from 'vue';
import router from '../router/router';
import { getCookie } from './cookies';

export const currentUser = ref(null);
let userLoaded = false;

export async function login() {
  try {
    const api = getApi();
    // Get the auth URL from the server
    const response = await api.get(`auth/login`, {
      withCredentials: true,
    });
    if (response.data.auth_url) {
      // Open login page in a new tab
      const authWindow = window.open(response.data.auth_url, '_blank');
      // Poll to check when login completes - every second
      const pollInterval = setInterval(async () => {
        try {
          const userResponse = await api.get('auth/status', {
            withCredentials: true,
          });
          // Check if user was returned
          if (userResponse.data.user) {
            // Stop polling
            clearInterval(pollInterval);
            // Close the pop-up
            authWindow.close();
            // Store user globally
            currentUser.value = userResponse.data.user;
            this.$router.push({
              path: '/',
            });
            return;
          }
        } catch (err) {
          console.error('Polling error:', err);
        }
      }, 1000);
    }
  } catch (error) {
    console.error('Login failed:', error);
  }
}

export async function logout() {
  try {
    const api = getApi();
    // Navigate to login page
    router.push('/login');
    currentUser.value = null;
    await api.get(`auth/logout`, { withCredentials: true });
  } catch (error) {
    console.error('Logout failed:', error);
  }
}

export function loadUser(reloadUser = false) {
  return new Promise((resolve) => {
    // Check if user is already loaded and it is not a manual reload
    if (userLoaded && !reloadUser) {
      resolve(currentUser.value);
      return;
    }
    // Check if the CSRF Token is stored in the cookies
    const csrfToken = getCookie('csrf_access_token');
    if (csrfToken) {
      const api = getApi();
      // Get the current logged in user if user is logged in
      api
        .get(`auth/status`, {
          withCredentials: true,
        })
        .then((response) => {
          currentUser.value = response.data.user;
          userLoaded = true;
          resolve(currentUser.value);
        })
        .catch(() => {
          logout();
          resolve(null);
        });
    } else {
      logout();
      resolve(null);
    }
  });
}
