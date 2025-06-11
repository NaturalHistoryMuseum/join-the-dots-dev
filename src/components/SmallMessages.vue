<template>
  <div class="warnings">
    <div v-if="message_type == 'success'" class="save-msg">
      <i class="bi bi-check-circle-fill save-icon"></i>
      {{ message_text }}
    </div>
    <div v-if="message_type == 'error'" class="error-msg">
      <i class="bi-x-circle-fill error-icon"></i>
      {{ message_text }}
    </div>
    <div v-if="message_type == 'warning'" class="warning-msg">
      <i class="bi-exclamation-circle-fill warning-icon"></i>
      {{ message_text }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'SmallMessages',
  props: {
    message_text: String,
    message_type: String,
  },
  methods: {},
}
</script>

<style>
.warnings {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
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
  margin-bottom: 0.5rem;
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
