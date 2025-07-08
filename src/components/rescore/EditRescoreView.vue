<template>
  <div class="rescore">
    <div class="main-header">
      <div class="row">
        <!-- Rescore Details -->
        <div class="col-md-4">
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
        </div>
      </div>
    </div>

    <!-- Add Collapsible Tabs to show units -->
    <CollapsibleTabs
      :units="units"
      :fetchUnitsData="fetchUnitsData"
      v-if="!rescore_review && !success"
    />
  </div>
</template>

<script>
import ActionsBtnGroup from '../ActionsBtnGroup.vue';
import BulkEditScoreModal from '../BulkEditScoreModal.vue';
import CollapsibleTabs from '../CollapsibleTabs.vue';

export default {
  name: 'EditRescoreView',
  components: {
    CollapsibleTabs,
    ActionsBtnGroup,
    BulkEditScoreModal,
  },
  props: {
    rescore_session_id: String,
    units: Array,
    fetchUnitsData: Function,
  },
  data() {
    return {
      show_actions: false,
    };
  },
  methods: {
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
