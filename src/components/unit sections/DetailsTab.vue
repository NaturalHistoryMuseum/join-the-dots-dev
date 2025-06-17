<template>
  <div class="row">
    <h4 class="subheading">Unit Details</h4>
    <div class="col-md-4 field">
      <zoa-input
        zoa-type="textbox"
        label="Unit Name"
        v-model="unit_value.unit_name"
        @change="handleFieldChange('unit_name', unit_value.unit_name)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input
        zoa-type="textbox"
        label="Public Unit Name"
        v-model="unit_value.public_unit_name"
        @change="handleFieldChange('public_unit_name', unit_value.public_unit_name)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input
        zoa-type="textbox"
        label="Named Collection"
        v-model="unit_value.named_collection"
        @change="handleFieldChange('named_collection', unit_value.named_collection)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input
        zoa-type="textbox"
        label="Archives Fond Ref"
        v-model="unit_value.archives_fond_ref"
        @change="handleFieldChange('archives_fond_ref', unit_value.archives_fond_ref)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input
        zoa-type="number"
        label="Sort Order"
        v-model="unit_value.sort_order"
        @change="handleFieldChange('sort_order', unit_value.sort_order)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Unit Active?" class="comments-title" />
      <zoa-input
        zoa-type="checkbox"
        :label="
          unit_value.unit_active != null
            ? unit_value.unit_active.charAt(0).toUpperCase() + unit_value.unit_active.slice(1)
            : 'No'
        "
        label-position="right"
        v-model="unitIsActive"
        @change="handleFieldChange('unit_active', unit_value.unit_active)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Publish Unit?" class="comments-title" />
      <zoa-input
        zoa-type="checkbox"
        :label="
          unit_value.publish_flag != null
            ? unit_value.publish_flag.charAt(0).toUpperCase() + unit_value.publish_flag.slice(1)
            : 'No'
        "
        label-position="right"
        v-model="publishFlag"
        @change="handleFieldChange('publish_flag', unit_value.publish_flag)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Type Collection?" class="comments-title" />
      <zoa-input
        zoa-type="checkbox"
        :label="
          unit_value.type_collection_flag != null
            ? unit_value.type_collection_flag.charAt(0).toUpperCase() +
              unit_value.type_collection_flag.slice(1)
            : 'No'
        "
        label-position="right"
        v-model="typeCollectionFlag"
        @change="handleFieldChange('type_collection_flag', unit_value.type_collection_flag)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="ES Recent Specimen?" class="comments-title" />
      <zoa-input
        zoa-type="checkbox"
        :label="
          unit_value.es_recent_specimen_flag != null
            ? unit_value.es_recent_specimen_flag.charAt(0).toUpperCase() +
              unit_value.es_recent_specimen_flag.slice(1)
            : 'No'
        "
        label-position="right"
        v-model="recentSpecimenFlag"
        @change="handleFieldChange('es_recent_specimen_flag', unit_value.es_recent_specimen_flag)"
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Count Curatorial Units?" class="comments-title" />
      <zoa-input
        zoa-type="checkbox"
        :label="
          unit_value.count_curatorial_units_flag != null
            ? unit_value.count_curatorial_units_flag.charAt(0).toUpperCase() +
              unit_value.count_curatorial_units_flag.slice(1)
            : 'No'
        "
        label-position="right"
        v-model="countCuratorialUnitsFlag"
        @change="
          handleFieldChange('count_curatorial_units_flag', unit_value.count_curatorial_units_flag)
        "
      />
    </div>
  </div>

  <div class="row">
    <h4 class="subheading">Responsible Curator</h4>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Curator Name" class="comments-title" />
      <p class="view-field">{{ unit_value.responsible_curator }}</p>
    </div>
  </div>
  <div class="row">
    <h4 class="subheading">Curtorial Unit Definition</h4>
    <div class="col-md-4 field">
      <zoa-input
        zoa-type="dropdown"
        label="Curatorial Unit Definition"
        :config="{ options: curatorial_def_options }"
        v-model="unit_value.curatorial_unit_definition_id"
        @change="
          () => {
            setCurrentCuratorialDef()
            handleFieldChange(
              'curatorial_unit_definition_id',
              unit_value.curatorial_unit_definition_id,
            )
          }
        "
      />
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Item Type" class="comments-title" />
      <p class="view-field">{{ current_curatorial_def.item_type }}</p>
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Bibliographic Level" class="comments-title" />
      <p class="view-field">{{ current_curatorial_def.bibliographic_level }}</p>
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Preservation Method" class="comments-title" />
      <p class="view-field">{{ current_curatorial_def.preservation_method }}</p>
    </div>
    <div class="col-md-4 field">
      <zoa-input zoa-type="empty" label="Items Unestimatable Flag" class="comments-title" />
      <p class="view-field">{{ current_curatorial_def.items_unestimatable_flag }}</p>
    </div>
  </div>
  <div v-if="department_id == 2" class="row">
    <h4 class="subheading">Library and Archives Function</h4>
    <div class="col-md-4 field">
      <zoa-input
        zoa-type="dropdown"
        label="Library and Archives Function"
        :config="{ options: lib_function_options }"
        v-model="unit_value.library_and_archives_function_id"
        @change="
          () => {
            setCurrentLibFunction()
            handleFieldChange(
              'library_and_archives_function_id',
              unit_value.library_and_archives_function_id,
            )
          }
        "
      />
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService'

