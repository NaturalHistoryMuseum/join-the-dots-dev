import { ref } from 'vue'
import axios from 'axios'

export const currentUser = ref(null)
let userLoaded = false

const API_URL = 'http://localhost:5000/api/auth'

// Auth where it navigates to the auth URL
// export async function login() {
//   try {
//     // Get the auth URL from the server
//     const response = await axios.get(`${API_URL}/login`)
//     if (response.data.auth_url) {
//       // Redirect the user to the auth URL
//       window.location.href = response.data.auth_url
//     }
//   } catch (error) {
//     console.error('Login failed:', error)
//   }
// }

export async function login() {
  try {
    // Get the auth URL from the server
    const response = await axios.get(`${API_URL}/login`)
    if (response.data.auth_url) {
      // Open login page in a new tab
      const authWindow = window.open(response.data.auth_url, '_blank')
      // Poll to check when login completes - every second
      const pollInterval = setInterval(async () => {
        try {
          const userResponse = await axios.get(`${API_URL}/auth/status`, { withCredentials: true })

          if (userResponse.data.token) {
            // Stop polling
            clearInterval(pollInterval)
            // Close the pop-up
            authWindow.close()
            // Store user globally
            currentUser.value = userResponse.data.user
            console.log('Login successful:', userResponse.data.user)
            // Store JWT token in localStorage
            localStorage.setItem('jwt', userResponse.data.token)

            console.log('Login successful:', userResponse.data)
            // Contains the JWT token and user info
            return userResponse.data.user
          }
        } catch (err) {
          console.error('Polling error:', err)
        }
      }, 1000)
    }
  } catch (error) {
    console.error('Login failed:', error)
  }
}

// Not used atm
// export async function handleAuthRedirect(code) {
//   try {
//     const response = await axios.get(`${API_URL}/auth/redirect?code=${code}`, {
//       withCredentials: true,
//     })
//     return response.data
//   } catch (error) {
//     console.error('Auth redirect failed:', error)
//   }
// }

export async function logout() {
  try {
    localStorage.removeItem('jwt')
    currentUser.value = null
    await axios.get(`${API_URL}/logout`, { withCredentials: true })
    // window.location.href = '/'
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

// export function loadUser() {
//   const storedToken = localStorage.getItem('jwt')
//   if (storedToken) {
//     axios
//       .get(`${API_URL}/auth/status`, {
//         headers: { Authorization: `Bearer ${storedToken}` },
//         withCredentials: true,
//       })
//       .then((response) => {
//         currentUser.value = response.data.user
//       })
//       .catch(() => {
//         logout()
//       })
//   }
// }
export function loadUser() {
  return new Promise((resolve) => {
    if (userLoaded) {
      resolve(currentUser.value)
      return
    }

    const storedToken = localStorage.getItem('jwt')
    if (storedToken) {
      axios
        .get(`${API_URL}/auth/status`, {
          headers: { Authorization: `Bearer ${storedToken}` },
          withCredentials: true,
        })
        .then((response) => {
          currentUser.value = response.data.user
          userLoaded = true
          resolve(currentUser.value)
        })
        .catch(() => {
          logout()
          resolve(null)
        })
    } else {
      logout()
      resolve(null)
    }
  })
}
