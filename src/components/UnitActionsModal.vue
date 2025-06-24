<template>
  <zoa-modal class="modal-btn" :kind="success ? 'success' : 'warning'">
    <template v-slot:button >{{ action.header }}</template>
    <template v-slot:header> {{ action.header }} </template>
    <div class="flex flex-col center gap-4">
      <div v-if="selected_unit_ids.length > 0" >
        <div >{{ action.action }} the following units:</div>
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
      <div v-else>
        <p>Please select units to perform this action.</p>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
export default {
  props: {
    selected_unit_ids: Array,
    action: Object,
  },
  data() {
    return {
      confirm_changes: false,
      success: false,
    };
  },
  methods: {
    handleConformChanges() {
      switch (this.action.action) {
        case 'delete':
          console.log('Deleting units:', this.selected_unit_ids);
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
          console.error('Unknown action ID:', this.action.id);
      }
      this.confirm_changes = false;
      // this.$emit('closeModal');

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
