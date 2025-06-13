<template>
  <div class="main-page">
    <div class="main-header">
      <h1>Login</h1>
    </div>
    <div v-if="currentUser" class="content">
      <p>You are already logged in</p>
      <zoa-button label="Log Out" @click="logout" class="login-btn" />
    </div>
    <div v-else>
      <p>You are not currently logged in</p>
      <p></p>
      <zoa-button label="Login using SSO (Single Sign On)" @click="login" class="login-btn" />
    </div>
  </div>

  <p class="temp-warning">
    *Please note: This web app is still in development. No changes will affect actual JtD data.
  </p>
</template>

<script>
import { login, logout, currentUser } from '../services/authService'

export default {
  data() {
    return {}
  },
  setup() {
    return { currentUser }
  },
  async mounted() {},
  methods: {
    // Add functions from authService
    login,
    logout,
  },
}
</script>

<style scoped>
.temp-warning {
  margin: 2rem;
}
</style>
