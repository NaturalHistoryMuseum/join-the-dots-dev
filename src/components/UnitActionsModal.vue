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
            label="Confirm change"
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
        <div v-if="action.action.toLowerCase() == 'split'">
          <div class="row">
            <p>
              How many units would you like to split this into? (This number
              should include the original unit. The maximum is 10)
            </p>
            <div class="col-md-4">
              <zoa-input
                zoa-type="number"
                label="New unit count"
                v-model="split_new_units"
                :config="{ max: 10, min: 2 }"
              />
            </div>
            <div class="col-md-8">
              <!-- <p>Current unit name:</p>
              <p>Current unit - Item Count:</p>
              <p>Current unit - Curitorial Item Count:</p>
              <p>Current unit - Barcode Percentage:</p> -->
              <div
                v-for="metric in current_units_metrics"
                :key="metric.collection_unit_metric_id"
                class="row"
              >
                <div class="col-md-6">
                  <!-- <p>
                  Current {{ fieldNameCalc(metric.metric_name) }}:
                  {{ metric.metric_value }}
                </p> -->
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
            </div>
          </div>

          <!-- {{ split_new_units }} -->
          <p>note: get the current metrics</p>
          <div
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
              <!-- <zoa-input
                zoa-type="number"
                label="New unit count"
                :config="{ placeholder: 5000 }"
              /> -->
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
          </div>
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
import { getGeneric, submitDataGeneric } from '@/services/dataService';
import fieldNameCalc from '@/utils/utils';

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
      split_new_units: null, // Specifically for split action
      current_unit_count: 5000,
      current_units_metrics: [],
    };
  },
  watch: {
    selected_unit_ids() {
      this.fetchCurrentMetrics();
    },
  },
  methods: {
    fieldNameCalc,
    async handleConformChanges() {
      switch (this.action.action.toLowerCase()) {
        case 'delete':
          this.loading = true;
          await submitDataGeneric('delete-units', {
            unit_ids: this.selected_unit_ids,
          });
          this.loading = false;
          this.success = true;
          this.$emit('update:refreshData');

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
    async fetchCurrentMetrics() {
      if (
        this.selected_unit_ids.length == 1 &&
        this.action.action.toLowerCase() == 'split'
      ) {
        this.current_units_metrics = await getGeneric(
          `units-metrics/${this.selected_unit_ids[0]}`,
        );
        console.log('current metrics:', this.current_units_metrics);
      }
    },
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
