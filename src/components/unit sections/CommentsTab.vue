<template>
  <div class="col-md-6 field">
    <zoa-input zoa-type="empty" label="Unit Comments" class="comments-title" />
    <textarea
      class="text-area"
      rows="7"
      v-model="unit_value.unit_comment"
    ></textarea>
  </div>
  <div class="col-md-4 field">
    <zoa-input
      zoa-type="empty"
      label="Date Comment Added"
      class="comments-title"
    />
    <p class="view-field">{{ formatDate(unit_value.date_comment_added) }}</p>
  </div>
</template>

<script>
export default {
  name: 'CommentsTab',
  props: {
    unit: Object,
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
  methods: {
    formatDate(date) {
      return new Date(date).toISOString().split('T')[0];
    },
  },
};
</script>

<style></style>
