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
    <template v-slot:button>Split Unit</template>
    <template v-slot:header> Split Unit </template>
    <div class="flex flex-col center gap-4 action-modal-content">
      <div v-if="selected_unit && !success && !loading">
        <p>Unit selected for split:</p>
        <p>
          <strong
            >{{ selected_unit.collection_unit_id }} -
            {{ selected_unit.unit_name }}</strong
          >
        </p>

        <!-- <div class="row"> -->
        <p>
          How many units would you like to split this into? (This number should
          include the original unit)
        </p>
        <div class="col-md-6 new-count">
          <zoa-input
            zoa-type="number"
            label="New unit count"
            v-model="split_new_units"
            :config="{ max: 10, min: 2 }"
          />
        </div>
        <!-- <div class="col-md-8">
              <div
                v-for="metric in current_units_metrics"
                :key="metric.collection_unit_metric_id"
                class="row"
              >
                <div class="col-md-6">
                  <zoa-input
                    zoa-type="empty"
                    :label="fieldNameCalc(metric.metric_name)"
                    class="comments-title"
                  />
                  <p class="view-field">{{ metric.metric_value }}</p>
                </div>
                <div class="col-md-6">
                  <zoa-input
                    zoa-type="empty"
                    label="Confidence"
                    class="comments-title"
                  />
                  <p class="view-field">{{ metric.confidence_level }}</p>
                </div>
              </div>
            </div> -->
        <!-- </div> -->

        <!-- {{ split_new_units }} -->
        <!-- <p>note: get the current metrics</p> -->
        <!-- <div
            class="row split-units-container"
            v-if="split_new_units <= 10 && split_new_units > 1"
          >
            <div
              v-for="i in split_new_units"
              :key="i"
              class="col-md-6 split-unit"
            >
              New unit - {{ i }}
              <zoa-input
                zoa-type="textbox"
                label="New unit name"
                :config="{ placeholder: 'This was the original name' }"
              />
              <div
                v-for="metric in current_units_metrics"
                :key="metric.collection_unit_metric_id"
                class="row"
              >
                <div class="col-md-6">
                  <zoa-input
                    zoa-type="number"
                    :label="fieldNameCalc(metric.metric_name)"
                    :config="{ placeholder: metric.metric_value }"
                  />
                </div>
                <div class="col-md-6">
                  <zoa-input
                    zoa-type="dropdown"
                    label="Confidence"
                    :config="{ options: ['High', 'Medium', 'Low'] }"
                  />
                </div>
              </div>
            </div>
          </div> -->
        <div class="confrim-container" v-if="split_new_units >= 2">
          <!-- <p>Please confirm the change</p>
          <zoa-input
            class="check"
            zoa-type="checkbox"
            label="Confirm change"
            label-position="left"
            v-model="confirm_changes"
          /> -->
          <zoa-button
            class="confirm-btn"
            label="Save Changes"
            @click="handleConformChanges"
          />
        </div>
        <div v-else-if="split_new_units == 1">
          You need to pick a number more than 1 to split a unit into multiple
          units.
        </div>
      </div>
      <div v-if="!success && !selected_unit && !loading">
        <p>Please select a unit to split.</p>
      </div>
      <div v-if="success && !loading">
        <p>Split successful! The new units IDs are:</p>
        <ul>
          <li v-for="id in new_units" :key="id">
            {{ id }}
          </li>
        </ul>
        <p>
          Make sure to amend the new units as required. The units have been
          automatically assinged to you.
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
  name: 'SplitModal',
  props: {
    selected_unit: Object,
    navigate_on_success: Boolean,
  },
  data() {
    return {
      confirm_changes: false,
      success: false,
      loading: false,
      split_new_units: null,
      new_units: [],
      // current_unit_count: 5000,
      // current_units_metrics: [],
    };
  },
  // watch: {
  //   selected_unit_ids() {
  //     this.fetchCurrentMetrics();
  //   },
  // },
  methods: {
    fieldNameCalc,
    async handleConformChanges() {
      this.loading = true;
      const resp = await submitDataGeneric('split-unit', {
        unit_id: this.selected_unit.collection_unit_id,
        new_count: this.split_new_units,
      });
      if (resp.success) {
        this.success = true;
        this.new_units = resp.new_units;
        this.loading = false;
      }
      this.confirm_changes = false;
      if (this.navigate_on_success) {
        // Wait a moment for user to see the success message
        setTimeout(() => {
          // Redirect to view units page
          this.$router.push({ path: '/view-units' });
        }, 1000);
      } else {
        // Emit update
        this.$emit('update:refreshData');
      }
    },
    resetModal() {
      this.confirm_changes = false;
      this.success = false;
      this.loading = false;
      this.split_new_units = null;
    },
    // async fetchCurrentMetrics() {
    //   if (
    //     this.selected_unit_ids.length == 1 &&
    //     this.action.action.toLowerCase() == 'split'
    //   ) {
    //     this.current_units_metrics = await getGeneric(
    //       `units-metrics/${this.selected_unit_ids[0]}`,
    //     );
    //   }
    // },
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

.action-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 2rem;
  margin-top: 1rem;
}

.split-unit {
  padding: 1rem;
}

.split-units-container {
  display: flex;
  align-items: center;
  margin: 1rem;
  overflow-y: scroll;
  max-height: 40vh;
}

.actions-modal {
  width: 70vw !important;
}
</style>
