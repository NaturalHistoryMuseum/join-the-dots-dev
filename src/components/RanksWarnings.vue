<template>
  <!-- Loop through messages and display with correct type -->
  <div class="warnings">
    <div v-for="error in checkErrors(criterion_id)" :key="error.message">
      <SmallMessages :message_text="error.message" :message_type="error.type" />
    </div>
  </div>
  <!-- Display save message if it has been saved -->
  <SmallMessages
    v-if="checkEdited(editedRanks[criterion_id]) && checkErrors(criterion_id).length == 0"
    message_text="Change Saved"
    message_type="success"
  />
</template>

<script>
import SmallMessages from './SmallMessages.vue'

export default {
  name: 'RanksWarnings',
  props: {
    criterion_id: Object,
    editedRanks: Object,
    ranks: Array,
    checkEdited: Function,
    checkErrors: Function,
  },
  components: {
    SmallMessages,
  },
  methods: {},
}
</script>

<style></style>
