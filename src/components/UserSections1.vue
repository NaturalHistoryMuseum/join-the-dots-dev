<script setup>
import { addSections } from '@/services/userService'
</script>

<template>
  <div>
    {{ selected_depts }}
    {{ selected_divis }}
    {{ selected_sects }}
    {{ currentSections }}
    <zoa-button
      label="Save Sections"
      kind="alt"
      @click="selected_sects.length > 0 ? addSections(selected_sects) : null"
    />
  </div>
  <div class="row">
    <div class="col-md-4">
      <h5>Department</h5>
      <div class="scrollbox">
        <div v-for="dept in departments" :key="dept.department_id">
          <zoa-input
            class="check"
            zoa-type="checkbox"
            :label="dept.department_name"
            label-position="right"
            @change="(event) => selectDept(event, dept.department_id)"
          />
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <h5>Division</h5>
      <div class="scrollbox">
        <div
          v-for="divis in selected_depts.length > 0
            ? divisions.filter((division) => selected_depts.includes(division.department_id))
            : divisions"
          :key="divis.division_id"
          class="scrollbox"
        >
          <zoa-input
            class="check"
            zoa-type="checkbox"
            :label="divis.division_name"
            label-position="right"
            @change="(event) => selectDivis(event, divis.division_id)"
          />
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <h5>Section</h5>
      <div class="scrollbox">
        <div
          v-for="sect in selected_divis.length > 0
            ? sections.filter(
                (section) => selected_divis.includes(section.division_id),
                // selected_depts.includes(section.department_id),
              )
            : sections"
          :key="sect.section_id"
          class="scrollbox"
        >
          {{ selected_sects.includes(sect.section_id) }}
          <zoa-input
            :id="sect.section_id"
            zoa-type="checkbox"
            :label="sect.section_name"
            label-position="right"
            @change="(event) => selectSects(event, sect.section_id)"
            :checked="selected_sects.includes(sect.section_id)"
          />
          <input type="checkbox" :checked="selected_sects.includes(sect.section_id)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService'
import { getSections } from '@/services/userService'

export default {
  data() {
    return {
      sections: [],
      divisions: [],
      departments: [],
      selected_depts: [],
      selected_divis: [],
      selected_sects: [],
      currentSections: [],
    }
  },
  mounted() {
    this.getData()
  },
  methods: {
    async getData() {
      this.departments = await getGeneric('all-departments')
      this.divisions = await getGeneric('all-divisions')
      this.sections = await getGeneric('all-sections')
      this.currentSections = await getSections()
      this.selected_sects = this.currentSections.map((section) => Number(section.section_id))
      console.log(this.selected_sects)
    },
    selectDept(event, id) {
      if (event) {
        this.selected_depts.push(id)
      } else {
        this.selected_depts = this.selected_depts.filter((Id) => Id !== id)
      }
      this.selected_divis = []
      this.selected_sects = []
    },
    selectDivis(event, id) {
      if (event) {
        this.selected_divis.push(id)
      } else {
        this.selected_divis = this.selected_divis.filter((Id) => Id !== id)
      }
      this.selected_sects = []
    },
    selectSects(event, id) {
      if (event) {
        this.selected_sects.push(id)
      } else {
        this.selected_sects = this.selected_sects.filter((Id) => Id !== id)
      }
    },
  },
}
</script>

<style scoped>
.check {
  margin: 1rem;
}

.scrollbox {
  max-height: 20rem;
  overflow-y: auto;
}
</style>
