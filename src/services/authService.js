import axios from 'axios';
import { ref } from 'vue';

export const currentUser = ref(null);
let userLoaded = false;

// FOR LOCAL TESTING
const API_URL = 'http://localhost:5000/api/auth';
// FOR K8S
// const API_URL = 'https://jtd-qa.nhm.ac.uk/api/auth';

export async function login() {
  try {
    // Get the auth URL from the server
    const response = await axios.get(`${API_URL}/login`, {
      withCredentials: true,
    });
    if (response.data.auth_url) {
      // Open login page in a new tab
      const authWindow = window.open(response.data.auth_url, '_blank');
      // Poll to check when login completes - every second
      const pollInterval = setInterval(async () => {
        try {
          const userResponse = await axios.get(`${API_URL}/auth/status`, {
            withCredentials: true,
          });

          if (userResponse.data.token) {
            // Stop polling
            clearInterval(pollInterval);
            // Close the pop-up
            authWindow.close();
            // Store user globally
            currentUser.value = userResponse.data.user;
            // Store JWT token in localStorage
            localStorage.setItem('jwt', userResponse.data.token);

            // Contains the JWT token and user info
            return userResponse.data.user;
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
    localStorage.removeItem('jwt');
    currentUser.value = null;
    await axios.get(`${API_URL}/logout`, { withCredentials: true });
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

    const storedToken = localStorage.getItem('jwt');
    if (storedToken) {
      axios
        .get(`${API_URL}/auth/status`, {
          headers: { Authorization: `Bearer ${storedToken}` },
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
