<template>
  <div v-if="!success">
    <h2 class="text-center">Review Rescore Changes</h2>
    <p>
      Please review all of the changes below and confirm before submitting them.
      These changes cannot be undone.
    </p>
    <div class="save-changes-container">
      <zoa-input
        class="check"
        zoa-type="checkbox"
        label="Confirm changes?"
        label-position="left"
        v-model="confirm_changes"
      />
      <zoa-button
        v-if="confirm_changes"
        label="Save Changes and Close Rescore"
        @click="handleSaveChanges"
      />
    </div>
    <ReviewUnitChanges :units="units" />
  </div>
  <div v-if="success">
    <zoa-flash
      kind="success"
      header="Rescore Completed"
      message="Your rescore has been successfully completed. Thank you!"
    />
  </div>
</template>

<script>
import { submitDataGeneric } from '@/services/dataService';

import ReviewUnitChanges from '@/components/ReviewUnitChanges.vue';

export default {
  name: 'ReviewRescoreView',
  components: {
    ReviewUnitChanges,
  },
  props: {
    units: Array,
    rescore_session_id: String,
  },
  data() {
    return { confirm_changes: false, success: false };
  },
  methods: {
    async handleSaveChanges() {
      const response = await submitDataGeneric('rescore-complete', {
        rescore_session_id: this.rescore_session_id,
      });
      if (response.success) {
        this.success = true;
      }
    },
  },
};
</script>

<style></style>
