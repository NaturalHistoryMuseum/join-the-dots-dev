<template>
  <zoa-modal class="modal-btn">
    <template v-slot:button>Edit Comments</template>
    <template v-slot:header> Edit Comments </template>
    <div class="flex flex-col gap-4">
      <div>
        <div
          v-for="rank in JSON.parse(unit.ranks_json).filter(
            (rank) => rank.criterion_id == crit.criterion_id,
          )"
          :key="rank.rank_id"
        >
          <!-- <p class="desc-title">Rank {{ ranks.rank_value }}:</p>
          <p>{{ ranks.comment }}</p> -->
          <zoa-input
            zoa-type="empty"
            :label="`Rank ${rank.rank_value} Comment`"
            class="comments-title"
          />
          <textarea class="text-area" rows="2" v-model="rank.comment"></textarea>
        </div>
        <div class="">
          <zoa-button label="Save" />
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
}
</script>

<style scoped>
/* Zoe model */
.modal-btn {
  margin: auto;
  z-index: 10;
}
</style>
