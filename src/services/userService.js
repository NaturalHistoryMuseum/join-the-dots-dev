import axios from 'axios'
import { currentUser, loadUser } from '../services/authService'

// const API_URL = 'http://localhost:5000/api/user'
const API_URL = 'https://jtd-api-test.nhm.ac.uk/api/user'

export async function getUser() {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    // Use stored user data if available
    const user = JSON.parse(storedUser)
    const user_details = await axios.get(`${API_URL}/user/${user.azure_id}`).then((response) => {
      return response.data
    })
    return user_details
  }
  return
}

export async function editRole(role) {
  if (currentUser) {
    try {
      console.log(currentUser.value.user_id)
      const response = await axios
        .put(
          `${API_URL}/edit-role`,
          {
            user_id: currentUser.value.user_id,
            role: role,
          },
          { headers: { 'Content-Type': 'application/json' } },
        )
        .then((response) => {
          return response.data
        })
      // Reload user to get new role
      await loadUser(true)
      return response
    } catch (error) {
      console.error('Error updating role:', error)
      throw error
    }
  }
}

export async function addSections(sections) {
  if (currentUser) {
    try {
      const response = await axios
        .post(
          `${API_URL}/add-sections`,
          {
            user_id: currentUser.value.user_id,
            sections: sections,
          },
          { headers: { 'Content-Type': 'application/json' } },
        )
        .then((response) => {
          return response.data
        })
      // Reload user to get new role
      await loadUser(true)
      return response
    } catch (error) {
      console.error('Error adding sections:', error)
      throw error
    }
  }
}

export async function getSections() {
  if (currentUser) {
    try {
      const response = await axios
        .get(`${API_URL}/get-sections/${currentUser.value.user_id}`)
        .then((response) => {
          return response.data
        })
      return response
    } catch (error) {
      console.error('Error getting sections:', error)
      throw error
    }
  }
}
