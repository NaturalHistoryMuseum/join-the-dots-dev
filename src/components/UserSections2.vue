<template>
  <div>
    <!-- {{ departments.department_name }}
    {{ select_depts }} -->
  </div>
  <div class="row">
    <div class="col-md-4">
      <!-- <div v-if="select_depts.length > 0"> -->
      <SelectComp :options="select_depts" label="Department" :multi="true" />
      <!-- </div> -->
    </div>
    <div class="col-md-4">
      <SelectComp :options="select_divis" label="Division" :multi="true" />
    </div>
    <div class="col-md-4">
      <SelectComp
        :options="select_sects"
        label="Section"
        help="this is help"
        :multi="true"
        :onChangeFunc="handleSectionChange"
      />
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService'
import SelectComp from './SelectComp.vue'

export default {
  components: {
    SelectComp,
  },
  data() {
    return {
      sections: [],
      divisions: [],
      departments: [],
      select_depts: [],
      select_divis: [],
      select_sects: [],
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
      this.select_depts = this.departments.map((dept) => ({
        value: dept.department_name,
      }))
      this.select_divis = this.divisions.map((divis) => ({ value: divis.division_name }))
      this.select_sects = this.sections.map((sect) => ({ value: sect.section_name }))

      console.log(this.select_depts)
    },
    handleSectionChange(value) {
      console.log('section change')
      console.log(value)
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
