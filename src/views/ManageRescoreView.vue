<template>
  <div class="main-header">
    <h1>Manage Rescore</h1>
    <p>Latest Rescore : {{ latestRescore() }}</p>
  </div>
  <div
    v-if="Object.keys(open_rescore).length && !is_loading"
    class="rescore-open"
  >
    <h5>Rescore Open:</h5>
    <p>Started : {{ open_rescore.created_at }}</p>
    <zoa-button
      label="Continue Rescore"
      @click="navigateRescore()"
      class="close-rescore-btn"
    />
    <zoa-button label="Close Rescore" @click="closeRescore()" />
  </div>
  <div v-else-if="!is_loading" class="rescore-closed">
    <h5>Rescore Status:</h5>
    <p>
      There is currently no rescore open - please select units and start rescore
      below
    </p>
    <div class="rescore-actions">
      <zoa-button
        label="Start Rescore with Selected Units"
        @click="createRescore"
      />
      <!-- <zoa-button label="Create new unit" /> -->
    </div>
    <div class="table-container">
      <TableCheckbox :units="units" :fields="fields">
        <!-- Custom rendering for a date field -->
        <template #cell(last_rescored)="row">
          {{ formatDate(row.value) }}
        </template>

        <!-- Actions column -->
        <template #cell(actions)="row">
          <zoa-button @click="() => viewUnit(row.item)" class="view-btn">
            View Unit
          </zoa-button>
        </template>
      </TableCheckbox>
    </div>
  </div>
</template>

<script>
import {
  getGeneric,
  markRescoreComplete,
  markRescoreOpen,
} from '@/services/dataService';
import TableCheckbox from '../components/TableCheckbox.vue';
import { currentUser } from '../services/authService';

export default {
  name: 'ManageRescoreView',
  components: { TableCheckbox },
  setup() {
    return { currentUser };
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

      open_rescore: {},
      is_loading: false,
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      // Start loading state so nothing is displayed until data is fetched
      this.is_loading = true;
      // Fetch data
      this.units = await getGeneric('units-by-user');
      const rescoreResp = await getGeneric('open-rescore');
      // End loading state
      this.is_loading = false;
      // Check if there is an open rescore session
      this.open_rescore = rescoreResp.length > 0 ? rescoreResp[0] : {};
    },
    navigateRescore(rescore_session_id) {
      // Navigate to the rescore page with the session ID as a query parameter
      const temp_id =
        rescore_session_id || this.open_rescore.rescore_session_id;
      this.$router.push({
        name: 'rescore',
        query: {
          rescore_session_id: temp_id,
        },
      });
    },

    async createRescore() {
      // Create rescore session with selected units
      markRescoreOpen(this.selectedUnitIds).then((response) => {
        this.open_rescore = response.rescore_session_id;
        this.navigateRescore(response.rescore_session_id);
      });
    },
    closeRescore() {
      // Close the rescore session
      markRescoreComplete(this.open_rescore.rescore_session_id);
      this.open_rescore = {};
    },
    latestRescore() {
      // Initialize to a very old date
      let latest_date = new Date(0);
      this.units.forEach((unit) => {
        if (unit.last_rescored) {
          const date = new Date(unit.last_rescored);
          if (!latest_date || date > latest_date) {
            latest_date = date;
          }
        }
      });

      return latest_date ? this.formatDate(latest_date) : 'N/A';
    },
    // Navigate to the view unit page
    viewUnit(unit) {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: unit.collection_unit_id,
        },
      });
    },
    // Format date to YYYY-MM-DD
    formatDate(date) {
      return date ? new Date(date).toISOString().split('T')[0] : 'No Data';
    },
  },
  computed: {
    selectedUnitIds() {
      // Return the IDs of the selected units
      return this.units.filter((unit) => unit.selected).map((unit) => unit.collection_unit_id);
    },
  },
};
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
