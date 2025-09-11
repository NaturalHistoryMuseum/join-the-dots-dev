<template>
  <OverlayMessage />
  <div class="main-header">
    <div class="">
      <h1>Manage Units Permissions</h1>
      <p>Manage who can edit units under you.</p>
    </div>
  </div>
  <div class="">
    <div class="units-assignment">
      <SidebarFilter
        :units="units"
        :show_filters="['unit_id', 'unit_name', 'section', 'curators']"
        :column_direction="false"
        :minimal="true"
        @update:filteredUnits="handleFilteredUnits"
      />
      <TableCheckbox :units="filtered_units" :fields="fields" ref="unitsTable">
        <template #cell(responsible_curator_id)="row">
          <zoa-input
            class="unit-col"
            zoa-type="dropdown"
            label="Responsible Curator"
            v-model="row.item.responsible_curator_id"
            @change="(value) => handleResponibleChange(row.item, value)"
            :config="{ options: curators_options }"
          />
        </template>
        <template #cell(assigned_editors)="row">
          <zoa-input
            class="unit-col"
            zoa-type="multiselect"
            label="Assigned Editors"
            v-model="row.item.assigned_editors"
            :config="{ options: curators_options }"
            @change="(value) => handleEditorsChange(row.item, value, true)"
          />
        </template>
      </TableCheckbox>
    </div>
  </div>
</template>

<script>
import OverlayMessage from '@/components/OverlayMessage.vue';
import SidebarFilter from '@/components/SidebarFilter.vue';
import TableCheckbox from '@/components/TableCheckbox.vue';
import { currentUser } from '@/services/authService';
import { getGeneric, submitDataGeneric } from '@/services/dataService';
import { useMessagesStore } from '@/stores/messages';

export default {
  name: 'AssignmentManagement',
  components: {
    TableCheckbox,
    OverlayMessage,
    SidebarFilter,
  },
  data() {
    return {
      currentUser,
      sections: [],
      units: [],
      curators_options: [],
      fields: [
        { label: 'Collection Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        { label: 'Section', key: 'section_name' },
        { label: 'Responsible Curator', key: 'responsible_curator_id' },
        { label: 'Assigned Editors', key: 'assigned_editors' },
      ],
      filtered_units: [],
    };
  },
  setup() {
    const store = useMessagesStore();
    return { store };
  },
  mounted() {
    this.fetchAllCurators();
    this.fetchAllUnits();
  },
  methods: {
    async fetchAllCurators() {
      this.curators_options = await getGeneric(`all-curators`);
    },
    async fetchAllUnits() {
      const response = await getGeneric(`units-assigned`);
      this.units = response.map((unit) => ({
        ...unit,
        assigned_editors: JSON.parse(unit.assigned_editors || '[]'),
      }));
    },
    async handleResponibleChange(unit, user_id) {
      const response = await submitDataGeneric('submit-field', {
        collection_unit_id: unit.collection_unit_id,
        field_name: 'responsible_curator_id',
        new_value: user_id,
      });
      this.store.handleChangeResponse(response);
      if (response.success && !unit.assigned_editors.includes(user_id)) {
        this.handleEditorsChange(unit, unit.assigned_editors, true);
      }
    },
    async handleEditorsChange(unit, user_ids, submit = false) {
      if (!user_ids.includes(unit.responsible_curator_id)) {
        user_ids.push(unit.responsible_curator_id);
      }
      if (submit) {
        const response = await submitDataGeneric('submit-unit-assigned', {
          unit_id: unit.collection_unit_id,
          assigned_users: user_ids,
        });
        this.store.handleChangeResponse(response);
      }
    },
    handleFilteredUnits(filtered_units) {
      // Only reset pagination if actual filter logic triggered
      if (!this._internalChange) {
        this.filtered_units = JSON.parse(JSON.stringify(filtered_units));
        if (filtered_units.length > 0) {
          this.$refs.unitsTable.resetPage();
        }
      }
    },
  },
};
</script>

<style>
.filters-row {
  display: flex;
  gap: 3rem;
  align-items: center;
  margin-bottom: 20px;
}
.unit-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-evenly;
}
.unit-col {
  width: 18rem;
  text-align: left;
  justify-self: center;
}

.table-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  width: 100%;
}
</style>
