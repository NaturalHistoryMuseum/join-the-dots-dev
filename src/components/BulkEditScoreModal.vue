nav-container
<template>
  <zoa-modal
    class="modal-btn bulk-modal"
    kind="warning"
    @opened="
      () => {
        resetModal()
        this.$refs.tableCheckbox.resetSelection()
      }
    "
    @closed="
      () => {
        resetModal()
        this.$refs.tableCheckbox.resetSelection()
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
        <div v-if="current_step === 2" class="modal-step-content">
          <p class="text-center">Edit the scores for the selected units.</p>
          <div class="nav-container">
            <zoa-button class="" @click="current_step = current_step - 1">Back</zoa-button>
            <!-- Display the scores for this unit and enable editing for rescore -->
            <zoa-button class="" @click="current_step = current_step + 1">Review Scores</zoa-button>
          </div>
          <UnitScores
            v-if="rank_json.length > 0"
            :unit="unit"
            :rescore="true"
            :bulk_edit="true"
            @newRanks="handleBulkUnitUpdate"
          />
        </div>
        <div v-if="current_step === 3" class="modal-step-content">
          <div v-if="edited_unit">
            <p class="text-center">Confirm the changes you made to the scores.</p>
            <div class="nav-container">
              <zoa-button class="" @click="current_step = current_step - 1">Back</zoa-button>
              <!-- Display the scores for this unit and enable editing for rescore -->
            </div>
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
                @click="$emit('saveChanges')"
              />
            </div>
            <p>These are your changes:</p>
            <div v-for="(criterion, index) in edited_unit.ranks_json" :key="index">
              <h5>{{ criterion[0].criterion_name }}</h5>
              <div class="changed-ranks-container">
                <div
                  v-for="(rank, rankIndex) in criterion"
                  :key="rankIndex"
                  class="changed-rank-item"
                >
                  <p>{{ `Rank ${rank.rank_value} (%)` }}</p>
                  <p>{{ rank.percentage ? rank.percentage * 100 : '0' }}</p>
                  <!-- Rank {{ rank.rank_value }}: {{ rank.percentage * 100 }}% -->
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p class="text-center">No changes made to the scores.</p>
          </div>
        </div>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
import TableCheckbox from '@/views/TableCheckbox.vue'
import StepperComp from './StepperComp.vue'
import UnitScores from './UnitScores.vue'

export default {
  name: 'BulkEditScoreModal',
  components: {
    StepperComp,
    TableCheckbox,
    UnitScores,
  },
  props: {
    units: Array,
  },
  async mounted() {
    const data = await import('../utils/ranks_json_temp.json')
    this.rank_json = data.default
    this.unit.ranks_json = this.rank_json
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
    }
  },
  methods: {
    handleBulkUnitUpdate(updatedUnit) {
      console.log('Bulk unit update:', updatedUnit)
      // Merge the updated ranks into the corresponding unit in your parent data
      this.edited_unit = updatedUnit
      // You might want to emit an event or handle the updated unit further
      // this.$emit('update:unit', this.unit);
    },
    handleStepChange(step) {
      this.current_step = step
    },
    // Reset the current step and selection when the modal is opened
    resetModal() {
      this.current_step = 1
      this.edited_unit = []
      this.confirm_changes = false
    },
  },
}
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

.changed-ranks-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
}
.changed-rank-item {
  width: 20%;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.save-changes-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
  gap: 1rem;
}
</style>
