<template>
  <div class="unit-save-msg-container">
    <transition-group name="fade" tag="div" class="message-stack">
      <div v-for="(message, index) in store.messages" :key="index">
        <SmallMessages
          :message_text="message.message_text"
          :message_type="message.message_type"
          class="unit-save-msg"
        />
      </div>
    </transition-group>
  </div>
</template>

<script>
import { useMessagesStore } from '@/stores/messages';
import SmallMessages from './SmallMessages.vue';

export default {
  name: 'OverlayMessage',
  components: {
    SmallMessages,
  },
  setup() {
    const store = useMessagesStore();
    return { store };
  },
};
</script>

<style>
.unit-save-msg {
  margin-top: 1rem;
  margin-bottom: -3rem;
}

.unit-save-msg-container {
  position: fixed;
  /* padding-top: 30rem; */
  left: 85%;
  z-index: 1;
  pointer-events: none;
  gap: 1rem;
}

.message-stack {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}
</style>
