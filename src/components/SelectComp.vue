<template>
  <zoa-input
    :zoa-type="multi ? 'multiselect' : 'dropdown'"
    :label="label"
    label-position="above"
    :help="help"
    @change="(value) => onChangeFunc && onChangeFunc(value) & $emit('input', $event)"
    :options="{ options, itemName: 'value', itemNamePlural: 'data', enableSearch: true }"
    v-model="localValue"
  />
</template>

<script>
export default {
  props: {
    multi: Boolean,
    options: Array,
    label: String,
    help: String,
    onChangeFunc: Function,
    value: String,
  },
  data() {
    return {
      localValue: this.value, // Create a local copy for v-model
    }
  },
  watch: {
    // Watch for prop changes and update localValue accordingly
    value(newVal) {
      this.localValue = newVal
    },
    // Watch for localValue changes and emit updates to parent
    localValue(newVal) {
      this.$emit('input', newVal) // Emit update to parent
    },
  },
}
</script>
