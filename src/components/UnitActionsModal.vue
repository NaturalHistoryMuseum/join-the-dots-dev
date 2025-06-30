<template>
  <zoa-modal
    class="modal-btn"
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
    <template v-slot:button>{{ action.header }}</template>
    <template v-slot:header> {{ action.header }} </template>
    <div class="flex flex-col center gap-4">
      <div v-if="selected_unit_ids.length > 0 && !success && !loading">
        <div>{{ action.action }} the following units:</div>
        <div>
          {{ selected_unit_ids.join(', ') }}
        </div>
        <div class="action-desc">
          <p>{{ action.description }}</p>
        </div>
        <div class="confrim-container">
          <zoa-input
            class="check"
            zoa-type="checkbox"
            label="Confirm score changes"
            label-position="left"
            v-model="confirm_changes"
          />
          <zoa-button
            v-if="confirm_changes"
            class="confirm-btn"
            label="Save Changes"
            @click="handleConformChanges"
          />
        </div>
      </div>
      <div v-if="!success && selected_unit_ids.length == 0 && !loading">
        <p>Please select units to perform this action.</p>
      </div>
      <div v-if="success && !loading">
        <p>{{ action.action }} successful</p>
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
  name: 'UnitActionsModal',
  props: {
    selected_unit_ids: Array,
    action: Object,
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
      switch (this.action.action.toLowerCase()) {
        case 'delete':
          this.loading = true;
          console.log('Deleting units:', this.selected_unit_ids);
          await submitDataGeneric('delete-units', {
            unit_ids: this.selected_unit_ids,
          });
          this.loading = false;
          this.success = true;
          this.$emit('update:refreshData');

          console.log('Deleted');
          break;
        case 'split':
          console.log('Splitting units:', this.selected_unit_ids);
          break;
        case 'combine':
          console.log('Combinging units:', this.selected_unit_ids);
          break;
        case 'edit':
          console.log('Editing units:', this.selected_unit_ids);
          break;
        default:
          console.error('Unknown action ID:', this.action.action);
      }
      this.confirm_changes = false;
      // this.$emit('closeModal');
    },
    resetModal() {
      this.confirm_changes = false;
      this.success = false;
    },
  },
};
</script>

<style scoped>
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
</style>
