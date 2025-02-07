<template>
  <div class="main-page">
    <div class="main-header">
      <h1>Account</h1>
    </div>
    <div v-if="currentUser">
      <p>
        {{ currentUser }}
      </p>
    </div>
    <div v-else>
      <p>you aren't logged in mate</p>
    </div>
    <button @click="addUser">Add TEST User</button>
  </div>
</template>

<script>
import axios from 'axios'
import { currentUser } from '../services/authService'

export default {
  name: 'ViewUnit',
  setup() {
    return { currentUser }
  },
  data() {
    return {
      users: [],
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    fetchUsers() {
      axios.get(`http://localhost:5000/api/user/all-users`).then((response) => {
        this.users = response.data
        console.log(this.users)
      })
    },
    async addUser() {
      try {
        let testUser = {
          azure_id: '123',
          name: 'Test User',
          email: 'test',
        }
        const response = await axios.post('http://localhost:5000/api/user/add-user', testUser, {
          headers: { 'Content-Type': 'application/json' },
        })

        console.log(response.data)
      } catch (error) {
        console.log(error.response?.data?.error || 'Failed to add user')
      }
    },
  },
}
</script>

<style></style>
