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
    <template v-slot:button> Upgrade Viewer to Editor</template>
    <template v-slot:header> Upgrade Viewer to Editor </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div class="show-box" v-show="!success && !loading && mode == 'select'">
        <p>
          Select a user to upgrade to an Editor. Please note they will be added
          to your Division.
        </p>
        <div class="viewer-container">
          <div class="field-container text-left">
            <zoa-input
              zoa-type="textbox"
              label="Search Users"
              v-model="search"
              :config="{ placeholder: 'Search: Name, Email' }"
            />
          </div>
          <TableCheckbox :units="filteredViewers" :fields="fields">
            <template #cell(actions)="row">
              <zoa-button
                @click="() => selectViewer(row.item)"
                class="view-btn"
              >
                Upgrade to Editor
              </zoa-button>
            </template>
          </TableCheckbox>
        </div>
      </div>
      <div class="show-box" v-if="!success && !loading && mode == 'confirm'">
        <p>Are you sure you want to upgrade this viewer to an editor?</p>
        <div class="viewer-details">
          <div class="field-container">
            <zoa-input
              zoa-type="empty"
              label="User Name"
              class="comments-title"
              help-position="right"
            />
            <p class="view-field">
              {{ upgrade_user.display_name }}
            </p>
          </div>
          <div class="field-container">
            <zoa-input
              zoa-type="empty"
              label="User Email"
              class="comments-title"
              help-position="right"
            />
            <p class="view-field">
              {{ upgrade_user.email }}
            </p>
          </div>
        </div>
        <div class="confrim-container">
          <p>Please confirm the change</p>
          <zoa-input
            class="check"
            zoa-type="checkbox"
            label="Confirm change"
            label-position="left"
            v-model="confirm_change"
          />
          <zoa-button
            v-if="confirm_change"
            class="confirm-btn"
            label="Upgrade User"
            @click="upgradeViewerToEditor()"
          />
        </div>
      </div>

      <div v-show="success && !loading">Change successful!</div>
      <div v-if="!success && loading">
        <p>loading...</p>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import TableCheckbox from '@/components/TableCheckbox.vue';
import { currentUser } from '@/services/authService';
import { getGenericUser, postGenericUser } from '@/services/userService';
export default {
  name: 'UpgradeViewerModal',
  components: { TableCheckbox },
  props: { divisions: Array },
  data() {
    return {
      currentUser,
      loading: false,
      success: false,
      viewers: [],
      confirm_change: false,
      mode: 'select',
      upgrade_user: [],
      search: '',
      fields: [
        { label: 'User ID', key: 'user_id' },
        { label: 'Name', key: 'display_name' },
        { label: 'Email', key: 'email' },
        { label: 'Role', key: 'role' },
        { label: 'Actions', key: 'actions' },
      ],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const response = await getGenericUser('all-viewers');
        this.viewers = response.map((user) => ({
          ...user,
          selected: false,
        }));
      } catch (error) {
        console.error('Error fetching viewer users:', error);
      } finally {
        this.loading = false;
      }
    },
    async upgradeViewerToEditor() {
      this.loading = true;
      try {
        const response = await postGenericUser('upgrade-viewer', {
          user_id: this.upgrade_user.user_id,
          division_id: this.currentUser.division_id,
        });
        if (response.success) {
          this.success = true;
          this.mode = '';
          this.reloadData();
        }
      } catch (error) {
        console.error('Error upgrading viewer to editor:', error);
      } finally {
        this.loading = false;
      }
    },
    selectViewer(user) {
      this.upgrade_user = user;
      this.mode = 'confirm';
    },
    resetModal() {
      this.success = false;
      this.loadng = false;
      this.mode = 'select';
      this.confirm_change = false;
      this.upgrade_user = [];
      this.search = '';
    },

    reloadData() {
      this.$emit('update:refreshData');
    },
  },
  computed: {
    filteredViewers() {
      if (!this.search) {
        return this.viewers;
      }
      const searchLower = this.search.toLowerCase();
      return this.viewers.filter(
        (user) =>
          user.display_name?.toLowerCase().includes(searchLower) ||
          user.email?.toLowerCase().includes(searchLower),
      );
    },
  },
};
</script>

<style>
.viewer-container {
  max-height: 65vh;
  overflow: auto;
}

.viewer-details {
  display: flex;
  gap: 1rem;
  flex-direction: row;
  justify-content: flex-end;
  text-align: left;
}
</style>
