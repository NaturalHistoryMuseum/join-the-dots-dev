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
    <template v-slot:button> Add New User</template>
    <template v-slot:header> Add New User </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div class="show-box" v-show="!success && !loading">
        <div class="add-user-container">
          <p>To add a new user enter their NHM email.</p>
          <div class="field-container text-left">
            <zoa-input
              zoa-type="textbox"
              label="New User Email"
              v-model="new_email"
            />
          </div>
          <div class="m-1">
            <zoa-button
              label="Check User"
              @click="checkUserEmail"
              v-if="new_email.endsWith('@nhm.ac.uk')"
            />
          </div>
          <div v-if="error_msg">
            <p>{{ error_msg }}</p>
          </div>
          <div class="user-info" v-else-if="new_user.id">
            <p class="user-info-p">User found:</p>
            <div class="field-container text-left">
              <zoa-input
                zoa-type="empty"
                label="Display Name"
                class="comments-title"
                help-position="right"
              />
              <p class="view-field">
                {{ new_user.displayName }}
              </p>
            </div>
            <div class="field-container text-left">
              <zoa-input
                zoa-type="empty"
                label="Job Title"
                class="comments-title"
                help-position="right"
              />
              <p class="view-field">
                {{ new_user.jobTitle }}
              </p>
            </div>
            <div class="field-container text-left">
              <zoa-input
                zoa-type="dropdown"
                label="Division"
                :config="{ options: division_options }"
                v-model="new_division_id"
              />
            </div>
            <div class="field-container text-left">
              <zoa-input
                zoa-type="dropdown"
                label="Role Level"
                :config="{
                  options: role_options.filter(
                    (role) =>
                      parseInt(role.role_id) <= parseInt(currentUser.role_id),
                  ),
                  placeholder,
                }"
                @change="(value) => handleRoleChange(value)"
                v-model="new_role_id"
              />
            </div>
            <div class="field-container">
              <zoa-button
                label="Add User"
                @click="addNewUser"
                v-if="new_division_id && new_role_id"
              />
            </div>
          </div>
        </div>
      </div>

      <div v-show="success && !loading">User added successfully!</div>
      <div v-if="!success && loading">
        <p>loading...</p>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import { currentUser } from '@/services/authService';
import { getUserFromDir, postGenericUser } from '@/services/userService';
export default {
  name: 'AddNewUserModal',
  components: {},
  props: { division_options: Array, role_options: Array },
  data() {
    return {
      currentUser,
      loading: false,
      success: false,
      confirm_change: false,
      new_email: '',
      new_user: {},
      new_role_id: 2,
      new_division_id: null,
      error_msg: '',
    };
  },
  methods: {
    resetModal() {
      this.success = false;
      this.loadng = false;
      this.confirm_change = false;
      this.new_email = '';
      this.error_msg = '';
      this.new_user = {};
      this.new_role_id = 2;
      this.new_division_id = this.currentUser.division_id;
    },
    async checkUserEmail() {
      const data = await getUserFromDir(this.new_email);
      if (data['success']) {
        if (data['new_user']) {
          this.new_user = data['user'] || {};
          this.error_msg = '';
        } else {
          let user = data['user'] || {};
          this.error_msg = `This user already exists ${user.role_id == 1 ? '- their current role is Viewer, you can upgrade them to an Editor.' : ''}`;
        }
      } else {
        this.error_msg = 'No user found with that email address';
      }
    },
    reloadData() {
      this.$emit('update:refreshData');
    },
    async addNewUser() {
      this.loading = true;
      const response = await postGenericUser('add-user', {
        email: this.new_user['mail'],
        azure_id: this.new_user['id'],
        role_id: this.new_role_id,
        division_id: this.new_division_id,
        display_name: this.new_user['displayName'],
      });
      this.loading = false;
      if (response.success) {
        this.success = true;
        this.reloadData();
      } else {
        this.error_msg = 'There was an error adding this user';
      }
    },
  },
};
</script>

<style>
.add-user-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.user-info-p {
  width: 100%;
}
</style>
