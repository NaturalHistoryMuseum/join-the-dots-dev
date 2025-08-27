<template>
  <div class="main-header">
    <h1>Manage Units Assignment</h1>
    <p>Manage who can edit units under you.</p>
  </div>
  <div class="content">
    <div class="filters-row">
      <zoa-input
        v-if="currentUser.role_id > 2"
        zoa-type="dropdown"
        label="Assign by..."
        labelPosition="left"
        :config="{ options: assign_by_options }"
        v-model="assign_by"
      />
      <zoa-input
        v-if="assign_by == 'units'"
        zoa-type="dropdown"
        label="Section Filter"
        labelPosition="left"
        :config="{ options: sections }"
      />
    </div>
    <div v-if="assign_by == 'units'" class="units-assignment">
      <TableCheckbox :units="units" :fields="fields">
        <template #cell(responsible_curator_id)="row">
          <zoa-input
            class="unit-col"
            zoa-type="dropdown"
            label="Responsible Curator"
            v-model="row.item.responsible_curator_id"
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
          />
        </template>
      </TableCheckbox>
    </div>
  </div>
</template>

<script>
import TableCheckbox from '@/components/TableCheckbox.vue';
import { currentUser } from '@/services/authService';
import { getGeneric } from '@/services/dataService';

export default {
  name: 'AssignmentManagement',
  components: {
    TableCheckbox,
  },
  data() {
    return {
      currentUser,
      assign_by_options: ['units', 'users'],
      assign_by: 'units',
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
    };
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
  width: 20rem;
  text-align: left;
}

.table-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  width: 100%;
}
</style>
