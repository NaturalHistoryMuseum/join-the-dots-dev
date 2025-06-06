<template>
  <div class="content">
    <div class="actions-bar">
      <ActionsBtnGroup :force_show="selected_unit_ids.length > 0">
        <zoa-button class="bulk-btn">Bulk Edit</zoa-button>
        <zoa-button class="merge-btn">Combine Units</zoa-button>
        <zoa-button class="delete-btn">Delete Unit(s)</zoa-button>
        <zoa-button class="split-btn">Split Unit(s)</zoa-button>
      </ActionsBtnGroup>
    </div>
    <!-- <div class="action-section" v-if="selected_unit_ids.length > 0">
      <div class="action-station col-md-6">
        <div class="action-header">
          <h4>{{ selected_unit_ids.length }} Units Selected</h4>
        </div>
        <div class="action-content">
          <zoa-button kind="primary">Bulk Edit</zoa-button>
          <zoa-button kind="alt">Combine Units</zoa-button>
          <zoa-button kind="primary">Delete Unit</zoa-button>
          <zoa-button kind="alt">Third Action</zoa-button>
        </div>
      </div>
    </div> -->
    <!-- <div>
      <div v-if="selected_unit_ids.length > 0">
        <h3>Selected Collection Unit IDs:</h3>
        {{ selected_unit_ids.join(', ') }}
      </div>
    </div> -->
    <div class="table-options">
      <!-- Pagination -->
      <b-pagination
        v-model="current_page"
        :total-rows="rows"
        :per-page="per_page"
        aria-controls="unit-table"
        class="customPagination"
      ></b-pagination>
      <!-- Rows per page dropdown -->
      <zoa-input
        zoa-type="dropdown"
        :config="{ options: per_page_options, placeholder: '10' }"
        label="Rows per page"
        @change="
          (value) => {
            resetPage()
            changePerPage(value)
          }
        "
      />
    </div>
    <div class="table-container">
      <div
        class="sidebar"
        :style="{
          width: is_collapsed ? collapsed_width : expanded_width,
        }"
      >
        <div class="sidebar-header">
          <zoa-button @click="toggleSidebar" class="toggle-btn">
            <!-- {{ is_collapsed ? <i class="bi bi-list"></i> : '<' }} -->
            <div v-if="is_collapsed"><i class="bi bi-list btn-icon"></i></div>
            <div v-else><i class="bi bi-x-lg btn-icon"></i></div>
          </zoa-button>
          <div v-if="!is_collapsed">
            <zoa-button
              @click="
                () => {
                  clearFilters()
                  resetPage()
                }
              "
              >Reset Filters</zoa-button
            >
          </div>
        </div>
        <div
          class="tab-container"
          :style="{
            width: is_collapsed ? collapsed_width : expanded_width,
          }"
        >
          <button
            v-for="(tab, index) in filter_tabs"
            :key="index"
            @click="active_tab = index"
            :class="['tab', active_tab === index ? 'active' : '', is_collapsed ? 'icon-only' : '']"
            :style="{
              backgroundColor: active_tab === index ? '#f2bab0' : '#e0e0e0',
              width: is_collapsed ? collapsed_width : expanded_width,
            }"
          >
            <span class="tab-title" v-if="!is_collapsed">{{ tab.label }}</span>
          </button>
        </div>
        <div v-if="!is_collapsed">
          <div class="filters">
            <h4>Filters</h4>

            <zoa-input
              zoa-type="checkbox"
              class="filter"
              label="Show Only Assigned"
              label-position="right"
              v-model="filter_assigned"
            />
            <zoa-input
              zoa-type="checkbox"
              class="filter"
              label="Show Inactive"
              label-position="right"
              v-model="filter_inactive"
            />
            <zoa-input
              zoa-type="textbox"
              class="filter"
              label="Search: Unit ID"
              label-position="above"
              v-model="search_id_query"
              :options="{ placeholder: 'Search...' }"
              @change="(value) => resetPage()"
            />
            <zoa-input
              zoa-type="textbox"
              class="filter"
              label="Search: Unit Name"
              label-position="above"
              v-model="search_name_query"
              :options="{ placeholder: 'Search...' }"
              @change="(value) => resetPage()"
            />
            <zoa-input
              :zoa-type="'multiselect'"
              class="filter"
              label="Search: Section"
              label-position="above"
              @change="(value) => resetPage()"
              :options="{
                options: sections,
                itemName: 'section',
                itemNamePlural: 'sections',
                enableSearch: true,
                itemHeight: 50,
              }"
              v-model="search_section"
            />
            <zoa-input
              :zoa-type="'multiselect'"
              class="filter"
              label="Search: Division"
              label-position="above"
              @change="(value) => resetPage()"
              :options="{
                options: divisions,
                itemName: 'division',
                itemNamePlural: 'divisions',
                enableSearch: true,
                itemHeight: 50,
              }"
              v-model="search_division"
            />
          </div>
        </div>
      </div>
      <!-- Table -->
      <b-table
        id="unit-table"
        class="unit-table"
        striped
        hover
        responsive
        :items="paginatedUnits"
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

        <template #head(section_name)="head"
          ><div class="header-filter">
            <div>{{ head.label }}</div>
            <zoa-input
              :zoa-type="'multiselect'"
              class="filter"
              label="Search: Section"
              label-position="above"
              @change="(value) => resetPage()"
              :options="{
                options: sections,
                itemName: 'section',
                itemNamePlural: 'sections',
                enableSearch: true,
                itemHeight: 50,
              }"
              v-model="search_section"
            /></div
        ></template>

        <template #head(division_name)="head"
          ><div class="header-filter">
            <div>{{ head.label }}</div>
            <zoa-input
              :zoa-type="'multiselect'"
              class="filter"
              label="Search: Division"
              label-position="above"
              @change="(value) => resetPage()"
              :options="{
                options: divisions,
                itemName: 'division',
                itemNamePlural: 'divisions',
                enableSearch: true,
                itemHeight: 50,
              }"
              v-model="search_division"
            /></div
        ></template>

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
        <template #cell(name)="row"> {{ row.value.first }} {{ row.value.last }} </template>

        <!-- Actions column -->
        <template #cell(actions)="row">
          <div class="row-actions">
            <zoa-button @click="viewUnit(row.item)" class="view-btn"> View Unit </zoa-button>
            <zoa-button class="delete-btn">Delete Unit</zoa-button>
          </div>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService'
