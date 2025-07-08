import axios from 'axios';
import { currentUser, loadUser } from '../services/authService';

// FOR LOCAL TESTING
const API_URL = 'http://localhost:5000/api/user';
// FOR K8S
// const API_URL = 'https://jtd-qa.nhm.ac.uk/api/user';

export async function getGenericUser(route) {
  try {
    const resp = await axios
      .get(`${API_URL}/${route}`, { withCredentials: true })
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
    const resp = await axios
      .post(`${API_URL}/${route}`, data, { withCredentials: true })
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
    const user_details = await axios
      .get(`${API_URL}/user/${user.azure_id}`, { withCredentials: true })
      .then((response) => {
        return response.data;
      });
    return user_details;
  }
  return;
}

export async function editRole(role) {
  if (currentUser) {
    try {
      const response = await axios
        .put(
          `${API_URL}/edit-user-role`,
          {
            user_id: currentUser.value.user_id,
            role_id: role,
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
      console.error('Error updating role:', error);
      throw error;
    }
  }
}

export async function assignUnits(units) {
  if (currentUser) {
    try {
      const response = await axios
        .post(
          `${API_URL}/assign-units`,
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

// export async function addSections(sections) {
//   if (currentUser) {
//     try {
//       const response = await axios
//         .post(
//           `${API_URL}/add-sections`,
//           {
//             user_id: currentUser.value.user_id,
//             sections: sections,
//           },
//           { headers: { 'Content-Type': 'application/json' } },
//         )
//         .then((response) => {
//           return response.data
//         })
//       // Reload user to get new role
//       await loadUser(true)
//       return response
//     } catch (error) {
//       console.error('Error adding sections:', error)
//       throw error
//     }
//   }
// }

// export async function getSections() {
//   if (currentUser) {
//     try {
//       const response = await axios
//         .get(`${API_URL}/get-sections/${currentUser.value.user_id}`)
//         .then((response) => {
//           return response.data
//         })
//       return response
//     } catch (error) {
//       console.error('Error getting sections:', error)
//       throw error
//     }
//   }
// }
