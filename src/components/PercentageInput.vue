<template>
  <zoa-input
    :class="computedClass"
    zoa-type="number"
    :label="label"
    v-model="percentageValue"
    :config="{ placeholder: 0, min: 0, max: 100, step: 0.001 }"
    @change="handleChange"
  />
</template>

<script>
export default {
  name: 'PercentageInput',
  props: {
    modelValue: Number,
    label: String,
    error: Array,
    submit: Function,
    rank: Object,
    ranks: Array,
    criterion_id: Number,
  },
  data() {
    return {
      // error: false,
    }
  },
  emits: ['update:modelValue'],
  computed: {
    percentageValue: {
      get() {
        return parseFloat(((this.modelValue ?? 0) * 100).toFixed(3))
      },
      set(val) {
        const rounded = parseFloat(val.toFixed(3))
        this.$emit('update:modelValue', rounded / 100)
      },
    },
    computedClass() {
      if (!this.error.length) return ''
      const type = this.error[0].type
      return {
        'has-error': type == 'error',
        'has-warning': type == 'warning',
      }
    },
  },
  methods: {
    handleChange() {
      this.submit(this.ranks, this.criterion_id)
    },
  },
}
</script>

<style>
.has-error .zoa__number__input {
  border: 1px solid red !important;
  border-radius: 10px;
}

.has-warning .zoa__number__input {
  border: 1px solid #ffe600 !important;
  border-radius: 10px;
}
</style>
