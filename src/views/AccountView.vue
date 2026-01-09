<template>
  <div class="account-page">
    <OverlayMessage />
    <h1 class="h1-style">Account</h1>
    <div v-if="currentUser" class="content">
      <div class="account-section">
        <h2 class="h2-style">User Details</h2>
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
              :config="{
                options: role_options.filter(
                  (role) =>
                    parseInt(role.role_id) <= parseInt(currentUser.role_id),
                ),
                placeholder,
              }"
              @change="(value) => handleRoleChange(value)"
              v-model="role_id"
              help="The access role assigned to your account for this JtD application"
              help-position="right"
            />
          </div>
          <div class="account-field" v-if="currentUser.level > 1">
            <zoa-input
              v-if="role_id >= 4"
              zoa-type="dropdown"
              label="Division"
              :config="{ options: division_options }"
              v-model="division_id"
              help="The division of the organisation you belong to"
              help-position="right"
              @change="handleDivisionSave()"
            />
            <div v-else-if="division_options && division_options.length > 0">
              <zoa-input
                zoa-type="empty"
                label="Division"
                class="comments-title"
                help="The division of the organisation you belong to"
                help-position="right"
              />
              <p class="view-field">
                {{
                  division_id
                    ? division_options.find((d) => d.division_id == division_id)
                        .division_name
                    : 'No division selected'
                }}
              </p>
            </div>
          </div>
          <div class="account-field" v-if="currentUser.level > 1">
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
              @change="show_save_btn = true"
            />
            <zoa-button
              label="Save"
              v-if="show_save_btn"
              @click="handleAssignedUnitsSave"
            />
          </div>
          <div
            class="account-field"
            v-if="currentUser.level > 1 && units && units.length > 0"
          >
            <zoa-input
              zoa-type="empty"
              label="Responsible Units"
              class="comments-title"
              help="The collection units you are responsible for"
              help-position="right"
            />
            <div
              class="view-dropdown-field"
              v-if="responsible_units && responsible_units.length > 0"
            >
              <div
                class="view-field"
                v-for="unit in responsible_units"
                :key="unit"
              >
                {{ unit }} -
                {{
                  units.find((u) => u.value.toString() === unit.toString())
                    ?.label
                }}
              </div>
            </div>
            <div v-else class="view-field">
              You are not responsible for any units
            </div>
          </div>
        </div>
      </div>
      <div v-if="role_id >= 3" class="account-section">
        <h2 class="h2-style">Manager Actions</h2>
        <div class="manager-actions">
          <zoa-button
            label="Manage User Permissions"
            @click="$router.push('/user-management')"
          />
          <zoa-button
            kind="alt"
            label="Manage Units Permissions"
            @click="$router.push({ path: '/manage-unit-permissions' })"
          />
        </div>
      </div>
    </div>
    <div v-else>
      <p>You are not currently logged in</p>
    </div>
  </div>
</template>

<script>
import OverlayMessage from '@/components/OverlayMessage.vue';
import { getGeneric, submitDataGeneric } from '@/services/dataService';
import { assignUnits, postGenericUser } from '@/services/userService';
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
      role_options: [],
      placeholder: 'Please select',
      assigned_units: this.currentUser.assigned_units
        ? JSON.parse(this.currentUser.assigned_units).map((unit) =>
            unit.toString(),
          )
        : [],
      responsible_units: this.currentUser.responsible_units
        ? JSON.parse(this.currentUser.responsible_units).map((unit) =>
            unit.toString(),
          )
        : [],
      units: [],
      division_id: this.currentUser.division_id,
      division_options: [],
      show_save_btn: false,
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
      // Get all roles and set them to options
      getGeneric(`all-roles`).then((response) => {
        this.role_options = response.map((role) => ({
          ...role,
          value: role.role_id,
          label: role.role[0].toUpperCase() + role.role.slice(1),
          order: role.role_id,
        }));
      });
      // Get all units
      getGeneric('unit-department').then((response) => {
        this.units = response.map((unit) => ({
          value: unit.collection_unit_id.toString(),
          label: unit.unit_name,
          order: unit.collection_unit_id,
          division_id: unit.division_id,
        }));
      });
      getGeneric('all-divisions').then((response) => {
        this.division_options = response.map((division) => ({
          ...division,
          value: division.division_id.toString(),
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
        this.store.handleChangeResponse(response);
      } catch (error) {
        console.error('Error updating division:', error);
        this.store.addMessage('Something went wrong', 'error');
      }
    },
    // Save assigned units function
    async handleAssignedUnitsSave() {
      if (this.responsible_units.length > 0) {
        this.responsible_units.forEach((unit) => {
          if (!this.assigned_units.includes(unit)) {
            this.assigned_units.push(unit);
          }
        });
      }

      try {
        const response = await submitDataGeneric(`submit-user-assigned`, {
          user_id: this.currentUser.user_id,
          assigned_units: this.assigned_units,
        });
        this.show_save_btn = false;
        this.store.handleChangeResponse(response);
      } catch (error) {
        console.error('Error updating assigned units:', error);
        this.store.addMessage('Something went wrong', 'error');
      }
    },
  },
  computed: {
    filteredUnits() {
      return this.units.filter((unit) => unit.division_id === this.division_id);
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

.account-section {
  margin-bottom: 2rem;
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

.manager-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-start;
}
</style>
