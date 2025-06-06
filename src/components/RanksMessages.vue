<template>
  <div class="warnings" v-for="error in checkErrors(criterion_id)" :key="error.message">
    <div :class="error.type == 'error' ? 'error-msg' : 'warning-msg'">
      <i
        class="bi"
        :class="
          error.type == 'error'
            ? 'bi-x-circle-fill error-icon'
            : 'bi-exclamation-circle-fill warning-icon'
        "
      ></i>
      {{ error.message }}
    </div>
  </div>
  <div
    class="warnings"
    v-if="checkEdited(editedRanks[criterion_id]) && checkErrors(criterion_id).length == 0"
  >
    <div class="save-msg">
      <i class="bi bi-check-circle-fill save-icon"></i>
      Change Saved
    </div>
  </div>
</template>

<script>
export default {
  name: 'RanksMessages',
  props: {
    criterion_id: Object,
    editedRanks: Object,
    ranks: Array,
    checkEdited: Function,
    checkErrors: Function,
  },
  methods: {},
}
</script>

<style>
.warnings {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.error-msg {
  /* color: red; */
  font-weight: bold;
  margin-right: 1rem;
  border: 1px solid red;
  border-radius: 10px;
  background-color: #feeae6;
  padding: 0.25rem 1rem;
}

.warning-msg {
  /* color: darkorange; */
  font-weight: bold;
  margin-right: 1rem;
  border: 1px solid #ffe600;
  border-radius: 10px;
  background-color: #fefce5;
  padding: 0.25rem 1rem;
}

.save-msg {
  font-weight: bold;
  margin-right: 1rem;
  border: 1px solid #30ff2e;
  border-radius: 10px;
  background-color: #e5fee5;
  padding: 0.25rem 1rem;
}

.save-icon {
  color: #30ff2e;
  margin-right: 0.5rem;
}

.error-icon {
  color: red;
  margin-right: 0.5rem;
}

.warning-icon {
  color: #ffe600;
  margin-right: 0.5rem;
}
</style>
