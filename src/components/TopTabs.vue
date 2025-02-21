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
      <!-- {{ key }} : {{ field }} -->
      <div>
        <zoa-input zoa-type="textbox" :label="fieldNameCalc(key)" v-model="filteredFields[key]" />
      </div>
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
        { id: 3, label: 'Storage' },
      ],
      unitTabMapping: [
        {
          tab_id: 0,
          fields: ['unit_name', 'public_unit_name', 'unit_active', 'responsible_curator'],
        },
        { tab_id: 1, fields: ['section_id', 'section_name', 'division_name', 'department_name'] },
        {
          tab_id: 2,
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
  flex-direction: row;
  width: 100%;
  border-bottom: 3px solid #f2bab0;
  overflow: auto;
}
/* .tab-container ::after {
  position: absolute;
  bottom: -1rem;
  left: 0;
  right: 0;
  height: 6px;
  background-color: red;
  opacity: 0;
} */

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
}

.content {
  margin: 1rem;
}

.field {
  padding: 5px;
}
</style>
