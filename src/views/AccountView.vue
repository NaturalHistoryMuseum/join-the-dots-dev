<script setup>
// import UserSections1 from '@/components/UserSections1.vue'
// import UserSections2 from '@/components/UserSections2.vue'
</script>

<template>
  <div class="main-page">
    <div class="main-header">
      <h1>Account</h1>

      <div v-if="currentUser" class="content">
        <h3>Linked Microsoft Account</h3>
        <div class="indent">
          <p>Name: {{ currentUser.name }}</p>
          <p>Email: {{ currentUser.email }}</p>
          <p>Role : {{ currentUser.role[0].toUpperCase() + currentUser.role.slice(1) }}</p>
          <p>User ID : {{ currentUser.user_id }}</p>
          <p>Assigned Units : {{ currentUser.assigned_units }}</p>
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
          <div class="col-md-4">
            <zoa-button label="Save" kind="alt" @click="role ? editRole(role) : null" />
          </div>
        </div>
        <h3>Assigned Units</h3>
        <div class="indent">
          <p>Units Assigned: {{ assigned_units }}</p>
          <div class="col-md-4">
            <zoa-input
              zoa-type="multiselect"
              label="Units Assigned"
              :options="{ options: units, placeholder, enableSearch: true }"
              v-model="assigned_units"
            />
          </div>
          <div class="col-md-4">
            <zoa-button
              label="Save"
              kind="alt"
              @click="assigned_units.length > 0 ? assignUnits(assigned_units) : null"
            />
          </div>
        </div>
        <!-- <h3>Assigned Sections</h3> -->
        <div class="indent">
          <!-- <UserSections2 /> -->
          <!-- <UserSections1 /> -->
        </div>
      </div>
      <div v-else>
        <p>You are not currently logged in</p>
      </div>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService'
import { currentUser } from '../services/authService'
import { editRole, getGenericUser, assignUnits } from '@/services/userService'

export default {
  name: 'ViewUnit',
  setup() {
    return { currentUser }
  },
  data() {
    return {
      users: [],
      role: '',
      options: [],
      placeholder: 'Please select',
      assigned_units: [],
      units: [],
      // String(currentUser.role).charAt(0).toLocaleUpperCase() + String(currentUser.role).slice(1),
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      getGenericUser(`all-roles`).then((response) => {
        this.options = response.map((role) => ({
          ...role,
          value: role.role_id,
          label: role.role[0].toUpperCase() + role.role.slice(1),
          order: role.role_id,
        }))
      })
      getGeneric('unit-department').then((response) => {
        this.units = response.map((unit) => ({
          ...unit,
          value: unit.collection_unit_id,
          label: unit.unit_name,
          order: unit.collection_unit_id,
        }))
      })
    },
    handleRoleChange(value) {
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
