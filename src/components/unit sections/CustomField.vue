<template>
  <div
    v-if="field && isValidFieldType(field.field_type)"
    :class="
      this.field.field_type === 'dropdown-search' && field.dependant_fields
        ? 'dd-container'
        : ''
    "
  >
    <div class="field-container">
      <div v-if="field.required" class="required-tag">*</div>

      <zoa-input
        zoa-type="empty"
        :label="field.label"
        class="comments-title"
        :help="field.help_text"
        help-position="right"
        v-if="!allow_edit"
      />
      <p v-if="!allow_edit" class="view-field">
        {{ displayValue }}
      </p>
      <zoa-input
        v-if="allow_edit && field.field_type === 'checkbox'"
        zoa-type="empty"
        :label="field.label"
        class="comments-title"
      />
      <zoa-input
        v-if="allow_edit"
        :zoa-type="field.field_type"
        :label="
          field.field_type === 'checkbox'
            ? value != null
              ? value.charAt(0).toUpperCase() + value.slice(1)
              : 'No'
            : field.label
        "
        :help="field.help_text"
        help-position="right"
        :label-position="field.field_type === 'checkbox' ? 'right' : 'above'"
        :config="field_config || {}"
        v-model="local_value"
      />
    </div>
    <div v-if="field.dependant_fields" class="row dep-fields-container">
      <div
        v-for="dep_field in field.dependant_fields"
        :key="dep_field.field_name"
        class="col-md-5 dep-field"
      >
        <zoa-input
          zoa-type="empty"
          :label="dep_field.label"
          class="comments-title"
          :help="dep_field.help_text"
        />
        <p class="view-field">
          {{
            current_option ? current_option[dep_field.field_name] || '-' : '-'
          }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';

export default {
  name: 'CustomField',
  props: {
    field: Object,
    value: [String, Number, Boolean],
    allow_edit: Boolean,
    errors: Array,
  },
  data() {
    return {
      // local_value: null,
      dropdown_options: [],
      current_option: {
        value: null,
        label: null,
      },
    };
  },
  mounted() {
    if (
      this.field.field_type === 'dropdown-search' &&
      this.field.options_source
    ) {
      this.fetchDropdownOptions();
    }
  },
  computed: {
    field_config() {
      switch (this.field.field_type) {
        case 'textbox':
          return { placeholder: 'Enter text here' };
        case 'number':
          return { placeholder: 'Enter a number' };
        case 'checkbox':
          return { checkValue: this.value === 'yes' };
        case 'dropdown-search':
          return {
            options:
              Array.isArray(this.dropdown_options) &&
              this.dropdown_options.length
                ? this.dropdown_options
                : ['Option 1', 'Option 2'],
            enableSearch: true,
            placeholder: 'Select an option',
          };
        default:
          return {};
      }
    },
    errorClass() {
      return this.errors?.find((e) => e.field === this.field.field_name)
        ? 'error-field'
        : '';
    },
    displayValue() {
      if (this.field.field_type === 'checkbox') {
        return this.value === 'yes' ? 'Yes' : 'No';
      } else if (this.field.field_type === 'dropdown-search') {
        return this.current_option.label
          ? this.current_option.label
          : this.allow_edit
            ? ''
            : '-';
      }
      return this.value ? this.value : this.allow_edit ? '' : '-';
    },
    local_value: {
      get() {
        // Reconfigure value for checkbox
        if (this.field.field_type === 'checkbox') {
          return this.value === 'yes';
        }
        return this.value && this.value !== undefined
          ? this.value.toString()
          : '';
      },
      set(val) {
        let new_val = val;
        // Reconfigure value for checkbox
        if (this.field.field_type === 'checkbox') {
          new_val = val ? 'yes' : 'no';
        }
        // Inform parent
        this.$emit('dataChange', this.field.field_name, new_val);
        this.$emit('updateValue', new_val);
        // Update dependent field binding
        this.setCurrentOption(new_val);
      },
    },
  },
  methods: {
    emitChange() {
      this.$emit('change', this.field.field_name, this.value);
    },
    fetchDropdownOptions() {
      getGeneric(this.field.options_source).then((response) => {
        this.dropdown_options =
          response.map((item) => ({
            ...item,
            value: item.value.toString(),
            label: item.label.toString(),
          })) || [];
        this.setCurrentOption();
      });
    },
    setCurrentOption(new_val) {
      const current_val = new_val || this.local_value;
      if (current_val == null) {
        this.current_option = {
          value: null,
          label: null,
        };
      } else {
        this.current_option = this.dropdown_options.find(
          (option) => option.value == current_val,
        );
      }
    },
    isValidFieldType(type) {
      const validTypes = [
        'textbox',
        'number',
        'dropdown-search',
        'checkbox',
        'textarea',
        'empty',
      ]; // Add all allowed types here
      return validTypes.includes(type);
    },
    handleChange() {
      if (this.field.field_type === 'dropdown-search') {
        this.setCurrentOption();
      }
    },
  },
  // watch: {
  //   // Watch for prop changes and update localValue accordingly
  //   value(new_val) {
  //     this.local_value = new_val;
  //   },
  // },
};
</script>

<style>
.field-container {
  width: 25vw;
}
.dd-container {
  width: 90vw;
  display: flex;
  flex-wrap: wrap;
}
.dep-field {
  margin: 1rem;
  margin-bottom: 2rem;
}

.dep-fields-container {
  width: 66%;
}
</style>
