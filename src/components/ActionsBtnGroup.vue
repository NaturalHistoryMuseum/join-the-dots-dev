<template>
  <!-- Actions button group -->
  <div class="actions">
    <div class="actions-group">
      <zoa-button @click="toggleActions()" class="open-btn">
        Actions
        <div v-if="show_actions">
          <i class="bi bi-chevron-right accordion-icon"></i>
        </div>
        <div v-else>
          <i class="bi bi-chevron-left accordion-icon"></i>
        </div>
      </zoa-button>
      <transition name="fade">
        <div v-show="show_actions" class="action-btns">
          <slot></slot>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActionsBtnGroup',
  props: { force_show: Boolean },
  data() {
    return {
      show_actions: false,
    };
  },
  methods: {
    // Function to toggle the visibility of the actions button group
    toggleActions() {
      this.show_actions = !this.show_actions;
    },
  },
  watch: {
    force_show(newVal) {
      if (newVal) {
        this.show_actions = true;
      }
    },
  },
};
</script>

<style scoped>
.actions {
  display: flex;
  justify-content: flex-end;
  align-items: start;
  gap: 1rem;
}

.action-btns {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
}

.open-btn {
  display: flex;
  gap: 0.5rem;

  margin-left: auto;
  /* margin-bottom: 0.5rem; */
}
.actions-group {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>
