<script setup>
// import UserSections1 from '@/components/UserSections1.vue'
import UserSections2 from '@/components/UserSections2.vue'
</script>

<template>
  <div class="main-page">
    <div class="main-header">
      <h1>Account</h1>
    </div>
    <div v-if="currentUser" class="account-content">
      <!-- <p>
        {{ currentUser }}
      </p> -->
      <h3>Linked Microsoft Account</h3>
      <div class="indent">
        <p>Name: {{ currentUser.name }}</p>
        <p>Email: {{ currentUser.email }}</p>
        <p>Role : {{ currentUser.role }}</p>
      </div>
      <h3>Role / Access Level</h3>
      <div class="indent">
        <zoa-input zoa-type="dropdown" label="Role" :options="{ options, placeholder }" />
      </div>

      <h3>Assigned Sections</h3>
      <div class="indent">
        <UserSections2 />
        <!-- <UserSections1 /> -->
      </div>
    </div>
    <div v-else>
      <p>you aren't logged in mate</p>
    </div>
  </div>
</template>

<script>
import { currentUser } from '../services/authService'

export default {
  name: 'ViewUnit',
  setup() {
    return { currentUser }
  },
  data() {
    return {
      users: [],
      options: ['Admin', 'Principle Curator in Charge (PCIC)', 'Curator'],
      placeholder: 'Please select',
      // String(currentUser.role).charAt(0).toLocaleUpperCase() + String(currentUser.role).slice(1),
    }
  },
  mounted() {},
  methods: {},
}
</script>

<style scoped>
.account-content {
  align-items: start;
  text-align: left;
  width: 100%;
}
.indent {
  margin: 1rem;
}
</style>
