<template>
  <div class="main-page">
    <div class="main-header">
      <h1>Login</h1>
    </div>
    <div v-if="currentUser" class="content">
      <p>You are already logged in</p>
      <zoa-button label="Log Out" @click="logoutUser" class="login-btn" />
    </div>
    <div v-else>
      <p>You are not currently logged in</p>
      <p></p>
      <zoa-button label="Login using SSO (Single Sign On)" @click="login" class="login-btn" />
    </div>
  </div>
</template>

<script>
import { login, logout, currentUser } from '../services/authService'

export default {
  data() {
    return {
      user: null,
    }
  },
  setup() {
    return { currentUser }
  },
  async mounted() {},
  methods: {
    login,
    logoutUser() {
      this.user = null
      localStorage.removeItem('user')
      logout()
    },
  },
}
</script>

<style scoped></style>
