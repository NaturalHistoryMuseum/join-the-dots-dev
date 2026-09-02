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

export async function getUserFromDir(user_email) {
  try {
    const response = await api.post(
      'user/check-user-by-email',
      { email: user_email },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      },
    );
    const existing_user = response.data.data;
    if (existing_user.length > 0) {
      return {
        new_user: false,
        user: existing_user[0],
        success: response.data.success,
      };
    } else {
      const new_user = await api.post(
        `user/azure/user`,
        { email: user_email },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        },
      );
      return {
        new_user: true,
        user: new_user.data.user,
        success: new_user.data.success,
      };
    }
  } catch (error) {
    console.error('Error submitting data:', error);
    throw error;
  }
}
