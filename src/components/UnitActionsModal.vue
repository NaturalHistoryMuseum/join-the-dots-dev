<template>
  <zoa-modal class="modal-btn">
    <template v-slot:button>{{ action.button_name }}</template>
    <template v-slot:header> {{ actions.header }} </template>
    <div class="flex flex-col gap-4">
      <div v-if="action.id == 1">Delete the following units:</div>
      <div>
        {{ selected_unit_ids }}
      </div>
    </div>
  </zoa-modal>
</template>

<script>
export default {
  props: {
    selected_unit_ids: Array,
    action: Object,
  },
  methods: {
    handleSave() {
      this.submit(this.ranks, this.criterion_id);
    },
  },
};
</script>

<style scoped>
/* Zoe model */
.modal-btn {
  margin: auto;
  z-index: 10;
}
</style>
