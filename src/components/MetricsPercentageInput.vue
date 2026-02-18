<template>
  <zoa-input
    zoa-type="number"
    :label="label"
    v-model="percentageValue"
    :config="{ placeholder: 0, min: 0, max: 100, step: 1 }"
    @change="handleChange"
  />
</template>

<script>
export default {
  name: 'MetricsPercentageInput',
  props: {
    modelValue: Number,
    label: String,
    submit: Function,
    collection_unit_metric_definition_id: Number,
  },
  data() {
    return {};
  },
  emits: ['update:modelValue'],
  computed: {
    percentageValue: {
      get() {
        return this.modelValue !== undefined
          ? parseFloat((this.modelValue * 100).toFixed(2))
          : 0;
      },
      set(val) {
        const normalized = Number(val) / 100;
        this.$emit('update:modelValue', parseFloat(normalized.toFixed(5)));
      },
    },
  },
  methods: {
    handleChange() {
      this.submit(this.collection_unit_metric_definition_id);
    },
  },
};
</script>

<style></style>
