<template>
  <div class="account-page">
    <OverlayMessage />
    <h1>Account</h1>

    <div v-if="currentUser" class="content">
      <div class="account-fields-box">
        <div class="account-field">
          <zoa-input
            zoa-type="empty"
            label="User ID"
            class="comments-title"
            help="The unique ID assigned to this account"
            help-position="right"
          />
          <p class="view-field">{{ currentUser.user_id }}</p>
        </div>
        <div class="account-field">
          <zoa-input
            zoa-type="empty"
            label="Name"
            class="comments-title"
            help="Name linked to your Microsoft account"
            help-position="right"
          />
          <p class="view-field">{{ currentUser.name }}</p>
        </div>
        <div class="account-field">
          <zoa-input
            zoa-type="empty"
            label="Email"
            class="comments-title"
            help="Email address linked to your Microsoft account"
            help-position="right"
          />
          <p class="view-field">{{ currentUser.email }}</p>
        </div>
        <div class="account-field">
          <zoa-input
            zoa-type="dropdown"
            label="Role"
            :config="{ options, placeholder }"
            @change="(value) => handleRoleChange(value)"
            v-model="role_id"
            help="The access role assigned to your account for this JtD application"
            help-position="right"
          />
        </div>
        <div class="account-field">
          <zoa-input
            zoa-type="dropdown"
            label="Division"
            :config="{ options: division_options }"
            v-model="division_id"
            help="The division of the organisation you belong to"
            help-position="right"
            @change="handleDivisionSave()"
          />
        </div>
        <div class="account-field">
          <zoa-input
            zoa-type="multiselect"
            label="Units Assigned"
            :config="{
              options: filteredUnits,
              placeholder,
              enableSearch: true,
            }"
            v-model="assigned_units"
            help="The collection units that are assigned to you"
            help-position="right"
          />
        </div>
      </div>
      <!-- Show current user information -->
      <!-- <h3>Linked Microsoft Account</h3>
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
      <h3>Role / Access Level</h3>
      <div class="indent">
        <div class="account-field">
          <zoa-input
            zoa-type="dropdown"
            label="Role"
            :config="{ options, placeholder }"
            @change="(value) => handleRoleChange(value)"
          />
        </div>
        <div class="account-field">
          <zoa-button
            label="Save"
            kind="alt"
            @click="role ? editRole(role) : null"
          />
        </div>
      </div>
      <h3>Division</h3>
      <div class="indent">
        <p>Division Assigned: {{ division_id }}</p>
        <div class="account-field">
          <zoa-input
            zoa-type="dropdown"
            label="Division"
            :config="{ options: division_options }"
            v-model="division_id"
          />
        </div>
        <div class="account-field">
          <zoa-button
            label="Save"
            kind="alt"
            @click="division_id ? handleDivisionSave() : null"
          />
        </div>
      </div>
      <h3>Assigned Units</h3>
      <div class="indent">
        <p>Units Assigned: {{ assigned_units }}</p>
        <div class="col-md-6">
          <zoa-input
            zoa-type="multiselect"
            label="Units Assigned"
            :config="{
              options: filteredUnits,
              placeholder,
              enableSearch: true,
            }"
            v-model="assigned_units"
          />
        </div>
        <div class="col-md-6">
          <zoa-button
            label="Save"
            kind="alt"
            @click="
              assigned_units.length > 0 ? assignUnits(assigned_units) : null
            "
          />
        </div>
      </div> -->
    </div>
    <div v-else>
      <p>You are not currently logged in</p>
    </div>
  </div>
</template>

<script>
import OverlayMessage from '@/components/OverlayMessage.vue';
import { getGeneric } from '@/services/dataService';
import {
  assignUnits,
  getGenericUser,
  postGenericUser,
} from '@/services/userService';
import { useMessagesStore } from '@/stores/messages';
import { currentUser } from '../services/authService';

export default {
  name: 'ViewUnit',
  setup() {
    const store = useMessagesStore();
    return { currentUser, store };
  },
  components: {
    OverlayMessage,
  },
  data() {
    return {
      users: [],
      role_id: this.currentUser.role_id,
      options: [],
      placeholder: 'Please select',
      assigned_units: [],
      units: [],
      division_id: this.currentUser.division_id,
      division_options: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    // At functions from userService
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
          value: unit.collection_unit_id,
          label: unit.unit_name,
          order: unit.collection_unit_id,
          division_id: unit.division_id,
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
    async handleRoleChange(role) {
      try {
        const response = await postGenericUser(
          `edit-user-role`,
          {
            user_id: currentUser.value.user_id,
            role_id: role,
          },
          true,
        );

        this.store.handleChangeResponse(response);
      } catch (error) {
        console.error('Error updating role:', error);
        this.store.addMessage('Failed to update role', 'error');
      }
    },
    // Save division function
    async handleDivisionSave() {
      try {
        const response = await postGenericUser(
          `update-division`,
          {
            division_id: this.division_id,
          },
          true,
        );

        // ✅ Pass API response to global messages
        this.store.handleChangeResponse(response);
      } catch (error) {
        console.error('Error updating division:', error);
        this.store.addMessage('Something went wrong', 'error');
      }
    },
  },
  computed: {
    filteredUnits() {
      return this.units.filter(
        (unit) => unit.division_id == this.currentUser.division_id,
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

.account-page {
  text-align: left;
  margin: 1rem 4rem;
}

.account-fields-box {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  text-align: left;
  width: 100%;
}

.account-field {
  width: 30%;
}
</style>
