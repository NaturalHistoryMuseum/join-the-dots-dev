<template>
  <zoa-modal
    class="modal-btn bulk-modal"
    :kind="success ? 'success' : 'warning'"
    @opened="
      () => {
        resetModal();
        this.$refs.tableCheckbox.resetSelection();
      }
    "
    @closed="
      () => {
        resetModal();
      }
    "
  >
    <template v-slot:button>Bulk Update</template>
    <template v-slot:header> Bulk Edit Scores </template>
    <div class="flex flex-col gap-4 modal-content">
      <div>
        <StepperComp
          :steps="steps"
          :current_step="current_step"
          @update:current_step="handleStepChange"
        />
        <div v-if="current_step === 1" class="modal-step-content">
          <p class="text-center">Select the units you want to edit.</p>
          <TableCheckbox :fields="fields" :units="units" ref="tableCheckbox">
            <div class="nav-container">
              <div></div>
              <zoa-button
                label="Edit Scores of Selected Units"
                @click="current_step = current_step + 1"
              />
            </div>
          </TableCheckbox>
        </div>
        <div v-show="current_step === 2" class="modal-step-content">
          <div class="nav-container">
            <zoa-button class="" @click="current_step = current_step - 1"
              >Back</zoa-button
            >
            <!-- Display the scores for this unit and enable editing for rescore -->
            <zoa-button class="" @click="current_step = current_step + 1"
              >Review Scores</zoa-button
            >
          </div>
          <p class="text-center">
            Edit the scores for the selected units. Only edited criteria will be
            changed.
          </p>
          <UnitScores
            v-if="rank_json.length > 0"
            :unit="unit"
            :rescore="true"
            :bulk_edit="true"
            @newUnit="handleBulkUnitUpdate"
          />
        </div>
        <div v-show="current_step === 3" class="modal-step-content">
          <div v-if="!loading && !success">
            <div v-if="edited_unit">
              <div class="nav-container">
                <zoa-button class="" @click="current_step = current_step - 1"
                  >Back</zoa-button
                >
                <!-- Display the scores for this unit and enable editing for rescore -->
              </div>
              <p class="text-center">Confirm the changes you made.</p>
              <div class="save-changes-container">
                <zoa-input
                  class="check"
                  zoa-type="checkbox"
                  label="Confirm score changes"
                  label-position="left"
                  v-model="confirm_changes"
                />
                <zoa-button
                  v-if="confirm_changes"
                  label="Save Changes"
                  @click="handleBulkUpload"
                />
              </div>

              <div
                v-if="
                  // edited_unit.metric_json && edited_unit.metric_json.length > 0
                  true
                "
                class="row text-left"
              >
                <div class="col-md-8">
                  <p>These are your changes:</p>
                  <div
                    v-if="
                      edited_unit.metric_json &&
                      edited_unit.metric_json.length > 0
                    "
                  >
                    <h4 class="indent">Metrics</h4>
                    <div
                      v-for="(metric, index) in edited_unit.metric_json"
                      :key="index"
                    >
                      <div class="changed-container metric">
                        <div class="changed-item">
                          <p>{{ fieldNameCalc(metric.metric_name) }}:</p>
                          <p>{{ metric.metric_value }}</p>
                        </div>
                        <div class="changed-item">
                          <p>Confidence:</p>
                          <p>{{ metric.confidence_level }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-if="edited_unit.unit_comment">
                    <h4>Unit Comment</h4>
                    <p>{{ edited_unit.unit_comment }}</p>
                  </div>
                  <div
                    v-if="
                      edited_unit.ranks_json &&
                      edited_unit.ranks_json.length > 0
                    "
                  >
                    <h4 class="indent">Scores</h4>
                    <div
                      v-for="(criterion, index) in edited_unit.ranks_json"
                      :key="index"
                    >
                      <h5>{{ criterion[0].criterion_name }}</h5>
                      <div class="changed-container">
                        <div
                          v-for="(rank, rankIndex) in criterion"
                          :key="rankIndex"
                          class="changed-item"
                        >
                          <p>{{ `Rank ${rank.rank_value} (%)` }}</p>
                          <p>
                            {{ rank.percentage ? rank.percentage * 100 : '0' }}
                          </p>
                          <!-- Rank {{ rank.rank_value }}: {{ rank.percentage * 100 }}% -->
                        </div>
                      </div>
                    </div>
                  </div>
                  <div
                    v-if="
                      !(
                        edited_unit.ranks_json &&
                        edited_unit.ranks_json.length > 0 &&
                        edited_unit.metric_json &&
                        edited_unit.metric_json.length > 0 &&
                        edited_unit.unit_comment
                      )
                    "
                  >
                    <p class="text-center">No changes.</p>
                  </div>
                </div>
                <div class="col-md-4 endited-units">
                  <p>These are the units you are about to edit:</p>
                  <ul class="units-list">
                    <div
                      v-for="unit in units.filter((unit) => unit.selected)"
                      :key="unit.collection_unit_id"
                    >
                      <li>
                        {{ unit.collection_unit_id + ' - ' + unit.unit_name }}
                      </li>
                    </div>
                  </ul>
                </div>
              </div>
            </div>
            <div v-else>
              <p class="text-center">No changes made to the scores.</p>
            </div>
          </div>
          <div v-if="loading">loading...</div>
          <div v-if="success">
            {{ success_message }}
          </div>
        </div>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import { submitDataGeneric } from '@/services/dataService';
import fieldNameCalc from '@/utils/utils';
import StepperComp from '../StepperComp.vue';
import TableCheckbox from '../TableCheckbox.vue';
import UnitScores from '../UnitScores.vue';

export default {
  name: 'BulkEditScoreModal',
  components: {
    StepperComp,
    TableCheckbox,
    UnitScores,
  },
  props: {
    units: Array,
    refresh_page_data: Function,
  },
  async mounted() {
    const data = await import('../../utils/ranks_json_temp.json');
    this.rank_json = data.default;
    this.resetModal();
  },
  data() {
    return {
      steps: [
        {
          step: 1,
          title: 'Select Units',
          description: 'Choose the units you want to edit.',
        },
        {
          step: 2,
          title: 'Edit Scores',
          description: 'Adjust the scores for the selected units.',
        },
        {
          step: 3,
          title: 'Review Changes',
          description: 'Review your changes before saving.',
        },
      ],
      current_step: 1,
      fields: [
        { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Collection Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        // { label: 'Last Rescored', key: 'last_rescored' },
        // { label: 'Actions', key: 'actions' },
      ],
      rank_json: [],
      unit: {
        collection_unit_id: 0,
        ranks_json: this.rank_json,
        metric_json: [],
        category_tracking: [],
        unit_comment_date_added: '',
      },
      confirm_changes: false,
      edited_unit: [],
      success: false,
      success_message: '',
      loading: false,
    };
  },
  methods: {
    fieldNameCalc,
    handleBulkUnitUpdate(updatedUnit) {
      // Merge the updated ranks into the corresponding unit in your parent data
      this.edited_unit = updatedUnit;
    },
    handleStepChange(step) {
      this.current_step = step;
    },
    // Reset the current step and selection when the modal is opened
    resetModal() {
      this.current_step = 1;
      this.edited_unit = [];
      this.confirm_changes = false;
      this.success = false;
      this.success_message = '';
      this.loading = false;
      // Reset the score data
      this.unit.ranks_json = JSON.parse(JSON.stringify(this.rank_json));
    },
    async handleBulkUpload() {
      this.loading = true;
      const response = await submitDataGeneric('bulk-upload-rescore', {
        units: this.units.filter((unit) => unit.selected),
        rescore_data: this.edited_unit,
      });
      this.loading = false;
      this.success = response.success_count > 0;
      this.success_message = `Changes successfully made for ${response.success_count} / ${response.total_units}! ${response.success_count < response.total_units ? 'Please check changes and try again' : ''}`;
      this.refresh_page_data();
    },
  },
};
</script>

<style>
/* Zoe model */
.modal-btn {
  margin: auto;
  z-index: 10;
  /* width: 80vw !important; */
}

.bulk-modal {
  width: 70vw !important;
}

.modal-step-content {
  padding: 1rem;
  margin-top: 1rem;
  max-height: 70vh;
  overflow: auto;
}

.changed-container {
  display: flex;
  flex-direction: row;
  /* justify-content: space-between; */
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  margin-left: 2rem;
  gap: 3rem;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* margin-bottom: 1rem; */
}

.save-changes-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
  margin-bottom: 2rem;
  gap: 1rem;
}
.endited-units {
  border-left: 2px solid black;
}
</style>
