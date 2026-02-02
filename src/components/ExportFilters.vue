<template>
  <!-- <h1 class="h1-style">Export</h1> -->
  <p>
    Please use the filters below to select the data you want to export and the
    type of file you want to download.
  </p>
  <hr />
  <h2 class="h4-style">Data Filters</h2>
  <div class="export-sections">
    <zoa-input
      :zoa-type="'multiselect'"
      class="export-filter"
      label="Division"
      label-position="above"
      :config="{
        options: divisions,
        itemName: 'division',
        itemNamePlural: 'divisions',
        enableSearch: true,
        itemHeight: 50,
      }"
      v-model="selected_divisions"
    />
    <zoa-input
      :zoa-type="'multiselect'"
      class="export-filter"
      label="Section"
      label-position="above"
      :config="{
        options: sections,
        itemName: 'section',
        itemNamePlural: 'sections',
        enableSearch: true,
        itemHeight: 50,
      }"
      v-model="selected_sections"
    />
    <zoa-input
      :zoa-type="'multiselect'"
      class="export-filter"
      label="Responsible Curator"
      label-position="above"
      :config="{
        options: responsible_curators,
        itemName: 'curator',
        itemNamePlural: 'curators',
        enableSearch: true,
        itemHeight: 50,
      }"
      v-model="selected_curators"
    />
    <zoa-input
      :zoa-type="'multiselect'"
      class="export-filter"
      label="Room Code"
      label-position="above"
      :config="{
        options: rooms,
        itemName: 'rooms',
        itemNamePlural: 'rooms',
        enableSearch: true,
        itemHeight: 50,
      }"
      v-model="selected_rooms"
    />
    <zoa-input
      :zoa-type="'multiselect'"
      class="export-filter"
      label="Curatorial Unit Definition"
      label-position="above"
      :config="{
        options: curatorial_definitions,
        itemName: 'definition',
        itemNamePlural: 'definitions',
        enableSearch: true,
        itemHeight: 50,
      }"
      v-model="selected_curatorial_definitions"
    />
    <zoa-input
      :zoa-type="'multiselect'"
      class="export-filter"
      label="Taxon Name"
      label-position="above"
      :config="{
        options: taxons,
        itemName: 'taxons',
        itemNamePlural: 'taxons',
        enableSearch: true,
        itemHeight: 50,
      }"
      v-model="selected_taxons"
    />
  </div>
  <h2 class="h4-style">Export Options</h2>
  <div class="export-sections">
    <zoa-input
      :zoa-type="'dropdown'"
      class="export-filter"
      label="Data Type"
      label-position="above"
      :config="{
        options: data_types,
        enableSearch: true,
        itemHeight: 50,
      }"
      v-model="selected_data_type"
    />
  </div>
  <div v-if="selected_data_type != 'ltc'" class="export-sections">
    <zoa-input
      zoa-type="checkbox"
      label="Include Scores?"
      label-position="right"
      v-model="include_scores"
    />
    <zoa-input
      zoa-type="checkbox"
      label="Include Metrics?"
      label-position="right"
      v-model="include_metrics"
    />
    <zoa-input
      zoa-type="checkbox"
      label="Include Scores Averages?"
      label-position="right"
      v-model="include_score_averages"
    />
  </div>
  <div v-else class="export-sections">
    <zoa-input
      zoa-type="checkbox"
      label="Include Measures (Scores and Metrics)?"
      label-position="right"
      v-model="include_ltc_measures"
    />
  </div>

  <zoa-button
    v-if="selected_data_type"
    class="export-btn"
    label="Export"
    @click="runExport()"
  />
  <hr />
</template>

<script>
import { downloadCSV, getGeneric } from '@/services/dataService';
import { downloadCustomExport } from '@/services/exportService';
import { useLoadingStore } from '@/stores/loadingStore';

export default {
  name: 'ExportFilters',
  components: {},
  data() {
    return {
      sections: [],
      divisions: [],
      responsible_curators: [],
      rooms: [],
      curatorial_definitions: [],
      taxons: [],
      selected_sections: [],
      selected_divisions: [],
      selected_curators: [],
      selected_rooms: [],
      selected_curatorial_definitions: [],
      selected_taxons: [],
      include_scores: true,
      include_metrics: true,
      include_score_averages: false,
      data_types: [
        { label: 'CSV', value: 'csv' },
        { label: 'JSON', value: 'json' },
        { label: 'Latimer Core JSON', value: 'ltc' },
      ],
      selected_data_type: 'csv',
      include_ltc_measures: false,
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData() {
      this.fetchSections();
      this.fetchDivisions();
      this.fetchResponsibleCurators();
      this.fetchRooms();
      this.fetchCuratorialDefinitions();
      this.fetchTaxons();
    },
    async createExport() {
      const loadingStore = useLoadingStore();
      try {
        loadingStore.startLoading();
        await downloadCSV(this.viewVal);
      } catch (error) {
        console.error('Error downloading CSV:', error);
      } finally {
        loadingStore.stopLoading();
      }
    },
    async runExport() {
      const loadingStore = useLoadingStore();
      try {
        loadingStore.startLoading();
        await downloadCustomExport({
          selected_sections: this.selected_sections,
          selected_divisions: this.selected_divisions,
          selected_curators: this.selected_curators,
          selected_rooms: this.selected_rooms,
          selected_curatorial_definitions: this.selected_curatorial_definitions,
          selected_taxons: this.selected_taxons,
          include_scores: this.include_scores,
          include_metrics: this.include_metrics,
          include_score_averages: this.include_score_averages,
          selected_data_type: this.selected_data_type,
          include_ltc_measures: this.include_ltc_measures,
        });
      } catch (error) {
        console.error('Error downloading custom export:', error);
      } finally {
        loadingStore.stopLoading();
      }
    },
    async fetchSections() {
      const response = await getGeneric('all-sections');
      this.sections = response.map((row) => ({
        ...row,
        value: row.value.toString(),
      }));
    },
    async fetchDivisions() {
      const response = await getGeneric('all-divisions');
      this.divisions = response.map((row) => ({
        ...row,
        value: row.value.toString(),
      }));
    },
    async fetchResponsibleCurators() {
      const response = await getGeneric('all-curators');
      this.responsible_curators = response.map((row) => ({
        ...row,
        value: row.value.toString(),
      }));
    },
    async fetchRooms() {
      const response = await getGeneric('room-data');
      this.rooms = response.map((row) => ({
        ...row,
        value: row.value.toString(),
      }));
    },
    async fetchCuratorialDefinitions() {
      const response = await getGeneric('all-curatorial-definition');
      this.curatorial_definitions = response.map((row) => ({
        ...row,
        value: row.value.toString(),
      }));
    },
    async fetchTaxons() {
      const response = await getGeneric('all-taxon');
      this.taxons = response.map((row) => ({
        ...row,
        value: row.value.toString(),
      }));
    },
  },
};
</script>

<style>
.export-sections {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-content: center;
  justify-content: flex-start;
  align-items: center;
  gap: 1rem;
  margin: 1rem 1rem 1rem 1rem;
}
.export-filter {
  width: 20rem;
}
.export-btn {
  margin-top: 1rem;
}
</style>
