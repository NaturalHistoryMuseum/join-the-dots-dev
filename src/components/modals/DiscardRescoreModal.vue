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
        checkRedirect();
      }
    "
  >
    <template v-slot:button> Discard Rescore </template>
    <template v-slot:header> Discard Rescore </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div v-if="!success && !loading">
        <div>
          Are you sure you want to Discard this Rescore -
          <strong>All changes will be lost.</strong>
        </div>
        <div class="confrim-container">
          <zoa-button
            class="confirm-btn"
            label="Confirm Discard Rescore"
            @click="handleConfirmChanges"
          />
        </div>
      </div>
      <div v-if="success && !loading">
        <p>Delete successful</p>
      </div>
      <div v-if="!success && loading">
        <p>loading...</p>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import { markRescoreComplete } from '@/services/dataService';

export default {
  name: 'DiscardRescoreModal',
  props: {
    rescore_session_id: Number,
    fetchUnitsData: Function,
  },
  data() {
    return {
      success: false,
      loading: false,
    };
  },
  methods: {
    async handleConfirmChanges() {
      this.loading = true;
      await markRescoreComplete(this.rescore_session_id);
      this.loading = false;
      this.success = true;
      this.$router.push('/rescore').then(() => {
        this.$router.go();
      });
      // this.$router.go();
    },
    resetModal() {
      this.success = false;
      this.loading = false;
    },
  },
};
</script>

<style>
/* Zoe model */
.modal-btn {
  margin: auto;
  z-index: 10;
}

.confirm-btn {
  background-color: #fa3608 !important;
}

.action-desc {
  margin-top: 1rem;
}

.confrim-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: auto;
  margin-top: 1rem;
}

.split-unit {
  padding: 1rem;
}

.split-units-container {
  display: flex;
  align-items: center;
  margin: 1rem;
  overflow-y: scroll;
  max-height: 40vh;
}

.actions-modal {
  width: 70vw !important;
}
</style>
