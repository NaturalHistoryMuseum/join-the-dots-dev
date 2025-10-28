<template>
  <div
    class="sidebar"
    :style="{
      width: is_collapsed ? collapsed_width : expanded_width,
    }"
  >
    <div
      v-if="!minimal"
      :class="column_direction ? 'sidebar-header-col' : 'sidebar-header-row'"
    >
      <zoa-button
        @click="toggleSidebar"
        class="toggle-btn"
        :title="is_collapsed ? 'Show Filters' : 'Hide Filters'"
      >
        <!-- {{ is_collapsed ? <i class="bi bi-list"></i> : '<' }} -->
        <div v-if="is_collapsed"><i class="bi bi-list btn-icon"></i></div>
        <div v-else><i class="bi bi-x-lg btn-icon"></i></div>
      </zoa-button>
      <div v-if="!is_collapsed">
        <zoa-button
          @click="
            () => {
              clearFilters();
            }
          "
          >Reset Filters</zoa-button
        >
      </div>
    </div>
    <div
      class="tab-container"
      v-if="show_filters.includes('departments')"
      :style="{
        width: is_collapsed ? collapsed_width : expanded_width,
      }"
    >
      <button
        v-for="(tab, index) in filter_tabs"
        :key="index"
        @click="active_tab = index"
        :class="[
          'tab',
          active_tab === index ? 'active' : '',
          is_collapsed ? 'icon-only' : '',
        ]"
        :style="{
          backgroundColor: active_tab === index ? '#f2bab0' : '#e0e0e0',
          width: is_collapsed ? collapsed_width : '13rem',
        }"
      >
        <span class="tab-title" v-if="!is_collapsed">{{ tab.label }}</span>
      </button>
    </div>
    <div v-if="!is_collapsed">
      <div :class="column_direction ? 'filters-column' : 'filters-row'">
        <h4 v-if="!minimal">Filters</h4>

        <zoa-input
          v-if="show_filters.includes('show_own')"
          zoa-type="checkbox"
          :class="minimal ? '' : 'filter'"
          label="Show Only My Assigned Units"
          label-position="right"
          v-model="filter_assigned"
        />
        <!-- <zoa-input
          zoa-type="checkbox"
          :class="minimal ? '' : 'filter'"
          label="Show Inactive"
          label-position="right"
          v-model="filter_inactive"
        /> -->
        <zoa-input
          v-if="show_filters.includes('unit_id')"
          zoa-type="textbox"
          :class="minimal ? '' : 'filter'"
          label="Search: Unit ID"
          label-position="above"
          v-model="search_id_query"
          :config="{ placeholder: 'Search...' }"
        />
        <zoa-input
          v-if="show_filters.includes('unit_name')"
          zoa-type="textbox"
          :class="minimal ? '' : 'filter'"
          label="Search: Unit Name"
          label-position="above"
          v-model="search_name_query"
          :config="{ placeholder: 'Search...' }"
        />
        <zoa-input
          v-if="show_filters.includes('division')"
          :zoa-type="'multiselect'"
          :class="minimal ? '' : 'filter'"
          label="Search: Division"
          label-position="above"
          :config="{
            options: divisions,
            itemName: 'division',
            itemNamePlural: 'divisions',
            enableSearch: true,
            itemHeight: 50,
          }"
          v-model="search_division"
        />
        <zoa-input
          v-if="show_filters.includes('section')"
          :zoa-type="'multiselect'"
          :class="minimal ? '' : 'filter'"
          label="Search: Section"
          label-position="above"
          :config="{
            options: sections,
            itemName: 'section',
            itemNamePlural: 'sections',
            enableSearch: true,
            itemHeight: 50,
          }"
          v-model="search_section"
        />
        <zoa-input
          v-if="show_filters.includes('curators')"
          :zoa-type="'multiselect'"
          :class="minimal ? '' : 'filter'"
          label="Search: Responsible Curator"
          label-position="above"
          :config="{
            options: responsibleCurators,
            itemName: 'curator',
            itemNamePlural: 'curators',
            enableSearch: true,
            itemHeight: 50,
          }"
          v-model="search_curators"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { currentUser } from '../services/authService';

