<template>
  <OverlayMessage />

  <div class="main-header">
    <div class="">
      <h1>Manage User Permissions</h1>
      <p>Manage the role and permissions of users in your division</p>
    </div>
  </div>
  <div class="">
    <div class="users-assignment">
      <TableCheckbox
        :units="filtered_users"
        :fields="user_table_fields"
        ref="usersTable"
      >
        <template #cell(edit_user_btn)="row">
          <ManageUserModel
            :user="row.item"
            :users="users"
            @update:refreshData="fetchAllUsers"
            :roles="roles"
            :divisions="divisions"
            :units="units"
          />
        </template>
      </TableCheckbox>
    </div>
  </div>
</template>

<script>
import ManageUserModel from '@/components/modals/ManageUserModal.vue';
import OverlayMessage from '@/components/OverlayMessage.vue';
import TableCheckbox from '@/components/TableCheckbox.vue';
import { currentUser } from '@/services/authService';
import { getGeneric } from '@/services/dataService';
import { useMessagesStore } from '@/stores/messages';

export default {
  name: 'UserManagement',
  components: {
    TableCheckbox,
    OverlayMessage,
    ManageUserModel,
  },
  data() {
    return {
      currentUser,
      sections: [],
      users: [],
      // units: [],
      fields: [
        { label: 'User ID', key: 'user_id' },
        { label: 'Name', key: 'name' },
        { label: 'Role', key: 'role_id' },
        { label: 'Division', key: 'division_id' },
        { label: 'Assigned Units', key: 'assigned_units' },
        { label: 'Responsible Units', key: 'responsible_units' },
      ],
      user_table_fields: [
        { label: 'User ID', key: 'user_id' },
        { label: 'Name', key: 'name' },
        { label: 'Role', key: 'role' },
        { label: 'Email', key: 'email' },
        { label: '', key: 'edit_user_btn' },
      ],
      filtered_users: [],
      divisions: [],
      roles: [],
      units: [],
    };
  },
  setup() {
    const store = useMessagesStore();
    return { store };
  },
  mounted() {
    this.fetchAllUsers();
    this.fetchAllUnits();
    this.fetchAllDivisions();
    this.fetchAllRoles();
  },
  methods: {
    async fetchAllUsers() {
      const response = await getGeneric(`division-users`);
      this.users = response.map((user) => ({
        ...user,
        assigned_units: JSON.parse(user.assigned_units || '[]').map((unit) =>
          unit.toString(),
        ),
        responsible_units: JSON.parse(user.responsible_units || '[]').map(
          (unit) => unit.toString(),
        ),
        value: user.user_id.toString(),
        label: user.name,
      }));
      // Parse json and filter out the current manager
      this.filtered_users = JSON.parse(JSON.stringify(this.users)).filter(
        (u) => u.user_id != this.currentUser.user_id,
      );
    },
    async fetchAllUnits() {
      const response = await getGeneric(
        `units-by-division/${this.currentUser.division_id}`,
      );
      this.units = response.map((unit) => ({
        ...unit,
        value: unit.collection_unit_id.toString(),
        label: unit.unit_name,
      }));
    },
    async fetchAllDivisions() {
      const response = await getGeneric(`all-divisions`);
      this.divisions = response.map((division) => ({
        ...division,
        value: division.division_id.toString(),
        label: division.division_name,
        order: division.division_id,
      }));
    },
    async fetchAllRoles() {
      const response = await getGeneric(`all-roles`);
      this.roles = response.map((role) => ({
        ...role,
        value: role.role_id.toString(),
        label: role.role[0].toUpperCase() + role.role.slice(1),
        order: role.role_id,
      }));
    },
  },
};
</script>

<style>
.user-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-evenly;
}
.user-col {
  width: 18rem;
  text-align: left;
  justify-self: center;
}

.role-col {
  width: 10rem;
  text-align: left;
  justify-self: center;
}
</style>
