<template>
  <div class="main-header">
    <h1>Manage Rescore</h1>
    <p>Latest Rescore : {{ latestRescore() }}</p>
  </div>
  <div class="stepper-container">
    <div v-for="(step, index) in rescore_steps" :key="step.step" class="step">
      <div class="step-line" v-if="index !== 0"></div>
      <button
        class="step-number"
        :class="{ 'selected-step': current_step === step.step }"
        @click="current_step = step.step"
      >
        {{ step.step }}
      </button>
      <div class="step-title">{{ step.title }}</div>
    </div>
  </div>
  <div v-if="Object.keys(open_rescore).length && !is_loading" class="rescore-open">
    <h5>Rescore Open:</h5>
    <p>Started : {{ open_rescore.created_at }}</p>
    <zoa-button label="Continue Rescore" @click="navigateRescore()" class="close-rescore-btn" />
    <zoa-button label="Close Rescore" @click="closeRescore()" />
  </div>
  <div v-else-if="!is_loading" class="rescore-closed">
    <h5>Rescore Status:</h5>
    <p>There is currently no rescore open - please select units and start rescore below</p>
    <div class="rescore-actions">
      <zoa-button label="Start Rescore with Selected Units" @click="createRescore" />
      <zoa-button label="Create new unit" />
    </div>
    <div class="table-container">
      <b-table
        id="unit-table"
        class="unit-table"
        striped
        hover
        responsive
        :items="units"
        :fields="fields"
      >
        <!-- Header checkbox for selecting all rows -->
        <template #head(select)="">
          <zoa-input
            class="check"
            zoa-type="checkbox"
            label=""
            label-position="right"
            v-model="selectAll"
            @change="(newValue) => toggleSelectAll(newValue)"
          />
        </template>

        <!-- Row checkbox -->
        <template #cell(select)="row">
          <zoa-input
            class="check"
            zoa-type="checkbox"
            label-position="none"
            @change="(newValue) => handleCheckboxChange(newValue, row.item)"
            v-model="row.item.selected"
          />
        </template>

        <!-- Custom rendering for the name column -->
        <template #cell(last_rescored)="row">
          {{ formatDate(row.value) }}
        </template>

        <!-- Actions column -->
        <template #cell(actions)="row">
          <zoa-button @click="viewUnit(row.item)" class="view-btn"> View Unit </zoa-button>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import { getGeneric, markRescoreComplete, markRescoreOpen } from '@/services/dataService'
import { currentUser } from '../services/authService'

export default {
  name: 'ManageRescoreView',
  components: {},
  setup() {
    return { currentUser }
  },
  data() {
    return {
      units: [],
      fields: [
        { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Collection Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        { label: 'Last Rescored', key: 'last_rescored' },
        { label: 'Actions', key: 'actions' },
      ],
      selected_unit_ids: [],
      open_rescore: {},
      is_loading: false,
      rescore_steps: [
        { step: 1, title: 'Modify Units' },
        { step: 2, title: 'Update Units' },
        { step: 3, title: 'Rescore Units' },
        { step: 4, title: 'Review' },
      ],
      current_step: 1,
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      // Start loading state so nothing is displayed until data is fetched
      this.is_loading = true
      // Fetch data
      this.units = await getGeneric('units-by-user')
      const rescoreResp = await getGeneric('open-rescore')
      // End loading state
      this.is_loading = false
      // Check if there is an open rescore session
      this.open_rescore = rescoreResp.length > 0 ? rescoreResp[0] : {}
    },
    navigateRescore(rescore_session_id) {
      // Navigate to the rescore page with the session ID as a query parameter
      const temp_id = rescore_session_id || this.open_rescore.rescore_session_id
      this.$router.push({
        name: 'rescore',
        query: {
          rescore_session_id: temp_id,
        },
      })
    },
    handleCheckboxChange(newValue, rowItem) {
      // Update the selected property directly
      rowItem.selected = newValue

      if (newValue) {
        //Add the item to the selected_unit_ids array
        this.selected_unit_ids.push(rowItem.collection_unit_id)
      } else {
        //Remove the item from the selected_unit_ids array
        const indexOfVal = this.selected_unit_ids.indexOf(rowItem.collection_unit_id)
        this.selected_unit_ids.splice(indexOfVal, 1)
      }
    },
    toggleSelectAll(newValue) {
      // Only update currently visible (filtered + paginated) rows
      this.units.forEach((unit) => {
        unit.selected = newValue
      })
      this.updateSelectedUnits()
    },
    updateSelectedUnits() {
      this.selected_unit_ids = this.units
        .filter((unit) => unit.selected)
        .map((unit) => unit.collection_unit_id)
    },
    async createRescore() {
      // Create rescore session with selected units
      markRescoreOpen(this.selected_unit_ids).then((response) => {
        this.open_rescore = response.rescore_session_id
        this.navigateRescore(response.rescore_session_id)
      })
    },
    closeRescore() {
      // Close the rescore session
      markRescoreComplete(this.open_rescore.rescore_session_id)
      this.open_rescore = {}
    },
    latestRescore() {
      // Initialize to a very old date
      let latest_date = new Date(0)
      this.units.forEach((unit) => {
        if (unit.last_rescored) {
          const date = new Date(unit.last_rescored)
          if (!latest_date || date > latest_date) {
            latest_date = date
          }
        }
      })

      return latest_date ? this.formatDate(latest_date) : 'N/A'
    },
    // Navigate to the view unit page
    viewUnit(unit) {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: unit.collection_unit_id,
        },
      })
    },
    // Format date to YYYY-MM-DD
    formatDate(date) {
      return date ? new Date(date).toISOString().split('T')[0] : 'N/A'
    },
  },
  computed: {
    // Handle the select all checkbox
    selectAll: {
      get() {
        return this.units.length > 0 && this.units.every((unit) => unit.selected)
      },
      set(newValue) {
        this.toggleSelectAll(newValue)
      },
    },
  },
}
</script>

<style scoped>
.table-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 1rem;
}
.rescore-open {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 1rem;
  gap: 1rem;
}

/* Stepper */
.stepper-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4rem;
  position: relative;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 6rem;
}

.step-number {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  border: 2px solid #3498db;
  background-color: white;
  color: #3498db;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}
.selected-step {
  background-color: #3498db;
  color: white;
}

.step-title {
  margin-top: 8px;
  font-size: 14px;
  color: #333;
  text-align: center;
}

.step-line {
  position: absolute;
  top: 1.5rem; /* half of button height */
  left: -100%;
  width: 140%;
  height: 2px;
  background-color: #3498db;
  z-index: 0;
}
</style>
