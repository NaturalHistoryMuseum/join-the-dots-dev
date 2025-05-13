<template>
  <div class="main-header">
    <h1>Manage Rescore</h1>
    <p>Latest Rescore : {{ latestRescore() }}</p>
  </div>
  <div v-if="Object.keys(open_rescore).length && !is_loading" class="rescore-open">
    <h5>Rescore Open:</h5>
    <p>Started : {{ open_rescore.created_at }}</p>
    <zoa-button label="Continue Rescore" @click="navigateRescore()" class="close-rescore-btn" />
    <zoa-button label="Close Rescore" @click="closeRescore()" />
  </div>
  <!-- <div class="">
    <zoa-input zoa-type="textbox" label="Section to rescore (temp)" v-model="sectionId" />
    <zoa-button label="Start Rescore" @click="navigateRescore()" />
  </div> -->
  <div v-else-if="!is_loading" class="rescore-closed">
    <h5>Rescore Status:</h5>
    <p>There is currently no rescore open - please select units and start rescore below</p>
    <div class="table-container">
      <zoa-button label="Start Rescore with Selected Units" @click="createRescore" />

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
          <!-- <p>{{ row.item.selected }}</p> -->
        </template>

        <!-- Custom rendering for the name column -->
        <template #cell(last_rescored)="row">
          {{ formatDate(row.value) }}
        </template>

        <!-- Actions column -->
        <template #cell(actions)="row">
          <!-- <b-button size="sm" @click="viewUnit(row.item)" class="mr-1"> View Unit </b-button> -->
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
      sectionId: 1,
      units: [],
      fields: [
        { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Collection Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        { label: 'Last Rescored', key: 'last_rescored' },
        { label: 'Actions', key: 'actions' },
      ],
      selectedUnitIds: [],
      open_rescore: {},
      is_loading: false,
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      this.is_loading = true
      this.units = await getGeneric('units-by-user')
      const rescoreResp = await getGeneric('open-rescore')
      this.is_loading = false
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
        //Add the item to the selectedUnitIds array
        this.selectedUnitIds.push(rowItem.collection_unit_id)
      } else {
        //Remove the item from the selectedUnitIds array
        const indexOfVal = this.selectedUnitIds.indexOf(rowItem.collection_unit_id)
        this.selectedUnitIds.splice(indexOfVal, 1)
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
      this.selectedUnitIds = this.units
        .filter((unit) => unit.selected)
        .map((unit) => unit.collection_unit_id)
    },
    async createRescore() {
      // Create rescore session with selected units
      // const rescore_session = await markRescoreOpen(this.selectedUnitIds)
      markRescoreOpen(this.selectedUnitIds).then((response) => {
        this.open_rescore = response.rescore_session_id
        this.navigateRescore(response.rescore_session_id)
      })
    },
    closeRescore() {
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
    viewUnit(unit) {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: unit.collection_unit_id,
        },
      })
    },
    formatDate(date) {
      return date ? new Date(date).toISOString().split('T')[0] : 'N/A'
    },
  },
  computed: {
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
</style>
