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
      <div class="show-box" v-show="mode == 'view' && !success">
        <p>
          Here you can view the chosen user and perform actions on their
          account.
        </p>
        <div class="user-action-btns">
          <zoa-button label="Change User's Role" @click="mode = 'role'" />
          <zoa-button
            label="Change Assigned / Responsible Units"
            @click="mode = 'units'"
          />
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
                  units.find(
                    (u) => u.collection_unit_id.toString() === unit.toString(),
                  )?.unit_name
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
                  units.find(
                    (u) => u.collection_unit_id.toString() === unit.toString(),
                  )?.unit_name
                }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="show-box" v-show="mode !== 'view' && !success">
        <div class="back-btn">
          <zoa-button label="Back" @click="mode = 'view'" class="back-btn" />
        </div>
        <div v-show="mode == 'role'">
          <p class="h4-style">Change Role</p>
          <p>Please select what their new role should be.</p>
          <div class="text-left assigned-units-editor">
            <zoa-input
              zoa-type="dropdown"
              :config="{
                options: roles.filter(
                  (r) =>
                    r.role_id <= currentUser.role_id &&
                    r.role_id !== user.role_id,
                ),
              }"
              label="New Role"
              v-model="new_role"
              @change="new_responsible_curator = null"
            />
          </div>
          <div
            v-show="new_role == 1 && local_user.responsible_units.length > 0"
          >
            <p>
              To demote this person to a Viewer you will need to nominate
              another user to takeover the units they are responsible for
            </p>
            <div class="row view-user-fields">
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
                        units.find(
                          (u) =>
                            u.collection_unit_id.toString() === unit.toString(),
                        )?.unit_name
                      }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="new_role > 1 || local_user.responsible_units.length === 0"
            class="confirm-container"
          >
            <zoa-button
              label="Confirm Role Change"
              class="confirm-btn"
              @click="handleRoleChange"
            />
          </div>
          <div v-else-if="new_responsible_curator" class="confirm-container">
            <zoa-button
              label="Confirm Role Change"
              class="confirm-btn"
              @click="handleRoleToViewer"
            />
          </div>
        </div>
        <div class="show-box" v-show="mode == 'units'">
          <p class="h4-style">Change Assigned Units</p>
          <p>
            Please select the units that should be assigned to this user, this
            allows them to edit said units. Please note you cannot unassign
            units that this user is responsible for.
          </p>
          <div class="text-left assigned-units-editor">
            <zoa-input
              class="field-container"
              zoa-type="multiselect"
              label="Assigned Units"
              v-model="local_user.assigned_units"
              :config="{
                options: units,
                enableSearch: true,
              }"
              @change="handleAssignedUnitsChange"
            />
          </div>
          <zoa-button label="Save Changes" @click="saveAssignedUnits" />
          <p class="h4-style margin-top">Change Responsible Units</p>
          <p>
            Changing the units this user is responsible for can be done per unit
            in the 'Manage Units Permissions' Page.
          </p>
          <zoa-button
            label="Manage Units Permissions"
            @click="$router.push({ path: '/manage-unit-permissions' })"
          />
        </div>
      </div>
      <div v-show="success">Change successful!</div>
    </div>
  </zoa-modal>
</template>

<script>
import { currentUser } from '@/services/authService';
import { submitDataGeneric } from '@/services/dataService';
import { postGenericUser } from '@/services/userService';
export default {
  name: 'ManageUserModel',
  props: {
    user: Object,
    users: Array,
    divisions: Array,
    roles: Array,
    units: Array,
  },
  data() {
    return {
      currentUser,

      mode: 'view',
      new_responsible_curator: null,
      new_role: null,
      success: false,
    };
  },
  mounted() {},
  methods: {
    resetModal() {
      this.mode = 'view';
      this.new_responsible_curator = null;
      this.new_role = null;
      this.success = false;
    },

    async handleRoleToViewer() {
      const response = await postGenericUser(`edit-user-role`, {
        user_id: this.local_user.user_id,
        role_id: this.new_role,
      });
      if (response.success) {
        const reassign_resp = await submitDataGeneric(
          'reassign-responsible-curator',
          {
            old_user_id: this.user.user_id,
            new_user_id: this.new_responsible_curator,
          },
        );
        if (reassign_resp.success) {
          this.success = true;
          this.reloadData();
        }
      } else {
        console.error('Role not changed');
      }
    },
    async handleRoleChange() {
      const response = await postGenericUser(`edit-user-role`, {
        user_id: this.local_user.user_id,
        role_id: this.new_role,
      });
      if (response.success) {
        this.success = true;
        this.reloadData();
      }
    },
    reloadData() {
      this.$emit('update:refreshData');
    },
    handleAssignedUnitsChange() {
      this.local_user.responsible_units.forEach((unit) => {
        if (
          !this.local_user.assigned_units.includes(unit) &&
          !this.local_user.assigned_units.includes(unit.toString())
        ) {
          this.local_user.assigned_units.push(unit);
        }
      });
    },
    async saveAssignedUnits() {
      const response = await submitDataGeneric('submit-user-assigned', {
        user_id: this.local_user.user_id,
        assigned_units: this.local_user.assigned_units,
      });
      if (response.success) {
        this.success = true;
        this.reloadData();
      }
    },
  },
  computed: {
    local_user: {
      get() {
        return this.user;
      },
      // set(value) {
      //   return
      // },
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
  max-height: 10rem;
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
  margin-top: 2rem;
}

.text-left {
  text-align: left;
}

.assigned-units-editor {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.margin-top {
  margin-top: 1rem;
}
</style>