import { currentUser } from '../services/authService'
import ActionsBtnGroup from './ActionsBtnGroup.vue'

export default {
  components: { ActionsBtnGroup },
  setup() {
    return { currentUser }
  },
  data() {
    return {
      per_page: 10,
      per_page_options: [
        // { order: 0, value: '10' },
        { order: 1, value: '20' },
        { order: 2, value: '50' },
        { order: 3, value: '100' },
      ],
      current_page: 1,
      units: [],
      fields: [
        { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Collection Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        // { label: 'Named Collection', key: 'named_collection' },
        { label: 'Section', key: 'section_name' },
        { label: 'Division', key: 'division_name' },
        // { label: 'Department', key: 'department_name' },
        { label: 'Actions', key: 'actions' },
      ],
      search_name_query: '',
      search_id_query: '',
      search_section: [],
      search_division: [],
      selected_unit_ids: [], // List of selected collection_unit_id
      filter_inactive: false,
      filter_tabs: [
        { id: 0, label: 'All' },
        { id: 1, label: 'Earth Sciences' },
        { id: 2, label: 'Life Sciences' },
        { id: 3, label: 'Library & Archives' },
      ],
      is_collapsed: false,
      active_tab: 0,
      expanded_width: '200px',
      collapsed_width: '50px',
      filter_assigned: true,
    }
  },
  mounted() {
    this.fetchData()
  },
  computed: {
    rows() {
      return this.filteredUnits.length
    },
    sections() {
      //Use map to get unique sections
      const uniqueSections = new Map()

      this.units.forEach((unit) => {
        if (!uniqueSections.has(unit.section_name)) {
          uniqueSections.set(unit.section_name, {
            label:
              unit.section_name.length > 20
                ? unit.section_name.substring(0, 20) + '...'
                : unit.section_name,
            value: unit.section_name,
          })
        }
      })
      // Covert to array
      return Array.from(uniqueSections.values())
    },
    divisions() {
      //Use map to get unique sections
      const uniqueDivision = new Map()

      this.units.forEach((unit) => {
        if (!uniqueDivision.has(unit.division_name)) {
          uniqueDivision.set(unit.division_name, {
            label:
              unit.division_name.length > 20
                ? unit.division_name.substring(0, 20) + '...'
                : unit.division_name,
            value: unit.division_name,
          })
        }
      })
      // Covert to array
      return Array.from(uniqueDivision.values())
    },
    filteredUnits() {
      // Filter the units based on the search queries and selected filters
      return this.units.filter(
        (unit) =>
          // Filter by the users assigned units
          (this.filter_assigned
            ? JSON.parse(this.currentUser.assigned_units).includes(unit.collection_unit_id)
            : true) &&
          // Filter by unit name
          unit.unit_name.toLowerCase().includes(this.search_name_query.toLowerCase()) &&
          // Filter by unit ID
          unit.collection_unit_id.toString().includes(this.search_id_query) &&
          // Filter by section
          (this.search_section.length > 0
            ? this.search_section.includes(unit.section_name.toString())
            : true) &&
          // Filter by division
          (this.search_division.length > 0
            ? this.search_division.includes(unit.division_name.toString())
            : true) &&
          // Filter by department
          (this.active_tab == 0
            ? true
            : unit.department_name.includes(this.filter_tabs[this.active_tab].label)) &&
          // Filter by active/inactive status
          (this.filter_inactive ? true : unit.unit_active == 'yes'),
      )
    },
    paginatedUnits() {
      const start = (this.current_page - 1) * this.per_page
      const end = start + this.per_page
      return this.filteredUnits.slice(start, end) // Paginate only filtered data
    },
    selectAll: {
      get() {
        return this.paginatedUnits.length > 0 && this.paginatedUnits.every((unit) => unit.selected)
      },
      set(newValue) {
        this.toggleSelectAll(newValue)
      },
    },
  },
  methods: {
    fetchData() {
      // Fetch units
      getGeneric('unit-department').then((response) => {
        // Add selected property to each unit
        this.units = response.map((unit) => ({
          ...unit,
          selected: false,
        }))
      })
    },
    // Function to navigate to the unit
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
      this.paginatedUnits.forEach((unit) => {
        unit.selected = newValue
      })
      this.updateSelectedUnits()
    },
    // Reset the selected units
    updateSelectedUnits() {
      this.selected_unit_ids = this.units
        .filter((unit) => unit.selected)
        .map((unit) => unit.collection_unit_id)
    },
    // Function to toggle the visibility of the filters sidebar
    toggleSidebar() {
      this.is_collapsed = !this.is_collapsed
    },
    // Function to reset all filters
    clearFilters() {
      this.search_name_query = ''
      this.search_id_query = ''
      this.active_tab = 0
      this.search_section = []
    },
    // Function to reset the current page back to the first page
    resetPage() {
      this.current_page = 1
    },
    // Function to set the number of rows per page
    changePerPage(value) {
      if (value === null) {
        this.per_page = 10
      } else {
        this.per_page = parseInt(value)
      }
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

<style scoped>
.table-container {
  display: flex;
  flex-direction: row;
}

.sidebar {
  transition: width 0.3s;
  color: white;
  display: flex;
  flex-direction: column;
  margin: 10px;
  width: 50px;
}
.sidebar-header {
  margin-bottom: 1rem;
}

.toggle-btn {
  padding: 10px;
  border: none;
  cursor: pointer;
  width: 3rem;
}

.tab-container {
  display: flex;
  flex-direction: column;
  width: 15rem;
  z-index: 1;
  border-left: 5px solid #f2bab0;
}

.tab-title {
  display: inline-block;
  font-weight: 600;
}

.tab {
  padding: 10px;
  border: none;
  cursor: pointer;
  color: black;
  font-weight: 600;
  text-align: left;
  border-radius: 0px 20px 20px 0px;
  margin-bottom: 5px;
  transition: all 0.3s;
}

.tab.icon-only {
  text-align: center;
}

.content {
  flex: 1;
  width: 100%;
  padding: 10px 20px;
}

.btn-icon {
  font-size: 1.3rem;
  color: black;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters {
  margin-top: 1rem;
  text-align: left;
  color: black;
}

.filter {
  margin-top: 0.5rem;
}

.table-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 2rem;
}

.customPagination {
  margin: 0 !important;
}

.unit-table {
  width: 100%;
}

.header-filter {
  display: flex;
  flex-direction: column;
  font-weight: bold;
  color: black;
  text-align: left;
  min-width: 15rem;
  max-width: 50rem;
}

.actions-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.action-header {
  background-color: #e6fdfd;
  width: 100%;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
.action-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.action-section {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

.action-station {
  /* width: 100%; */

  border: #0dedf7 1px solid;
  border-radius: 10px;
}

.delete-btn {
  background-color: #ff5957;
  /* color: white; */
}

.merge-btn {
  background-color: #0d17f5;
  color: white;
}

.bulk-btn {
  background-color: #00ad00;
  color: white;
}

.split-btn {
  background-color: #ffe600;
  /* color: white; */
}

.row-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
}
@media (max-width: 768px) {
  .table-container {
    flex-direction: column;
  }
  .unit-table {
    font-size: 0.9rem;
  }
  /* .sidebar {
  } */
  .mobile-toggle {
    text-align: center;
    margin-bottom: 10px;
  }
  .table-options {
    margin: 1rem 0;
    flex-direction: column;
    align-items: start;
    gap: 1rem;
  }
  .content {
    padding: 5px 10px;
  }
}
</style>
