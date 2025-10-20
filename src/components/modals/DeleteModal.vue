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
    <template v-slot:button> Delete Unit </template>
    <template v-slot:header> Delete Unit </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div v-if="included_in_rescore">
        <p>
          <strong>
            Warning: this action cannot be performed on a unit that is part of a
            current rescore.
          </strong>
        </p>
        <p>
          <strong>
            Please complete or close the rescore to perform this action.
          </strong>
        </p>
      </div>
      <div
        v-if="
          selected_units.length > 0 &&
          !success &&
          !loading &&
          !included_in_rescore
        "
      >
        <div>Delete the following units:</div>
        <div
          v-for="unit in selected_units"
          :key="unit.collection_unit_id"
          class="units-list"
        >
          <strong>
            {{ unit.collection_unit_id }} -
            {{ unit.unit_name }}
          </strong>
        </div>
        <div class="action-desc">
          <p>This will remove the selected unit(s). This cannot be undone.</p>
        </div>

        <div class="confrim-container">
          <p>Please confirm the change</p>
          <zoa-input
            class="check"
            zoa-type="checkbox"
            label="Confirm change"
            label-position="left"
            v-model="confirm_changes"
          />
          <zoa-button
            v-if="confirm_changes"
            class="confirm-btn"
            label="Delete Unit(s)"
            @click="handleConformChanges"
          />
        </div>
      </div>
      <div v-if="!success && selected_units.length == 0 && !loading">
        <p>Please select unit(s) to perform this action.</p>
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
import { submitDataGeneric } from '@/services/dataService';

export default {
  name: 'DeleteModal',
  props: {
    selected_units: Array,
    navigate_on_success: Boolean,
    included_in_rescore: Boolean,
  },
  data() {
    return {
      confirm_changes: false,
      success: false,
      loading: false,
    };
  },
  methods: {
    async handleConformChanges() {
      this.loading = true;
      await submitDataGeneric('delete-units', {
        unit_ids: this.selected_units.map((unit) => unit.collection_unit_id),
      });
      this.loading = false;
      this.success = true;
      if (this.navigate_on_success) {
        // Wait a moment for user to see the success message
        setTimeout(() => {
          // Redirect to view units page
          this.$router.push({ path: '/view-units' });
        }, 1000);
      } else {
        // Emit update
        this.$emit('update:refreshData');
      }

      this.confirm_changes = false;
    },
    resetModal() {
      this.confirm_changes = false;
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

.action-modal-content {
  text-align: center;
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
