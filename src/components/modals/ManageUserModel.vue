<template>
  <zoa-modal
    class="modal-btn actions-modal"
    :kind="success ? 'success' : 'warning'"
    @opened="
      () => {
        resetModal();
      }
    "
    @closed="
      () => {
        resetModal();
      }
    "
  >
    <template v-slot:button> Edit Permissions</template>
    <template v-slot:header> {{ local_user.name }} </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div class="show-box" v-show="mode == 'view'">
        <p>
          Here you can view the chosen user and perform actions on their
          account.
        </p>
        <div class="user-action-btns">
          <zoa-button label="Remove User" @click="mode = 'delete'" />
          <zoa-button
            label="Change Assigned / Responsible Units"
            @click="mode = 'units'"
          />
          <zoa-button
            label="Change User's Division"
            @click="mode = 'division'"
          />
          <zoa-button label="Change User's Role" @click="mode = 'role'" />
        </div>
        <div class="row text-left view-user-fields">
          <div class="col-md-4 user-field">
            <zoa-input
              zoa-type="empty"
              label="User ID"
              class="comments-title"
              help="The unique ID assigned to their account"
              help-position="right"
            />
            <p class="view-field">
              {{ local_user.user_id }}
            </p>
          </div>
          <div class="col-md-4 user-field">
            <zoa-input
              zoa-type="empty"
              label="Name"
              class="comments-title"
              help="Name linked to their Microsoft account"
              help-position="right"
            />
            <p class="view-field">
              {{ local_user.name }}
            </p>
          </div>
          <div class="col-md-4 user-field">
            <zoa-input
              zoa-type="empty"
              label="Email"
              class="comments-title"
              help="Email address linked to their Microsoft account"
              help-position="right"
            />
            <p class="view-field">
              {{ local_user.email }}
            </p>
          </div>
          <div class="col-md-4 user-field">
            <zoa-input
              zoa-type="empty"
              label="Role"
              class="comments-title"
              help="The access role assigned to their account for this JtD application"
              help-position="right"
            />
            <p class="view-field">
              {{ local_user.role }}
            </p>
          </div>
          <div class="col-md-4">
            <zoa-input
              zoa-type="empty"
              label="Division"
              class="comments-title"
              help="The division of the organisation they belong to"
              help-position="right"
            />
            <p class="view-field">
              {{ local_user.division_name }}
            </p>
          </div>
        </div>
        <div class="row view-user-fields">
          <div class="dropdown-field view-user-units col-md-6">
            <zoa-input
              zoa-type="empty"
              label="Assigned Units"
              class="comments-title"
              help="The collection units that they are assigned to be able to edit"
              help-position="right"
            />
            <div class="view-dropdown-field">
              <div
                class="view-field"
                v-for="unit in local_user.assigned_units"
                :key="unit"
              >
                {{ unit }} -
                {{
                  units.find((u) => u.collection_unit_id === unit)?.unit_name
                }}
              </div>
            </div>
          </div>
          <div class="dropdown-field view-user-units col-md-6">
            <zoa-input
              zoa-type="empty"
              label="Responsible Units"
              class="comments-title"
              help="The collection units that they are responsible for"
              help-position="right"
            />
            <div class="view-dropdown-field">
              <div
                class="view-field"
                v-for="unit in local_user.responsible_units"
                :key="unit"
              >
                {{ unit }} -
                {{
                  units.find((u) => u.collection_unit_id === unit)?.unit_name
                }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="show-box" v-show="mode !== 'view'">
        <div class="back-btn">
          <zoa-button label="Back" @click="mode = 'view'" class="back-btn" />
        </div>
        <div v-show="mode == 'delete'">
          <h4>Remove User</h4>
          <p>
            To remove this person you will need to nominate another user to
            takeover the units they are responsible for
          </p>
        </div>

        <div
          v-show="mode == 'delete' || mode == 'units'"
          class="row view-user-fields"
        >
          <div class="col-md-5 text-left">
            <div class="required-tag">*</div>
            <zoa-input
              class="field-container"
              zoa-type="dropdown"
              label="New Responsible Curator"
              v-model="new_responsible_curator"
              :config="{
                options: users.filter((u) => u.user_id != user.user_id),
              }"
            />
          </div>
          <div class="col-md-7">
            <div class="dropdown-field">
              <zoa-input
                zoa-type="empty"
                label="Responsible Units"
                class="comments-title"
                help="The collection units that they are responsible for"
                help-position="right"
              />
              <div class="view-dropdown-field">
                <div
                  class="view-field"
                  v-for="unit in local_user.responsible_units"
                  :key="unit"
                >
                  {{ unit }} -
                  {{
                    units.find((u) => u.collection_unit_id === unit)?.unit_name
                  }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="new_responsible_curator" class="confirm-container">
          <zoa-button label="Confirm Remove User" class="confirm-btn" />
        </div>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import { currentUser } from '@/services/authService';
import { getGeneric, submitDataGeneric } from '@/services/dataService';
export default {
  name: 'ManageUserModel',
  props: {
    user: Object,
    users: Array,
  },
  data() {
    return {
      currentUser,
      divisions: [],
      roles: [],
      units: [],
      mode: 'view',
      new_responsible_curator: null,
    };
  },
  mounted() {
    this.fetchAllUnits();
    this.fetchAllDivisions();
    this.fetchAllRoles();
  },
  methods: {
    resetModal() {
      this.mode = 'view';
      this.new_responsible_curator = null;
      this.fetchAllUnits();
      this.fetchAllDivisions();
      this.fetchAllRoles();
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
    async handleChange() {
      switch (this.mode) {
        case 'delete':
          await submitDataGeneric('remove-user', {
            user_id: this.user.user_id,
            new_responsible_curator_id: this.new_responsible_curator,
          });
          break;
      }
    },
  },
  computed: {
    local_user: {
      get() {
        return this.user;
      },
      set(value) {
        return console.log(value);
      },
    },
  },
};
</script>

<style>
.view-user-fields {
  padding: 1rem 2rem;
}

.user-field {
  padding: 0.5rem;
}

.view-dropdown-field {
  height: 10rem;
  overflow-y: scroll;
}

.dropdown-field {
  text-align: left;
}

.view-user-units {
  width: 45%;
}

.user-action-btns {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 1rem;
}

.back-btn {
  display: flex;
  justify-content: flex-start;
  /* margin-bottom: 0.5rem; */
}

.show-box {
  width: 100%;
}

.confirm-container {
  margin: 2rem;
}

.text-left {
  text-align: left;
}
</style>
