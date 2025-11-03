import { currentUser, loadUser } from '../services/authService';
import api from './api';

export async function getGenericUser(route) {
  try {
    const resp = await api
      .get(`user/${route}`, { withCredentials: true })
      .then((response) => {
        return response.data;
      });
    return resp;
  } catch (error) {
    console.error('Error getting user data:', error);
    throw error;
  }
}

export async function postGenericUser(route, data, reloadUser = false) {
  try {
    const resp = await api
      .post(`user/${route}`, data, { withCredentials: true })
      .then((response) => {
        return response.data;
      });
    if (reloadUser) {
      await loadUser(true);
    }
    return resp;
  } catch (error) {
    console.error('Error posting user data:', error);
    throw error;
  }
}

export async function getUser() {
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    // Use stored user data if available
    const user = JSON.parse(storedUser);
    const user_details = await api
      .get(`/user/${user.azure_id}`, { withCredentials: true })
      .then((response) => {
        return response.data;
      });
    return user_details;
  }
  return;
}

export async function assignUnits(units) {
  if (currentUser) {
    try {
      const response = await api
        .post(
          `/assign-units`,
          {
            user_id: currentUser.value.user_id,
            units: units,
          },
          { headers: { 'Content-Type': 'application/json' } },
        )
        .then((response) => {
          return response.data;
        });
      // Reload user to get new role
      await loadUser(true);
      return response;
    } catch (error) {
      console.error('Error assigning units:', error);
      throw error;
    }
  }
}
