<template>
  <div class="table-container">
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
        :config="{ options: per_page_options, placeholder: 'Rows per page' }"
        label="Rows per page"
        @change="
          (value) => {
            resetPage();
            changePerPage(value);
          }
        "
        v-model="per_page"
      />
    </div>
    <div v-if="selected_unit_ids.length > 0" class="selected-units">
      <slot></slot>
    </div>
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
        <template v-if="hasAssignedUnitsOnPage">
          <zoa-input
            class="check"
            zoa-type="checkbox"
            label=""
            label-position="right"
            v-model="selectAll"
            @change="(newValue) => toggleSelectAll(newValue)"
          />
        </template>
      </template>

      <!-- Row checkbox -->
      <template #cell(select)="row">
        <zoa-input
        v-if="JSON.parse(this.currentUser.assigned_units).includes(
                row.item.collection_unit_id,
              )"
          class="check"
          zoa-type="checkbox"
          label-position="none"
          @change="(newValue) => handleCheckboxChange(newValue, row.item)"
          v-model="row.item.selected"
        />
      </template>

      <!-- Forward slot if custom slot exists, fallback to default - exclude the checkbox column -->
      <template
        v-for="field in fields.filter((col) => col.key != 'select')"
        v-slot:[`cell(${field.key})`]="row"
      >
        <template v-if="$slots[`cell(${field.key})`]">
          <slot :name="`cell(${field.key})`" v-bind="row"></slot>
        </template>
        <template v-else>
          {{ row.value }}
        </template>
      </template>
    </b-table>
  </div>
</template>

<script>
import { currentUser } from '@/services/authService';


export default {
  name: 'TableCheckbox',
  props: {
    units: Array,
    fields: Array,
  },
  setup(){
    return {currentUser};
  },
  data() {
    return {
      selected_unit_ids: [], // Array to hold selected unit IDs
      per_page: 10, // Default rows per page
      per_page_options: [
        { order: 0, value: '10' },
        { order: 1, value: '20' },
        { order: 2, value: '50' },
        { order: 3, value: '100' },
      ],
      current_page: 1,
    };
  },
  mounted(){
    this.per_page = parseInt(localStorage.getItem('per_page_default')) || 10
    this.current_page = parseInt(localStorage.getItem('current_page')) || 1;
  },
  watch: {
    current_page(newPage) {
      localStorage.setItem('current_page', newPage);
    }
  },
  methods: {
    toggleSelectAll(newValue) {
      // Only update currently visible (filtered + paginated + assinged to user) rows
      const assignedUnitIds = JSON.parse(this.currentUser.assigned_units);
      this.paginatedUnits.forEach((unit) => {
        if (assignedUnitIds.includes(unit.collection_unit_id)) {
          unit.selected = newValue;
        }
      });
      this.updateSelectedUnits();
    },
    updateSelectedUnits() {
      this.selected_unit_ids = this.units
        .filter((unit) => unit.selected)
        .map((unit) => unit.collection_unit_id);
    },
    handleCheckboxChange(newValue, rowItem) {
      // Update the selected property directly
      rowItem.selected = newValue;

      if (newValue) {
        //Add the item to the selected_unit_ids array
        this.selected_unit_ids.push(rowItem.collection_unit_id);
      } else {
        //Remove the item from the selected_unit_ids array
        const indexOfVal = this.selected_unit_ids.indexOf(
          rowItem.collection_unit_id,
        );
        this.selected_unit_ids.splice(indexOfVal, 1);
      }
    },
    // Reset selection state for all units
    resetSelection() {
      this.units.forEach((unit) => {
        unit.selected = false;
      });
      this.updateSelectedUnits();
    },
    // Function to reset the current page back to the first page
    resetPage() {
      this.current_page = 1;
    },
    // Function to set the number of rows per page
    changePerPage(value) {
      if (value == null) {
        localStorage.setItem('per_page_default', 10);
        this.per_page = 10;
      } else {
        localStorage.setItem('per_page_default', parseInt(value));
        this.per_page = parseInt(value);
      }
    },
  },
  computed: {
    // Handle the select all checkbox
    selectAll: {
      get() {
        const assignedPaginatedUnits = this.paginatedUnits.filter((unit) =>
          JSON.parse(this.currentUser.assigned_units).includes(
            unit.collection_unit_id,
          ),
        );
        console.log('assignedPaginatedUnits', assignedPaginatedUnits)
        return (
          assignedPaginatedUnits.length > 0 &&
          assignedPaginatedUnits.every((unit) => unit.selected)
        );
      },
      set(newValue) {
        this.toggleSelectAll(newValue);
      },
    },
    paginatedUnits() {
      const start = (this.current_page - 1) * this.per_page;
      const end = start + this.per_page;
      return this.units.slice(start, end); // Paginate only filtered data
    },
    rows() {
      return this.units.length;
    },
    hasAssignedUnitsOnPage() {
    const assignedUnitIds = JSON.parse(this.currentUser.assigned_units);
    return this.paginatedUnits.some(unit =>
      assignedUnitIds.includes(unit.collection_unit_id)
    );
  },

  },
};
</script>

<style scoped>
.table-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.table-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  width: 100%;
}

@media (max-width: 768px) {
  .table-options {
    margin: 1rem 0;
    flex-direction: column;
    align-items: start;
    gap: 1rem;
  }
}
</style>
