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
    <template v-slot:button>Split Unit</template>
    <template v-slot:header> Split Unit </template>
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
      <div v-if="selected_unit && !success && !loading && !included_in_rescore">
        <p>Unit selected for split:</p>
        <p>
          <strong
            >{{ selected_unit.collection_unit_id }} -
            {{ selected_unit.unit_name }}</strong
          >
        </p>

        <!-- <div class="row"> -->
        <p>
          How many units would you like to split this into? (This number should
          include the original unit)
        </p>
        <div class="col-md-6 new-count">
          <zoa-input
            zoa-type="number"
            label="New unit count"
            v-model="split_new_units"
            :config="{ max: 10, min: 2 }"
          />
        </div>
        <div class="confrim-container" v-if="split_new_units >= 2">
          <zoa-button
            class="confirm-btn"
            label="Save Changes"
            @click="handleConfirmChanges"
          />
        </div>
        <div v-else-if="split_new_units == 1">
          You need to pick a number more than 1 to split a unit into multiple
          units.
        </div>
      </div>
      <div v-if="!success && !selected_unit && !loading">
        <p>Please select a unit to split.</p>
      </div>
      <div v-if="success && !loading">
        <p>Split successful! The new units IDs are:</p>
        <div v-for="id in new_units" :key="id">
          <strong>{{ id }}</strong>
        </div>
        <p>
          Make sure to amend the new units as required. The units have been
          automatically assigned to you.
        </p>
      </div>
      <div v-if="!success && loading">
        <p>loading...</p>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import { submitDataGeneric } from '@/services/dataService';
import fieldNameCalc from '@/utils/utils';

export default {
  name: 'SplitModal',
  props: {
    selected_unit: Object,
    navigate_on_success: Boolean,
    included_in_rescore: Boolean,
  },
  data() {
    return {
      confirm_changes: false,
      success: false,
      loading: false,
      split_new_units: null,
      new_units: [],
    };
  },
  methods: {
    fieldNameCalc,
    async handleConfirmChanges() {
      this.loading = true;
      const resp = await submitDataGeneric('split-unit', {
        unit_id: this.selected_unit.collection_unit_id,
        new_count: this.split_new_units,
      });
      if (resp.success) {
        this.success = true;
        this.new_units = resp.new_units;
        this.loading = false;
      }
      this.confirm_changes = false;
      if (!this.navigate_on_success) {
        // Emit update
        this.$emit('update:refreshData');
      }
    },
    resetModal() {
      this.confirm_changes = false;
      this.success = false;
      this.loading = false;
      this.split_new_units = null;
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

.new-count {
  justify-self: center;
}

.action-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 2rem;
  margin-top: 1rem;
  margin: 1rem 2rem 2rem 2rem;
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
