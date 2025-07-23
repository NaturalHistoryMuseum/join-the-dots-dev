<template>
  <zoa-modal class="modal-btn">
    <template v-slot:button>
      <i class="bi bi-info-circle help-icon"></i>
    </template>
    <template v-slot:header> Definitions </template>
    <div class="flex flex-col gap-4">
      <div>
        <!-- Criteria name -->
        <p class="desc-title">{{ crit.criterion_name }}:</p>
        <p>{{ crit.definition }}</p>
        <!-- All Ranks for this Criteria -->
        <div
          v-for="ranks in unit.ranks_json.filter(
            (rank) => rank.criterion_id == crit.criterion_id,
          )"
          :key="ranks.rank_id"
        >
          <p class="desc-title">Rank {{ ranks.rank_value }}:</p>
          <p>{{ ranks.definition }}</p>
        </div>
      </div>
    </div>
  </zoa-modal>
</template>

<script>
export default {
  props: {
    crit: Object,
    unit: Object,
  },
};
</script>

<style scoped>
/* Zoe model */
.modal-btn {
  margin: auto;
  z-index: 10;
}

.help-icon {
  font-size: 1.2rem;
}
</style>
