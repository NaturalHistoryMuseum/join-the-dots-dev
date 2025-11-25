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
        <div>
          Delete the following unit{{ selected_units.length > 1 ? 's' : '' }}:
        </div>
        <div class="view-dropdown-field">
          <div
            class="view-field text-left"
            v-for="unit in selected_units"
            :key="unit.collection_unit_id"
          >
            <strong>
              {{ unit.collection_unit_id }} -
              {{ unit.unit_name }}
            </strong>
          </div>
        </div>
        <div class="action-desc">
          <p>
            This will remove the selected unit{{
              selected_units.length > 1 ? 's' : ''
            }}
            from JtD.
          </p>
        </div>

        <div class="confrim-container">
          <zoa-input
            zoa-type="empty"
            :label="`Please provide justification for deleting the unit${selected_units.length > 1 ? 's' : ''}`"
            class="comments-title"
          />
          <textarea
            class="text-area"
            rows="2"
            v-model="justification_text"
          ></textarea>
          <zoa-button
            v-if="justification_text.length > 0"
            class="confirm-btn"
            :label="`Delete Unit${selected_units.length > 1 ? 's' : ''}`"
            @click="handleConfirmChanges"
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
      success: false,
      loading: false,
      justification_text: '',
    };
  },
  methods: {
    async handleConfirmChanges() {
      this.loading = true;
      await submitDataGeneric('delete-units', {
        unit_ids: this.selected_units.map((unit) => unit.collection_unit_id),
        justification: this.justification_text,
      });
      this.loading = false;
      this.success = true;
      if (!this.navigate_on_success) {
        // Emit update
        this.$emit('update:refreshData');
      }
      this.justification_text = '';
    },
    resetModal() {
      this.justification_text = '';
      this.success = false;
      this.loading = false;
    },
    checkRedirect() {
      if (this.navigate_on_success && this.success) {
        // Redirect to view units page
        this.$router.push({ path: '/view-units' });
      } else {
        this.resetModal();
      }
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
