import axios from 'axios'

const API_URL = 'http://localhost:5000/api/auth'

export async function login() {
  try {
    const response = await axios.get(`${API_URL}/login`)
    console.log('Response from login request:', response.data)
    if (response.data.auth_url) {
      window.location.href = response.data.auth_url
    }
  } catch (error) {
    console.error('Login failed:', error)
  }
}

export async function handleAuthRedirect(code) {
  try {
    const response = await axios.get(`${API_URL}/auth/redirect?code=${code}`, {
      withCredentials: true,
    })
    return response.data
  } catch (error) {
    console.error('Auth redirect failed:', error)
  }
}

export async function logout() {
  try {
    await axios.get(`${API_URL}/logout`, { withCredentials: true })
    window.location.href = '/'
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
