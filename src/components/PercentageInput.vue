<template>
  <zoa-input
    zoa-type="number"
    :label="label"
    v-model="percentageValue"
    :step="0.1"
    :min="0"
    :max="100"
  />
</template>

<script>
export default {
  name: 'PercentageInput',
  props: {
    modelValue: Number,
    label: String,
  },
  emits: ['update:modelValue'],
  computed: {
    percentageValue: {
      get() {
        return (this.modelValue ?? 0) * 100
      },
      set(val) {
        this.$emit('update:modelValue', val / 100)
      },
    },
  },
}
</script>
