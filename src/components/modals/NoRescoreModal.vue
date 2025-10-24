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
    <template v-slot:button>Mark As No Changes</template>
    <template v-slot:header> Mark No Change </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div v-if="!success && !loading">
        <div v-if="selected_units.length > 0">
          <p>
            Are you sure you want to mark the selected units have had no score
            or measure changes?
          </p>
          <div class="confrim-container">
            <p>Please confirm the change</p>
            <zoa-input
              class="check"
              zoa-type="checkbox"
              label="Confirm Assessment"
              label-position="left"
              v-model="confirm_changes"
            />
            <zoa-button
              v-if="confirm_changes"
              class="confirm-btn"
              label="Confirm No Changes"
              @click="handleConfirmChanges"
            />
            <div
              class="view-dropdown-field"
              v-if="
                selected_units &&
                selected_units.length > 0 &&
                units &&
                units.length > 0
              "
            >
              <div
                class="view-field text-left"
                v-for="unit in selected_units"
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
        <div v-else>
          <p>Please select units.</p>
        </div>
      </div>

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
import { submitDataGeneric } from '@/services/dataService';

export default {
  name: 'NoRescoreModal',
  props: {
    selected_units: Array,
    units: Array,
  },
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
    async handleConfirmChanges() {
      this.loading = true;
      const resp = await submitDataGeneric('update-assessed-date', {
        unit_ids: this.selected_units,
        new_date: new Date().toISOString(),
      });
      this.loading = false;
      if (resp.success) {
        this.success = true;
        this.$emit('update:refreshData');
      } else {
        this.success = false;
      }
    },
  },
};
</script>

<style></style>