export default {
  name: 'SidebarFilter',
  props: {
    units: Array,
    show_filters: Array,
    column_direction: Boolean,
    minimal: Boolean,
  },
  setup() {
    return { currentUser };
  },
  data() {
    return {
      active_tab: 0,
      is_collapsed: false,
      expanded_width: this.column_direction ? '325px' : '100%',
      collapsed_width: '50px',
      dropdown_char_limit: 38,
      search_name_query: '',
      search_id_query: '',
      search_section: [],
      search_division: [],
      search_curators: [],
      filter_inactive: false,
      // filter_assigned: this.currentUser.assigned_units ? true : false,
      filter_assigned:
        this.currentUser.assigned_units &&
        this.show_filters.includes('show_own'),
      filter_tabs: [
        { id: 0, label: 'All' },
        { id: 1, label: 'Earth Sciences' },
        { id: 2, label: 'Life Sciences' },
        { id: 3, label: 'Library & Archives' },
      ],
    };
  },
  watch: {
    filteredUnits: {
      handler(newVal) {
        this.$emit('update:filteredUnits', newVal);
      },
      immediate: true,
      deep: true,
    },
  },
  computed: {
    sections() {
      //Use map to get unique sections
      const uniqueSections = new Map();
      // CONCEPT TO MAP JUST THE sections OF THE FILTERED UNITS - DOESNT WORK BECUASE YOU CANT SELECT MULTIPLE sections
      // this.filteredUnits.forEach((unit) => {
      this.units.forEach((unit) => {
        if (!uniqueSections.has(unit.section_name)) {
          uniqueSections.set(unit.section_name, {
            label:
              unit.section_name.length > this.dropdown_char_limit
                ? unit.section_name.substring(0, this.dropdown_char_limit) +
                  '...'
                : unit.section_name,
            value: unit.section_name,
          });
        }
      });
      // Covert to array
      return Array.from(uniqueSections.values());
    },
    divisions() {
      //Use map to get unique divisions
      const uniqueDivision = new Map();
      // CONCEPT TO MAP JUST THE DIVISIONS OF THE FILTERED UNITS - DOESNT WORK BECUASE YOU CANT SELECT MULTIPLE DIVISIONS
      // this.filteredUnits.forEach((unit) => {
      this.units.forEach((unit) => {
        if (!uniqueDivision.has(unit.division_name)) {
          uniqueDivision.set(unit.division_name, {
            label:
              unit.division_name.length > this.dropdown_char_limit
                ? unit.division_name.substring(0, this.dropdown_char_limit) +
                  '...'
                : unit.division_name,
            value: unit.division_name,
          });
        }
      });
      // Covert to array
      return Array.from(uniqueDivision.values());
    },
    responsibleCurators() {
      //Use map to get unique curators
      const uniqueCurators = new Map();
      this.units.forEach((unit) => {
        if (
          !uniqueCurators.has(unit.responsible_curator_id) &&
          unit.curator_name
        ) {
          uniqueCurators.set(unit.responsible_curator_id, {
            label:
              unit.curator_name.length > this.dropdown_char_limit
                ? unit.curator_name.substring(0, this.dropdown_char_limit) +
                  '...'
                : unit.curator_name,
            value: unit.responsible_curator_id.toString(),
          });
        }
      });
      // Covert to array
      return Array.from(uniqueCurators.values());
    },
    filteredUnits() {
      // Filter the units based on the search queries and selected filters
      return this.units.filter(
        (unit) =>
          // Filter by the users assigned units
          (this.filter_assigned
            ? this.currentUser.assigned_units &&
              JSON.parse(this.currentUser.assigned_units).includes(
                unit.collection_unit_id,
              )
            : true) &&
          // Filter by unit name
          unit.unit_name
            .toLowerCase()
            .includes(this.search_name_query.toLowerCase()) &&
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
            : unit.department_name.includes(
                this.filter_tabs[this.active_tab].label,
              )) &&
          // Filter by responsible curator
          (this.search_curators.length > 0
            ? this.search_curators.includes(
                unit.responsible_curator_id.toString()
                  ? unit.responsible_curator_id.toString()
                  : '',
              )
            : true) &&
          // Filter by active/inactive status
          (this.filter_inactive ? true : unit.unit_active == 'yes'),
      );
    },
  },
  methods: {
    // Function to toggle the visibility of the filters sidebar
    toggleSidebar() {
      this.is_collapsed = !this.is_collapsed;
    },
    // Function to reset all filters
    clearFilters() {
      this.search_name_query = '';
      this.search_id_query = '';
      this.active_tab = 0;
      this.search_section = [];
      this.search_division = [];
      this.search_curators = [];
    },
  },
};
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
  margin: 1rem 1rem 0rem 1rem;
  /* width: 50px; */
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
  z-index: 1;
  border-left: 5px solid var(--accent-col);
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

.btn-icon {
  font-size: 1.3rem;
  color: black;
}

.sidebar-header-col {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.sidebar-header-row {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  gap: 5rem;
}

.filters-column {
  margin-top: 1rem;
  text-align: left;
  color: black;
}

.filters-row {
  margin-top: 1rem;
  gap: 2rem;
  text-align: left;
  color: black;
  display: flex;
  flex-direction: row;
  /* align-items: flex-start; */
}

.filter {
  margin-top: 1rem;
}
</style>
