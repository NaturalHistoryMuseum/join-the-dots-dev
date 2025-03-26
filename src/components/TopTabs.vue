<script setup>
import fieldNameCalc from '@/utils/utils'
</script>

<template>
  <div class="tab-container">
    <button
      v-for="(tab, index) in tabs"
      :key="index"
      @click="activeTab = index"
      :class="['tab', activeTab === index ? 'active' : '']"
      :style="{
        backgroundColor: activeTab === index ? '#f2bab0' : '#e0e0e0',
      }"
    >
      <span class="tab-title">{{ tab.label }}</span>
    </button>
  </div>

  <div class="content row">
    <div v-for="(field, key) in filteredFields" :key="key" class="col-md-4 field">
      <zoa-input zoa-type="textbox" :label="fieldNameCalc(key)" v-model="filteredFields[key]" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    unit: Array,
  },
  data() {
    return {
      tabs: [
        { id: 1, label: 'Unit Details' },
        { id: 2, label: 'Section' },
        { id: 3, label: 'Properties' },
        { id: 4, label: 'Storage' },
        { id: 5, label: 'Scores' },
        { id: 6, label: 'Comments' },
      ],
      unitTabMapping: [
        {
          tab_id: 0,
          fields: [
            'collection_unit_id',
            'unit_name',
            'public_unit_name',
            'item_type',
            'description',
            //only if lib and arch
            'function_name',
            'unit_active',
            'responsible_curator',
            'archives_fond_ref',
            'bibliographic_level',
            'count_curatorial_units_flag',
            'es_recent_specimen_flag',
            'items_unestimatable_flag',
            'named_collection',
            'preservation_method',
            'publish_flag',
            'sort_order',
            'type_collection_flag',
            'typical_item_count',
            'typical_item_count_range',
          ],
        },
        { tab_id: 1, fields: ['section_id', 'section_name', 'division_name', 'department_name'] },
        {
          tab_id: 2,
          fields: [
            'informal_taxon',
            'geographic_origin_id',
            'geographic_origin_name',
            'region_type',
            'geological_time_period_from_id',
            'from_period',
            'geological_time_period_to_id',
            'to_period',
            'ls_external_ref_name',
            'ls_taxon_name',
            'ls_taxon_rank',
            'pal_external_ref_name',
            'pal_taxon_name',
            'pal_taxon_rank',
          ],
        },
        {
          tab_id: 3,
          fields: [
            'container_name',
            'temperature',
            'relative_humidity',
            'room_name',
            'room_code',
            'floor_name',
            'building_name',
            'site_name',
          ],
        },
        {
          tab_id: 4,
          fields: [],
        },
        {
          tab_id: 5,
          fields: ['unit_comment', 'date_comment_added'],
        },
      ],
      activeTab: 0,
    }
  },
  computed: {
    filteredFields() {
      console.log(this.unitTabMapping.filter((id) => this.activeTab == id.tab_id)[0]['fields'])
      // Find the tab mapping for the active tab
      const mapping = this.unitTabMapping.find((item) => item.tab_id === this.activeTab)
      console.log('mapping - ', mapping.fields)

      return mapping && this.unit
        ? Object.fromEntries(
            Object.entries(this.unit).filter(([key]) => mapping.fields.includes(key)),
          )
        : {}
    },
  },
}
</script>

<style scoped>
.tab-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  border-bottom: 3px solid #f2bab0;
  overflow-x: auto;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
  scrollbar-width: none; /* Hide scrollbar on Firefox */
}

.tab-container::-webkit-scrollbar {
  display: none; /* Hide scrollbar on Chrome, Safari */
}

.tab {
  padding: 0.5rem 2rem;
  border: none;
  cursor: pointer;
  color: black;
  font-weight: 600;
  text-align: center;
  border-radius: 20px 20px 0px 0px;
  margin-right: 5px;
  transition: all 0.3s;
  flex-shrink: 0; /* Prevent tabs from shrinking */
}

.content {
  margin: 1rem;
}

.field {
  padding: 5px;
}

@media (max-width: 768px) {
  .tab {
    padding: 0.4rem 1rem;
  }
}

@media (max-width: 480px) {
}
</style>
