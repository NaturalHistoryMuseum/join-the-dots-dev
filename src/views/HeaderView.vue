<script setup>
import NavLinks from '../components/NavLinks.vue'
</script>

<template>
  <header class="header-bar">
    <div class="title-header">
      <button @click="navigateHome" class="icon-btn">
        <img alt="NHM logo" class="logo" src="@/assets/nhm_white_logo.png" />
      </button>
      <button @click="navigateHome" class="icon-btn"><h1 class="title">Join the Dots</h1></button>

      <div class="account-header">
        <div v-if="currentUser">
          <button @click="navigateAccount" class="icon-btn">
            <i alt="Account Button" class="bi bi-person-fill icon"></i>
          </button>
          <button @click="logoutUser" class="icon-btn">
            <i alt="Logout Button" class="bi bi-box-arrow-in-right icon"></i>
          </button>
        </div>
        <div v-else>
          <button @click="login" class="icon-btn">
            <i alt="Login Button" class="bi bi-box-arrow-in-left icon"></i>
          </button>
          <!-- <button @click="login">Login with Microsoft</button> -->
        </div>
      </div>
    </div>

    <div class="nav-header">
      <NavLinks />
    </div>
  </header>
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
    navigateAccount() {
      this.$router.push('/account')
    },
    navigateHome() {
      this.$router.push('/')
    },
  },
}
</script>

<style>
.header-bar {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  align-items: flex-end;
  padding: 1rem 2rem;
  padding-bottom: 1rem;
  background-color: var(--primary-col);
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.title-header {
  display: flex;
  width: 100%;
}

.nav-header {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  gap: 3rem;
  width: 100%;
}

.account-header {
  display: flex;
  align-items: flex-start;
  justify-self: flex-end;
  margin-left: auto;
  gap: 3rem;
}

.logo {
  height: 5rem;
  justify-self: flex-start;
}
.title {
  align-self: center;
  color: white;
  margin: 0;
  margin-left: 3rem;
  font-size: 2.5rem;
}

.icon-btn {
  background-color: transparent;
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  margin: 0;
}

.icon {
  font-size: 2rem;
  color: white;
  margin: 0 0.5rem;
}

@media (max-width: 768px) {
  .header-bar {
    padding: 0.5rem 1rem;
    padding-bottom: 1rem;
  }
  .nav-header {
    gap: 1rem;
  }
  .logo {
    height: 4rem;
  }
  .title {
    font-size: 1.8rem;
    margin-left: 2rem;
  }
  .icon {
    font-size: 1.4rem;
  }
}
@media (max-width: 480px) {
  .header-bar {
    padding: 0.5rem 1rem;
    padding-bottom: 0.7rem;
  }
  .logo {
    height: 3rem;
  }
  .title {
    font-size: 1.2rem;
    margin-left: 1.5rem;
  }
  .icon {
    font-size: 1.3rem;
  }
}
</style>
