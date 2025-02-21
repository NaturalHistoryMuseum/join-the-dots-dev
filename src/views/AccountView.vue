<script setup>
import UserSections1 from '@/components/UserSections1.vue'
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
        <p>User ID : {{ currentUser.user_id }}</p>
      </div>
      <h3>Role / Access Level</h3>
      <div class="indent">
        <div class="col-md-4">
          <zoa-input
            zoa-type="dropdown"
            label="Role"
            :options="{ options, placeholder }"
            @change="(value) => handleRoleChange(value)"
          />
        </div>
        {{ role }}
        <div class="col-md-4">
          <zoa-button label="Save" kind="alt" @click="role ? editRole(role) : null" />
        </div>
      </div>

      <h3>Assigned Sections</h3>
      <div class="indent">
        <!-- <UserSections2 /> -->
        <UserSections1 />
      </div>
    </div>
    <div v-else>
      <p>you aren't logged in mate</p>
    </div>
  </div>
</template>

<script>
import { currentUser } from '../services/authService'
import { editRole } from '@/services/userService'

export default {
  name: 'ViewUnit',
  setup() {
    return { currentUser }
  },
  data() {
    return {
      users: [],
      role: '',
      options: ['Admin', 'Principle Curator in Charge (PCIC)', 'Curator'],
      placeholder: 'Please select',
      // String(currentUser.role).charAt(0).toLocaleUpperCase() + String(currentUser.role).slice(1),
    }
  },
  mounted() {},
  methods: {
    handleRoleChange(value) {
      console.log('role change')
      this.role = value
    },
  },
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
