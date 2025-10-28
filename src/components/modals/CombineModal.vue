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
    <template v-slot:button>Combine Units</template>
    <template v-slot:header> Combine Units </template>
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
        v-if="selected_units && !success && !loading && !included_in_rescore"
      >
        <p>Unit selected to be combined:</p>
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
        <p class="message">
          Please select the unit that you would like to be the primary unit.
          (The combination will take on all data from this unit and you will
          need to manually make change the new unit)
        </p>
        <zoa-input
          zoa-type="dropdown"
          :config="{
            options: selected_units.map((unit) => ({
              ...unit,
              value: unit.collection_unit_id,
              label: unit.unit_name,
            })),
          }"
          @change="(event) => (primary_unit_id = event)"
          class="col-md-6 new-count"
        />
        <div class="confrim-container" v-if="primary_unit_id">
          <zoa-button
            class="confirm-btn"
            label="Save Changes"
            @click="handleConfirmChanges"
          />
        </div>
      </div>
      <div v-if="!success && !selected_units && !loading">
        <p>Please select a unit to split.</p>
      </div>
      <div v-if="success && !loading">
        <p>Merge successful! The new unit ID is: {{ new_unit_id }}</p>
        <p>
          Make sure to amend the new unit as required. The unit has been
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
  name: 'CombineModal',
  props: {
    selected_units: Object,
    included_in_rescore: Boolean,
  },
  data() {
    return {
      confirm_changes: false,
      success: false,
      loading: false,
      new_unit_id: null,
      primary_unit_id: null,
    };
  },
  methods: {
    fieldNameCalc,
    async handleConfirmChanges() {
      this.loading = true;
      const resp = await submitDataGeneric('combine-unit', {
        primary_unit_id: this.primary_unit_id,
        unit_id_list: this.selected_units.map(
          (unit) => unit.collection_unit_id,
        ),
      });
      if (resp.success) {
        this.success = true;
        this.new_unit_id = resp.new_unit_id;
        this.loading = false;
      }
      this.confirm_changes = false;
      this.$emit('update:refreshData');
    },
    resetModal() {
      this.confirm_changes = false;
      this.success = false;
      this.loading = false;
      this.primary_unit_id = null;
      this.new_unit_id = null;
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

.units-selector-container {
  display: flex;
  align-content: flex-start;
  flex-wrap: wrap;
}

.units-selector {
  margin: 1rem;
}

.message {
  margin-top: 1rem;
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

.actions-modal {
  width: 70vw !important;
}
</style>
