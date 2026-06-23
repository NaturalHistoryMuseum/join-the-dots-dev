import { loadUser } from '../services/authService';
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
