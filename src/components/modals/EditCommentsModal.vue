<template>
  <zoa-modal class="modal-btn">
    <template v-slot:button>Edit Comments</template>
    <template v-slot:header> Edit Comments - {{ criterion_name }}</template>
    <div class="flex flex-col gap-4">
      <div>
        <div v-for="rank in ranks" :key="rank.rank_id">
          <!-- Show the comment for each rank -->
          <zoa-input
            zoa-type="empty"
            :label="`Rank ${rank.rank_value} Comment - (Score: ${rank.percentage * 100}%)`"
            class="comments-title"
          />
          <textarea
            class="text-area"
            rows="2"
            v-model="rank.comment"
            @change="handleSave"
          ></textarea>
        </div>
        <!-- <div class="">
          <zoa-button label="Save" @click="handleSave" />
        </div> -->
      </div>
    </div>
  </zoa-modal>
</template>

<script>
export default {
  name: 'EditCommentsModal',
  props: {
    criterion_id: Number,
    criterion_name: String,
    ranks: Array,
    submit: Function,
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
