<template>
  <div class="main-page">
    <div class="main-header">
      <h1>Account</h1>

      <div v-if="currentUser" class="content">
        <!-- Show current user information -->
        <h3>Linked Microsoft Account</h3>
        <div class="indent">
          <p>Name: {{ currentUser.name }}</p>
          <p>Email: {{ currentUser.email }}</p>
          <p>
            Role :
            {{ currentUser.role[0].toUpperCase() + currentUser.role.slice(1) }}
          </p>
          <p>level : {{ currentUser.level }}</p>
          <p>User ID : {{ currentUser.user_id }}</p>
          <p>Assigned Units : {{ currentUser.assigned_units }}</p>
          <p>Division : {{ currentUser.division_id }}</p>
        </div>
        <!-- Edit role -->
        <h3>Role / Access Level</h3>
        <div class="indent">
          <div class="col-md-4">
            <zoa-input
              zoa-type="dropdown"
              label="Role"
              :config="{ options, placeholder }"
              @change="(value) => handleRoleChange(value)"
            />
          </div>
          <div class="col-md-4">
            <zoa-button
              label="Save"
              kind="alt"
              @click="role ? editRole(role) : null"
            />
          </div>
        </div>
        <!-- Edit assigned units -->
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
              @click="
                assigned_units.length > 0 ? assignUnits(assigned_units) : null
              "
            />
          </div>
        </div>
        <!-- Edit division -->
        <h3>Division</h3>
        <div class="indent">
          <p>Division Assigned: {{ division_id }}</p>
          <div class="col-md-4">
            <zoa-input
              zoa-type="dropdown"
              label="Division"
              :config="{ options: division_options }"
              v-model="division_id"
            />
          </div>
          <div class="col-md-4">
            <zoa-button
              label="Save"
              kind="alt"
              @click="division_id ? handleDivisionSave() : null"
            />
          </div>
        </div>
      </div>
      <div v-else>
        <p>You are not currently logged in</p>
      </div>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';
import {
  assignUnits,
  editRole,
  getGenericUser,
  postGenericUser,
} from '@/services/userService';
import { currentUser } from '../services/authService';

export default {
  name: 'ViewUnit',
  setup() {
    return { currentUser };
  },
  data() {
    return {
      users: [],
      role: '',
      options: [],
      placeholder: 'Please select',
      assigned_units: [],
      units: [],
      division_id: '',
      division_options: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    // At functions from userService
    editRole,
    assignUnits,
    // Page specific functions
    async fetchData() {
      // get all roles and set them to options
      getGenericUser(`all-roles`).then((response) => {
        this.options = response.map((role) => ({
          ...role,
          value: role.role_id,
          label: role.role[0].toUpperCase() + role.role.slice(1),
          order: role.role_id,
        }));
      });
      // Get all units
      getGeneric('unit-department').then((response) => {
        this.units = response.map((unit) => ({
          ...unit,
          value: unit.collection_unit_id,
          label: unit.unit_name,
          order: unit.collection_unit_id,
        }));
      });
      getGeneric('all-divisions').then((response) => {
        this.division_options = response.map((division) => ({
          ...division,
          value: division.division_id,
          label: division.division_name,
          order: division.division_id,
        }));
      });
    },
    // Edit role function
    handleRoleChange(value) {
      this.role = value;
    },
    // Save division function
    handleDivisionSave() {
      postGenericUser(
        `update-division`,
        {
          division_id: this.division_id,
        },
        true,
      );
    },
  },
};
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
