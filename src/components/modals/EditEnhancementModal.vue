<template>
  <zoa-modal
    class="modal-btn bulk-modal"
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
    <template v-slot:button>{{
      add_mode ? 'Add Enhancement' : 'Edit Enhancement'
    }}</template>
    <template v-slot:header>
      {{ add_mode ? 'Add Enhancement' : 'Edit Enhancement' }}
    </template>
    <div class="flex flex-col center gap-4 modal-content">
      <div v-if="success" class="text-center">
        <p>Enhancement updated successfully!</p>
      </div>
      <div v-else>
        <div v-if="loading" class="text-center">
          <zoa-loader />
          <p>Submitting changes, please wait...</p>
        </div>
        <div v-else-if="edit_enhancement">
          <p>Please fill out the details below.</p>
          <div class="field-container">
            <div class="required-tag">*</div>
            <zoa-input
              zoa-type="date-simple"
              label="Expected Date"
              v-model="edit_enhancement.expected_date"
            />
          </div>
          <div class="">
            <div class="required-tag">*</div>
            <zoa-input zoa-type="empty" label="Enhancement Description" />
            <textarea
              class="text-area"
              id="Enhancement Description"
              aria-label="Enhancement Description"
              rows="3"
              v-model="edit_enhancement.description"
            ></textarea>
            <div class="modal-actions">
              <zoa-button
                @click="updateEnhancements(edit_enhancement)"
                v-if="
                  edit_enhancement.description.length > 0 &&
                  edit_enhancement.expected_date != ''
                "
                >Save Enhancement</zoa-button
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import { submitDataGeneric } from '@/services/dataService';

export default {
  name: 'EditEnhancementModal',
  props: {
    getEnhancements: Function,
    set_enhancement: Object,
    add_mode: Boolean,
  },
  data() {
    return {
      success: false,
      loading: false,
      edit_enhancement: this.set_enhancement,
    };
  },
  created() {
    this.getEnhancements();
  },
  methods: {
    resetModal() {
      this.success = false;
      this.loading = false;
      this.edit_enhancement = this.set_enhancement;
    },
    addTempexpected_date() {
      this.enhancements.unshift(this.edit_enhancements);
      this.expanded_accordion = 0;
    },
    async updateEnhancements(enhancements) {
      this.loading = true;
      let resp = null;
      if (this.add_mode) {
        resp = await submitDataGeneric('add-enhancements', enhancements);
      } else {
        resp = await submitDataGeneric('update-enhancements', enhancements);
      }
      this.success = resp.success;
      this.loading = false;
      this.getEnhancements();
    },
  },
};
</script>
