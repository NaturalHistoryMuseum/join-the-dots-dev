<template>
  <div class="rescore">
    <div class="main-header">
      <div class="row">
        <!-- Rescore Details -->
        <div class="col-md-4">
          <h1>Rescore</h1>
          <div v-if="units.length > 0">
            <h5>Units assigned: {{ units.length }}</h5>
            <h5>Units completed: {{ countUnitsCompleted(units) }}</h5>
          </div>
        </div>
        <!-- Actions button group -->
        <div class="col-md-8 actions">
          <ActionsBtnGroup v-if="!rescore_review">
            <BulkEditScoreModal :units="units" />
            <zoa-button kind="alt">See History</zoa-button>
            <zoa-button kind="primary">Other Action</zoa-button>
            <zoa-button kind="alt">Third Action</zoa-button></ActionsBtnGroup
          >
          <zoa-button
            v-if="!success"
            @click="rescore_review = !rescore_review"
            >{{
              rescore_review ? 'Edit scores' : 'Review and commit changes'
            }}</zoa-button
          >
        </div>
      </div>
    </div>

    <!-- Add Collapsible Tabs to show units -->
    <CollapsibleTabs
      :units="units"
      :fetchUnitsData="fetchUnitsData"
      v-if="!rescore_review && !success"
    />
    <div v-if="rescore_review && !success">
      <h2 class="text-center">Review Rescore Changes</h2>
      <p>
        Please review all of the changes below and confirm before submitting
        them. These changes cannot be undone.
      </p>
      <div class="save-changes-container">
        <zoa-input
          class="check"
          zoa-type="checkbox"
          label="Confirm changes"
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
  </div>
</template>

<script>
import ActionsBtnGroup from '@/components/ActionsBtnGroup.vue';
import BulkEditScoreModal from '@/components/BulkEditScoreModal.vue';
import CollapsibleTabs from '@/components/CollapsibleTabs.vue';
import { getGeneric, submitDataGeneric } from '@/services/dataService';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import ReviewUnitChanges from '@/components/ReviewUnitChanges.vue';

export default {
  name: 'RescoreView',
  components: {
    CollapsibleTabs,
    ActionsBtnGroup,
    BulkEditScoreModal,
    ReviewUnitChanges,
  },
  setup() {
    const route = useRoute();

    // Access query parameters
    const rescore_session_id = ref(null);
    onMounted(() => {
      rescore_session_id.value = route.query.rescore_session_id;
    });

    return {
      rescore_session_id,
    };
  },
  data() {
    return {
      units: [],
      show_actions: false,
      rescore_review: false,
      confirm_changes: false,
      success: false,
    };
  },
  mounted() {
    this.fetchUnitsData();
  },
  methods: {
    fetchUnitsData() {
      // Fetch units in this rescore session
      getGeneric(`rescore-units/${this.rescore_session_id}`).then(
        (response) => {
          this.units = response.map((unit) => {
            // Parse category tracking JSON
            unit.category_tracking = JSON.parse(unit.category_tracking);
            unit.ranks_json = JSON.parse(unit.ranks_json);
            unit.metric_json = JSON.parse(unit.metric_json);
            return unit;
          });
        },
      );
    },
    // Function to toggle the visibility of the actions button group
    toggleActions() {
      this.show_actions = !this.show_actions;
    },
    // Function to count the number of completed units
    countUnitsCompleted(units) {
      let completed_count = 0;
      // Loop through each unit and check if all categories are complete
      units.forEach((unit) => {
        const categories_json = unit.category_tracking;
        const completed = categories_json.every((category) => {
          return category.complete == 1;
        });
        if (completed) {
          completed_count++;
        }
      });
      return completed_count;
    },
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

<style>
.prog-bar {
  margin-top: 1rem;
  width: 20rem;
}

/* .main-page {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 2rem;
} */
</style>
