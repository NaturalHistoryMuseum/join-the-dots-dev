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
    <template v-slot:button> Bulk Edit Permissions </template>
    <template v-slot:header> Bulk Edit Permissions </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div
        v-if="
          selected_units.length > 0 &&
          !success &&
          !loading &&
          !included_in_rescore
        "
      >
        <div class="permissions-fields">
          <p>
            Edit the <strong>Responsible Curator</strong> or
            <strong>Assigned Editors</strong> for the
            <i>{{ selected_units.length }} units</i> selected:
          </p>
          <zoa-input
            class="unit-col"
            zoa-type="dropdown"
            label="Responsible Curator"
            v-model="responsible_curator_id"
            :config="{ options: curators_options }"
            @change="checkResponsibleAssigned"
          />
          <p>
            <i
              >*Please note this will replace the
              <strong>Responsible Curator</strong> for
              <strong>all units selected</strong>*</i
            >
          </p>
          <zoa-input
            class="unit-col"
            zoa-type="multiselect"
            label="Assigned Editors"
            v-model="assigned_editors"
            :config="{
              options: curators_options,
              itemName: 'curator',
              itemNamePlural: 'curators',
              enableSearch: true,
            }"
            @change="checkResponsibleAssigned"
          />
          <p>
            <i
              >*Please note this will replace the
              <strong>Assigned Editors</strong> for
              <strong>all units selected</strong> - so please select all
              Curators that should be assigned*</i
            >
          </p>
        </div>

        <div class="confrim-container">
          <zoa-button
            class="confirm-btn"
            label="Edit all selected units"
            @click="handleConfirmChanges"
          />
        </div>
      </div>
      <div v-if="!success && selected_units.length == 0 && !loading">
        <p>Please select unit(s) to perform this action.</p>
      </div>
      <div v-if="success && !loading">
        <p>Change successful</p>
      </div>
      <div v-if="!success && loading">
        <p>loading...</p>
        <p>please don't close the modal</p>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import { submitDataGeneric } from '@/services/dataService';

export default {
  name: 'BulkEditResponsibility',
  props: {
    selected_units: Array,
    curators_options: Array,
    selected_unit_ids: Array,
  },
  data() {
    return {
      success: false,
      loading: false,
      responsible_curator_id:
        this.selected_units.length > 0 &&
        this.selected_units.every(
          (unit) =>
            unit.responsible_curator_id ==
            this.selected_units[0].responsible_curator_id,
        )
          ? this.selected_units[0].responsible_curator_id
          : null,
      assigned_editors: [],
    };
  },
  methods: {
    async handleConfirmChanges() {
      this.loading = true;
      const response = await submitDataGeneric('bulk-submit-unit-permissions', {
        unit_ids: this.selected_unit_ids,
        assigned_users: this.assigned_editors,
        responsible_curator_id:
          this.responsible_curator_id !=
          this.selected_units[0].responsible_curator_id
            ? this.responsible_curator_id
            : null,
      });
      if (response.success) {
        this.loading = false;
        this.success = true;
        this.$emit('update:refreshData');
      }
    },
    resetModal() {
      this.success = false;
      this.loading = false;
      this.responsible_curator_id =
        this.selected_units.length > 0 &&
        this.selected_units.every(
          (unit) =>
            unit.responsible_curator_id ==
            this.selected_units[0].responsible_curator_id,
        )
          ? this.selected_units[0].responsible_curator_id
          : null;
      this.assigned_editors = [];
      this.checkResponsibleAssigned();
    },
    checkResponsibleAssigned() {
      if (
        !this.assigned_editors.includes(this.responsible_curator_id) &&
        this.responsible_curator_id
      ) {
        this.assigned_editors.push(this.responsible_curator_id);
      }
    },
  },
};
</script>

<style>
.permissions-fields {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
