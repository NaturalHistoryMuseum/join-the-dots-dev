<template>
  <div class="warnings">
    <div v-if="message_type == 'success'" class="msg save-msg">
      <i class="bi bi-check-circle-fill save-icon"></i>
      {{ message_text }}
    </div>
    <div v-if="message_type == 'error'" class="msg error-msg">
      <i class="bi-x-circle-fill error-icon"></i>
      {{ message_text }}
    </div>
    <div v-if="message_type == 'warning'" class="msg warning-msg">
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
};
</script>

<style>
.warnings {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.msg {
  font-weight: bold;
  margin-right: 1rem;
  border-radius: 10px;
  padding: 0.25rem 1rem;
  cursor: auto;
}

.error-msg {
  border: 1px solid #fa3608;
  background-color: #feeae6;
}

.warning-msg {
  border: 1px solid #ffe600;
  background-color: #fefce5;
}

.save-msg {
  border: 1px solid #30ff2e;
  background-color: #e5fee5;
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