export default {
  name: 'DetailsTab',
  props: {
    unit: Object,
    department_id: Number,
    handleFieldChange: Function,
  },
  data() {
    return {
      curatorial_def_options: [],
      current_curatorial_def: {},
      lib_function_options: [],
      current_lib_function: {},
    }
  },
  computed: {
    unit_value: {
      get() {
        return this.unit
      },
      set(value) {
        this.$emit('updateUnit', value)
      },
    },
    unitIsActive: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit?.unit_active === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit) {
          this.unit_value.unit_active = val ? 'yes' : 'no'
        }
      },
    },
    publishFlag: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit_value?.publish_flag === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit) {
          this.unit_value.publish_flag = val ? 'yes' : 'no'
        }
      },
    },
    typeCollectionFlag: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit_value?.type_collection_flag === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit_value) {
          this.unit_value.type_collection_flag = val ? 'yes' : 'no'
        }
      },
    },
    recentSpecimenFlag: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit_value?.es_recent_specimen_flag === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit_value) {
          this.unit_value.es_recent_specimen_flag = val ? 'yes' : 'no'
        }
      },
    },
    countCuratorialUnitsFlag: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit_value?.count_curatorial_units_flag === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit_value) {
          this.unit_value.count_curatorial_units_flag = val ? 'yes' : 'no'
        }
      },
    },
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      getGeneric(`all-curtorial-definition`).then((response) => {
        this.curatorial_def_options = response.map((curatorial_def) => ({
          ...curatorial_def,
          value: curatorial_def.curatorial_unit_definition_id,
          label: curatorial_def.description,
        }))
        this.setCurrentCuratorialDef()
      })
      getGeneric(`all-lib-function`).then((response) => {
        this.lib_function_options = response.map((lib_function) => ({
          ...lib_function,
          value: lib_function.library_and_archives_function_id,
          label: lib_function.function_name,
        }))
        this.setCurrentLibFunction()
      })
    },
    setCurrentCuratorialDef() {
      if (this.unit.curatorial_unit_definition_id == null) {
        this.current_curatorial_def = {
          value: null,
          curatorial_definition_name: null,
        }
      } else {
        this.current_curatorial_def = this.curatorial_def_options.filter(
          (curatorial_def) =>
            curatorial_def.curatorial_unit_definition_id == this.unit.curatorial_unit_definition_id,
        )[0]
      }
    },
    setCurrentLibFunction() {
      if (this.unit.library_and_archives_function_id == null) {
        this.current_lib_function = {
          value: null,
          lib_function_name: null,
        }
      } else {
        this.current_lib_function = this.lib_function_options.filter(
          (lib_function) =>
            lib_function.library_and_archives_function_id ==
            this.unit.library_and_archives_function_id,
        )[0]
      }
    },
  },
}
</script>

<style></style>
