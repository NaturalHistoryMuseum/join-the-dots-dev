<template>
  <zoa-input
    :zoa-type="multi ? 'multiselect' : 'dropdown'"
    :label="label"
    label-position="above"
    :help="help"
    @change="(value) => onChangeFunc && onChangeFunc(value)"
    :options="{ options, itemName: 'value', itemNamePlural: 'data', enableSearch: true }"
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
  },
}
</script>
