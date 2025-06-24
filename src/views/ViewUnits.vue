<template>
  <div class="main-page">
    <div class="units-content">
      <div class="actions-bar">
        <ActionsBtnGroup :force_show="selectedUnitIds.length > 0">
          <!-- <zoa-button class="bulk-btn">Bulk Edit</zoa-button>
          <zoa-button class="merge-btn">Combine Units</zoa-button>
          <zoa-button class="delete-btn">Delete Unit(s)</zoa-button>
          <zoa-button class="split-btn">Split Unit(s)</zoa-button> -->
          <!-- Add a modal for all actions -->
          <div v-for="action in actions" :key="action.action">
            <UnitActionsModal :action="action" :selected_unit_ids="selectedUnitIds" />
          </div>
        </ActionsBtnGroup>
      </div>
      <div class="content-container">
        <!-- Search bar -->
        <SidebarFilter :units="units"  @update:filteredUnits="handleFilteredUnits"/>
        <!-- Table -->
        <TableCheckbox ref="viewTable" :units="filteredUnits" :fields="fields" >
          <!-- Custom rendering for the name column -->
          <template #cell(name)="row">
            {{ row.value.first }} {{ row.value.last }}
          </template>

          <!-- Actions column -->
          <!-- <template #cell(actions)="row">
            <div class="row-actions">
              <zoa-button @click="viewUnit(row.item)" class="view-btn">
                View Unit
              </zoa-button>
              <zoa-button class="delete-btn">Delete Unit</zoa-button>
            </div>
          </template> -->
          <template #cell(actions)="row">
            <zoa-button @click="() => viewUnit(row.item)" class="view-btn">
              View Unit
            </zoa-button>
          </template>
        </TableCheckbox>
      </div>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';
import SidebarFilter from '@/components/SidebarFilter.vue';
import UnitActionsModal from '@/components/UnitActionsModal.vue';
import ActionsBtnGroup from '@/components/ActionsBtnGroup.vue';
import TableCheckbox from '@/components/TableCheckbox.vue';

export default {
  name: 'ViewUnits',
  components: {
    SidebarFilter,
    UnitActionsModal,
    ActionsBtnGroup,
    TableCheckbox,
  },
  data() {
    return {
      actions: [
        { action: 'Delete', header: 'Delete Units', description: 'This will remove the selected units. This cannot be undone without contacting an admin.' },
        { action: 'Split', header: 'Split Units', description: 'This will split the selected units into different units. This cannot be undone.' },
        { action: 'Combine', header: 'Combine Units', description: 'This will combine the selected units into one new unit. This cannot be undone.' },
        { action: 'Edit', header: 'Bulk Edit Units', description: 'This make changes to the selected units. This cannot be undone.' },
      ],
      units: [],
      fields: [
        { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        // { label: 'Named Collection', key: 'named_collection' },
        { label: 'Section', key: 'section_name' },
        { label: 'Division', key: 'division_name' },
        // { label: 'Department', key: 'department_name' },
        { label: 'Actions', key: 'actions' },
      ],
      filteredUnits: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      // Fetch units
      getGeneric('unit-department').then((response) => {
        // Add selected property to each unit
        this.units = response.map((unit) => ({
          ...unit,
          selected: false,
        }));
      });
    },
    viewUnit(unit) {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: unit.collection_unit_id,
        },
      });
    },
    handleFilteredUnits(filteredUnits) {
      // Only reset pagination if actual filter logic triggered
      if (!this._internalChange) {
        this.filteredUnits = JSON.parse(JSON.stringify(filteredUnits));
        if (filteredUnits.length > 0) {
          this.$refs.viewTable.resetPage();
        }
      }
    }
  },
  computed: {
    // Computed property to get the selected unit IDs
    selectedUnitIds() {
      return this.units.filter(unit => unit.selected).map(unit => unit.collection_unit_id);
    },
  }
};
</script>

<style>
.content-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}
.units-content {
  flex: 1;
  width: 100%;
  /* padding: 10px 20px; */
}

.unit-table {
  width: 100%;
}

.customPagination {
  margin: 0 !important;
}

@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
  }
  .unit-table {
    font-size: 0.9rem;
  }
  .mobile-toggle {
    text-align: center;
    margin-bottom: 10px;
  }

  .units-conten {
    padding: 5px 10px;
  }
}
</style>
