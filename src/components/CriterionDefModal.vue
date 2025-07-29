<template>
  <zoa-modal class="modal-btn criterion-modal" kind="info">
    <template v-slot:button>
      <i class="bi bi-info-circle help-icon"></i>
    </template>
    <template v-slot:header>
      Definition - {{ crit.criterion_code }}: {{ crit.criterion_name }}
    </template>
    <div class="flex flex-col gap-4 criterion-definitions-content">
      <div v-if="unit.ranks_json && unit.ranks_json.length > 0">
        <!-- Criteria name -->
        <div class="desc-title">
          <div class="bold-header">Criterion Definition:</div>
          {{ crit.definition }}
        </div>
        <!-- All Ranks for this Criteria -->
        <div
          v-for="ranks in unit.ranks_json.filter(
            (rank) => rank.criterion_id == crit.criterion_id,
          )"
          :key="ranks.rank_id"
        >
          <div class="desc-title">
            <div class="bold-header">Rank {{ ranks.rank_value }}:</div>
            {{ ranks.definition }}
          </div>
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

<style>
/* Zoe model */
.modal-btn {
  margin: auto;
  z-index: 10;
}

.help-icon {
  font-size: 1.2rem;
}

.criterion-modal {
  width: 80vw !important;
}

.indent {
  margin: 1rem;
}

.desc-title {
  margin-bottom: 0.5rem;
}

.bold-header {
  font-weight: bold;
}

.criterion-definitions-content {
  max-height: 75vh;
  overflow: auto;
}
</style>
