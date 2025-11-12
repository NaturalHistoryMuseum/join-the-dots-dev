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
    <template v-slot:button> Raise Issue</template>
    <template v-slot:header> Raise Issue </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div class="show-box" v-show="!success && !loading">
        <p>Please explain your issue below.</p>
        <p>
          <i
            >If your issue is urgent you can reach out to:
            jointhedots@nhm.ac.uk</i
          >
        </p>
        <div class="issue-fields">
          <div class="field-container">
            <div class="required-tag">*</div>
            <zoa-input zoa-type="empty" label="Issue" class="comments-title" />
            <textarea
              class="text-area"
              id="Issue"
              aria-label="Issue"
              rows="3"
              v-model="issue"
            ></textarea>
          </div>

          <div class="field-container">
            <zoa-input
              zoa-type="empty"
              label="User email"
              class="comments-title"
            />
            <p class="view-field">
              {{ currentUser.email }}
            </p>
          </div>
        </div>
        <zoa-button
          v-if="issue"
          class="confirm-btn"
          label="Submit Issue"
          @click="submitIssue"
        />
      </div>
      <div v-show="success && !loading">Issue successfully raised</div>
      <div v-if="!success && loading">
        <p>loading...</p>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import { currentUser } from '@/services/authService';
import { submitDataGeneric } from '@/services/dataService';

export default {
  name: 'FeedbackModal',
  components: {},
  props: {},
  data() {
    return {
      currentUser,
      loading: false,
      success: false,
      confirm_change: false,
      issue: '',
    };
  },
  methods: {
    submitIssue() {
      submitDataGeneric('submit-issue', { issue: this.issue })
        .then((response) => {
          this.success = response.success;
        })
        .catch(() => {
          this.success = false;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    resetModal() {
      this.success = false;
      this.loadng = false;
      this.issue = '';
      this.confirm_change = false;
    },
  },
};
</script>

<style>
.issue-fields {
  display: flex;
  align-items: center;
  justify-content: end;
  text-align: left;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.issue-footer {
  margin-top: 2rem;
}
</style>
