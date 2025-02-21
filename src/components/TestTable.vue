<template>
  <div>
    <!-- Display the list of selected collection_unit_id -->
    <div>
      <h3>Selected Collection Unit IDs:</h3>
      <p>{{ currentPage }} / {{ units.length }}</p>
      <ul>
        <li v-for="id in selectedUnitIds" :key="id">{{ id }}</li>
      </ul>
    </div>

    <!-- Pagination -->
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="unit-table"
      class="customPagination"
    ></b-pagination>

    <!-- Table -->
    <b-table
      id="unit-table"
      striped
      hover
      responsive
      :items="units"
      :fields="fields"
      :per-page="perPage"
      :current-page="currentPage"
    >
      <!-- Header checkbox for selecting all rows -->
      <template #head(select)="">
        <b-form-checkbox
          v-model="selectAll"
          @change="(newValue) => toggleSelectAll(newValue)"
          aria-label="Select All"
        ></b-form-checkbox>
      </template>

      <!-- Row checkbox -->
      <template #cell(select)="row">
        <b-form-checkbox
          v-model="row.item.selected"
          @input="(newValue) => handleCheckboxChange(newValue, row.item)"
          aria-label="Select Row"
        ></b-form-checkbox>
        <p>{{ row.item.selected }}</p>
      </template>

      <!-- Custom rendering for the name column -->
      <template #cell(name)="row"> {{ row.value.first }} {{ row.value.last }} </template>

      <!-- Actions column -->
      <template #cell(actions)="row">
        <b-button size="sm" @click="viewUnit(row.item)" class="mr-1"> View Unit </b-button>
      </template>
    </b-table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      perPage: 50,
      currentPage: 1,
      units: [],
      fields: [
        { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Collection Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        { label: 'Named Collection', key: 'named_collection' },
        { label: 'Section', key: 'section_name' },
        { label: 'Division', key: 'division_name' },
        { label: 'Department', key: 'department_name' },
        { label: 'Actions', key: 'actions' },
      ],
      selectAll: false, // State for the header checkbox
      selectedUnitIds: [], // List of selected collection_unit_id
    }
  },
  computed: {
    rows() {
      return this.units.length
    },
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:5000/api/data/unit-department').then((response) => {
        this.units = response.data.map((unit) => ({
          ...unit,
          selected: false,
        }))
      })
    },
    viewUnit(unit) {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: unit.collection_unit_id,
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
      this.units.forEach((unit) => {
        unit.selected = newValue
      })
      console.log('units:', this.units)
      this.updateSelectedUnits()
    },
  },
}
</script>

<style>
.page-item.active .page-link {
  background-color: var(--secondary-col) !important;
  border-color: var(--secondary-col) !important;
  color: white !important;
}
.page-item .page-link {
  color: var(--primary-col) !important;
}
</style>
