import axios from 'axios'

export async function getUser() {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    // Use stored user data if available
    const user = JSON.parse(storedUser)
    const user_details = await axios
      .get(`http://localhost:5000/api/user/user/${user.azure_id}`)
      .then((response) => {
        return response.data
      })
    return user_details
  }
  return
}
