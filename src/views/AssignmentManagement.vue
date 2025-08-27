<template>
  <div class="main-header">
    <h1>Manage Units Assignment</h1>
    <p>Manage who can edit units under you.</p>
  </div>
  <div class="content">
    <div class="filters-row">
      <zoa-input
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
      <div
        v-for="unit in units"
        :key="unit.collection_unit_id"
        class="unit-row"
      >
        <div class="unit-col">
          {{ unit.unit_name }}
          {{ unit.section_id }}
        </div>
        <zoa-input
          class="unit-col"
          zoa-type="dropdown"
          label="Responsible Curator"
          :config="{ options: curators_options }"
        />
        <zoa-input
          class="unit-col"
          zoa-type="multiselect"
          label="Assigned Editors"
          :config="{ options: curators_options }"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';

export default {
  name: 'AssignmentManagement',
  data() {
    return {
      assign_by_options: ['units', 'users'],
      assign_by: 'units',
      sections: [],
      units: [],
      curators_options: [],
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
      this.units = await getGeneric(`units-assigned`);
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
</style>
