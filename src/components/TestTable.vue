<template>
  <div class="content">
    <!-- Display the list of selected collection_unit_id -->
    <div>
      <!-- <p>{{ currentPage }} / {{ units.length }}</p> -->
      <div v-if="selectedUnitIds.length > 0">
        <h3>Selected Collection Unit IDs:</h3>
        {{ selectedUnitIds.join(', ') }}
      </div>
    </div>
    <div class="table-options">
      <!-- Pagination -->
      <b-pagination
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        aria-controls="unit-table"
        class="customPagination"
      ></b-pagination>
      <!-- Rows per page dropdown -->
      <zoa-input
        zoa-type="dropdown"
        :options="{ options: perPageOptions, placeholder: '10' }"
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
          width: isCollapsed ? collapsedWidth : expandedWidth,
        }"
      >
        <div class="sidebar-header">
          <zoa-button @click="toggleSidebar" class="toggle-btn">
            <!-- {{ isCollapsed ? <i class="bi bi-list"></i> : '<' }} -->
            <div v-if="isCollapsed"><i class="bi bi-list btn-icon"></i></div>
            <div v-else><i class="bi bi-x-lg btn-icon"></i></div>
          </zoa-button>
          <div v-if="!isCollapsed">
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
            width: isCollapsed ? collapsedWidth : expandedWidth,
          }"
        >
          <button
            v-for="(tab, index) in filterTabs"
            :key="index"
            @click="activeTab = index"
            :class="['tab', activeTab === index ? 'active' : '', isCollapsed ? 'icon-only' : '']"
            :style="{
              backgroundColor: activeTab === index ? '#f2bab0' : '#e0e0e0',
              width: isCollapsed ? collapsedWidth : expandedWidth,
            }"
          >
            <span class="tab-title" v-if="!isCollapsed">{{ tab.label }}</span>
          </button>
        </div>
        <div v-if="!isCollapsed">
          <div class="filters">
            <h4>Filters</h4>
            <zoa-input
              zoa-type="textbox"
              class="filter"
              label="Search: Unit ID"
              label-position="above"
              v-model="searchIdQuery"
              :options="{ placeholder: 'Search...' }"
              @change="(value) => resetPage()"
            />
            <zoa-input
              zoa-type="textbox"
              class="filter"
              label="Search: Unit Name"
              label-position="above"
              v-model="searchNameQuery"
              :options="{ placeholder: 'Search...' }"
              :value="searchSection"
              @change="(value) => resetPage()"
            />
            <!-- <SelectComp :options="sections" label="Search: Section" help="" :multi="true" /> -->
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
              v-model="searchSection"
            />
            <zoa-input
              zoa-type="checkbox"
              class="filter"
              label="Show Inactive"
              label-position="right"
              v-model="filterInActive"
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
          <!-- <b-form-checkbox
          v-model="selectAll"
          @change="(newValue) => toggleSelectAll(newValue)"
          aria-label="Select All"
        ></b-form-checkbox> -->
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
          <!-- <b-form-checkbox
          v-model="row.item.selected"
          @input="(newValue) => handleCheckboxChange(newValue, row.item)"
          aria-label="Select Row"
        ></b-form-checkbox> -->
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
        <template #cell(name)="row"> {{ row.value.first }} {{ row.value.last }} </template>

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
import { getGeneric } from '@/services/dataService'
// import SelectComp from '@/components/SelectComp.vue'

export default {
  components: {
    // SelectComp,
  },
  data() {
    return {
      perPage: 10,
      perPageOptions: [
        // { order: 0, value: '10' },
        { order: 1, value: '20' },
        { order: 2, value: '50' },
        { order: 3, value: '100' },
      ],
      currentPage: 1,
      units: [],
      fields: [
        { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Collection Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        { label: 'Named Collection', key: 'named_collection' },
        { label: 'Section', key: 'section_name' },
        // { label: 'Division', key: 'division_name' },
        { label: 'Department', key: 'department_name' },
        { label: 'Actions', key: 'actions' },
      ],
      searchNameQuery: '',
      searchIdQuery: '',
      searchSection: [],
      selectedUnitIds: [], // List of selected collection_unit_id
      filterInActive: false,
      filterTabs: [
        { id: 0, label: 'All' },
        { id: 1, label: 'Earth Sciences' },
        { id: 2, label: 'Life Sciences' },
        { id: 3, label: 'Library & Archives' },
      ],
      isCollapsed: false,
      activeTab: 0,
      expandedWidth: '200px',
      collapsedWidth: '50px',
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
    filteredUnits() {
      // if (!this.searchQuery) {
      //   return this.units
      // }
      return this.units.filter(
        (unit) =>
          unit.unit_name.toLowerCase().includes(this.searchNameQuery.toLowerCase()) &&
          unit.collection_unit_id.toString().includes(this.searchIdQuery) &&
          (this.searchSection.length > 0
            ? this.searchSection.includes(unit.section_name.toString())
            : true) &&
          (this.activeTab == 0
            ? true
            : unit.department_name.includes(this.filterTabs[this.activeTab].label)) &&
          (this.filterInActive ? true : unit.unit_active == 'yes'),
      )
    },
    paginatedUnits() {
      const start = (this.currentPage - 1) * this.perPage
      const end = start + this.perPage
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
      getGeneric('unit-department').then((response) => {
        this.units = response.map((unit) => ({
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
      // Only update currently visible (filtered + paginated) rows
      this.paginatedUnits.forEach((unit) => {
        unit.selected = newValue
      })
      this.updateSelectedUnits()
    },
    updateSelectedUnits() {
      this.selectedUnitIds = this.units
        .filter((unit) => unit.selected)
        .map((unit) => unit.collection_unit_id)
    },
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
    },
    clearFilters() {
      this.searchNameQuery = ''
      this.searchIdQuery = ''
      this.activeTab = 0
      this.searchSection = []
    },
    resetPage() {
      this.currentPage = 1
    },
    changePerPage(value) {
      if (value === null) {
        this.perPage = 10
      } else {
        this.perPage = parseInt(value)
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

@media (max-width: 768px) {
  .table-container {
    flex-direction: column;
  }
  .unit-table {
    font-size: 0.9rem;
  }
  .sidebar {
    /* width: 100% !important; */
  }
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
