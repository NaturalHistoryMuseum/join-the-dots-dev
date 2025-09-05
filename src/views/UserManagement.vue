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
      <!-- <SidebarFilter
        :users="users"
        :show_filters="['user_id', 'user_name', 'section']"
        :column_direction="false"
        :minimal="true"
        @update:filteredusers="handleFilteredusers"
      /> -->

      <!-- <TableCheckbox :units="filtered_users" :fields="fields" ref="usersTable">
        <template #cell(role_id)="row">
          <zoa-input
            class="role-col"
            zoa-type="dropdown"
            label="Role"
            v-model="row.item.role_id"
            @change="(value) => handleChange(row.item, value)"
            :config="{ options: roles }"
          />
        </template>
        <template #cell(division_id)="row">
          <zoa-input
            class="user-col"
            zoa-type="dropdown"
            label="Division"
            v-model="row.item.division_id"
            @change="(value) => handleChange(row.item, value)"
            :config="{ options: divisions }"
          />
        </template>
        <template #cell(assigned_units)="row">
          <zoa-input
            class="user-col"
            zoa-type="multiselect"
            label="Assigned Units"
            v-model="row.item.assigned_units"
            @change="(value) => handleChange(row.item, value)"
            :config="{ options: units }"
          />
        </template>
      </TableCheckbox> -->
      <TableCheckbox
        :units="filtered_users"
        :fields="user_table_fields"
        ref="usersTable"
      >
        <template #cell(edit_user_btn)="row">
          <ManageUserModel :user="row.item" :users="users" />
        </template>
      </TableCheckbox>
    </div>
  </div>
</template>

<script>
import ManageUserModel from '@/components/modals/ManageUserModel.vue';
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
        // { label: 'Division', key: 'division_id' },
        // { label: 'Assigned Units', key: 'assigned_units' },
        // { label: 'Responsible Units', key: 'responsible_units' },
      ],
      filtered_users: [],
      // divisions: [],
      // roles: [],
    };
  },
  setup() {
    const store = useMessagesStore();
    return { store };
  },
  mounted() {
    // this.fetchAllUnits();
    this.fetchAllUsers();
    // this.fetchAllDivisions();
    // this.fetchAllRoles();
  },
  methods: {
    // async fetchAllUnits() {
    //   const response = await getGeneric(
    //     `units-by-division/${this.currentUser.division_id}`,
    //   );
    //   this.units = response.map((unit) => ({
    //     ...unit,
    //     value: unit.collection_unit_id.toString(),
    //     label: unit.unit_name,
    //   }));
    // },
    // async fetchAllDivisions() {
    //   const response = await getGeneric(`all-divisions`);
    //   this.divisions = response.map((division) => ({
    //     ...division,
    //     value: division.division_id.toString(),
    //     label: division.division_name,
    //     order: division.division_id,
    //   }));
    // },
    // async fetchAllRoles() {
    //   const response = await getGeneric(`all-roles`);
    //   this.roles = response.map((role) => ({
    //     ...role,
    //     value: role.role_id.toString(),
    //     label: role.role[0].toUpperCase() + role.role.slice(1),
    //     order: role.role_id,
    //   }));
    // },
    async fetchAllUsers() {
      const response = await getGeneric(`division-users`);
      this.users = response.map((user) => ({
        ...user,
        assigned_units: JSON.parse(user.assigned_units || '[]'),
        responsible_units: JSON.parse(user.responsible_units || '[]'),
        value: user.user_id.toString(),
        label: user.name,
      }));
      // Parse json and filter out the current manager
      this.filtered_users = JSON.parse(JSON.stringify(this.users)).filter(
        (u) => u.user_id != this.currentUser.user_id,
      );
      console.log(this.users);
    },
  },
};
</script>

<style>
.filters-row {
  display: flex;
  gap: 3rem;
  align-items: center;
  margin-bottom: 20px;
}
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

.table-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  width: 100%;
}
</style>
