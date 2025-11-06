<template>
  <div class="main-page">
    <div class="main-header">
      <p class="h1-style">Login</p>
    </div>
    <div v-if="currentUser" class="content">
      <p>You are already logged in</p>
      <zoa-button label="Log Out" @click="logout" class="login-btn" />
    </div>
    <div v-else>
      <p>You are not currently logged in</p>
      <p></p>
      <zoa-button
        label="Login using SSO (Single Sign On)"
        @click="login"
        class="login-btn"
      />
    </div>
  </div>

  <p v-if="APP_ENV == 'qa'" class="h5-style temp-warning env-warning">
    <SmallMessages
      message_type="warning"
      message_text="User Acceptance Testing is now concluded and this environment may not
    function as expected
    ."
    />
  </p>
  <p v-if="APP_ENV == 'prod'" class="h5-style temp-warning env-warning">
    <SmallMessages
      message_type="warning"
      message_text="This environment is not yet live. Please do not access."
    />
  </p>
  <p v-if="APP_ENV == 'dev'" class="h5-style temp-warning env-warning">
    <SmallMessages
      message_type="warning"
      message_text="This environment is dev."
    />
  </p>
</template>

<script>
import SmallMessages from '@/components/SmallMessages.vue';
import { APP_ENV } from '@/utils/utils';
import { currentUser, login, logout } from '../services/authService';

export default {
  components: { SmallMessages },
  data() {
    return {
      APP_ENV,
    };
  },
  setup() {
    return { currentUser };
  },
  async mounted() {},
  methods: {
    // Add functions from authService
    login,
    logout,
  },
};
</script>

<style scoped>
.temp-warning {
  margin: 2rem;
}

.env-warning {
  display: flex;
  justify-content: center;
}
</style>
