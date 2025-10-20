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
    <template v-slot:button>Mark No Change</template>
    <template v-slot:header> Mark No Change </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div v-if="!success && !loading"></div>
      <div v-if="success && !loading">
        <p>Success</p>
      </div>
      <div v-if="!success && loading">
        <p>loading...</p>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
// import { submitDataGeneric } from '@/services/dataService';

export default {
  name: 'NoRescoreModal',
  props: {},
  data() {
    return {
      confirm_changes: false,
      success: false,
      loading: false,
    };
  },
  methods: {
    resetModal() {
      this.confirm_changes = false;
      this.success = false;
      this.loading = false;
      this.split_new_units = null;
    },
  },
};
</script>

<style></style>
