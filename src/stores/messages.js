import { defineStore } from 'pinia';

export const useMessagesStore = defineStore('messages', {
  state: () => ({
    messages: [],
  }),
  actions: {
    addMessage(message_text, message_type) {
      this.messages.push({ message_text, message_type });
      this.removeMessage();
    },
    handleChangeResponse(response) {
      if (response.success) {
        this.addMessage('Change saved!', 'success');
      } else {
        this.addMessage('Change not saved', 'error');
      }
    },
    removeMessage() {
      setTimeout(() => {
        this.messages.shift();
      }, 3000);
    },
  },
});
