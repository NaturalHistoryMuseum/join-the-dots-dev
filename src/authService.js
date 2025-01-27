import axios from 'axios'

const API_BASE = 'http://localhost:5000/api/auth'

export const login = () => {
  window.location.href = `${API_BASE}/login/azure`
}

export const logout = async () => {
  await axios.get(`${API_BASE}/logout`)
  window.location.href = '/'
}

export const getUser = async () => {
  try {
    const response = await axios.get(`${API_BASE}/callback`)
    return response.data
  } catch (error) {
    console.error('Authentication failed', error)
    return null
  }
}
