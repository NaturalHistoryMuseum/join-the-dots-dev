<template>
  <div class="col-md-4 field">
    <div class="required-tag">*</div>
    <zoa-input
      :class="
        errors.find((err) => err.field == 'section_id') ? 'error-field' : ''
      "
      zoa-type="dropdown"
      label="Section Name"
      :config="{ options: section_options }"
      v-model="unit_value.section_id"
      @change="
        () => {
          setCurrentSection();
          handleFieldChange('section_id', unit_value.section_id);
        }
      "
    />
  </div>
  <div class="col-md-4 field">
    <zoa-input zoa-type="empty" label="Division Name" class="comments-title" />
    <p class="view-field">{{ current_section.division_name }}</p>
  </div>
  <div class="col-md-4 field">
    <zoa-input
      zoa-type="empty"
      label="Department Name"
      class="comments-title"
    />
    <p class="view-field">{{ current_section.department_name }}</p>
  </div>
</template>

<script>
export default {
  name: 'SectionTab',
  props: {
    unit: Object,
    section_options: Array,
    current_section: Object,
    setCurrentSection: Function,
    handleFieldChange: Function,
    errors: Array,
  },
  data() {
    return {};
  },
  computed: {
    unit_value: {
      get() {
        return this.unit;
      },
      set(value) {
        this.$emit('updateUnit', value);
      },
    },
  },
  methods: {},
};
</script>

<style></style>
