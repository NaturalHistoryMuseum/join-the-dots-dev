<template>
  <div class="rescore">
    <div class="row rescore-helper-container">
      <!-- Rescore Details -->
      <div class="col-md-4 unit-rescore-progress" v-if="units.length > 0">
        <h4 class="progress-msg">
          Units completed: {{ countUnitsCompleted(units) }} /
          {{ units.length }}
        </h4>
        <RoundProgressBar
          :progress="(countUnitsCompleted(units) / units.length) * 100"
        />
      </div>
      <!-- Actions button group -->
      <div class="col-md-8 actions">
        <ActionsBtnGroup v-if="!rescore_review">
          <BulkEditScoreModal
            :units="units"
            v-if="units.length > 1"
            :refresh_page_data="fetchUnitsData"
          />
          <!-- <zoa-button kind="alt">Undo Change</zoa-button>
          <zoa-button kind="primary">Revert All Changes</zoa-button> -->
        </ActionsBtnGroup>
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
import CollapsibleTabs from '../CollapsibleTabs.vue';
import BulkEditScoreModal from '../modals/BulkEditScoreModal.vue';
import RoundProgressBar from '../RoundProgressBar.vue';

export default {
  name: 'EditRescoreView',
  components: {
    CollapsibleTabs,
    ActionsBtnGroup,
    BulkEditScoreModal,
    RoundProgressBar,
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

.unit-rescore-progress {
  text-align: left;
  display: flex;
  align-items: center;
  justify-content: left;
  gap: 1rem;
}

.rescore-helper-container {
  padding: 1rem 1rem;
}

.progress-msg {
  margin: 0;
}
</style>
