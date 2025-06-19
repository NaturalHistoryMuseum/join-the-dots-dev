<template>
  <div class="tab-container">
    <button
      v-for="(tab, index) in tabs"
      :key="index"
      @click="changeTabFunc(index)"
      :class="['tab', active_tab === index ? 'active' : '']"
      :style="{
        backgroundColor: active_tab === index ? '#f2bab0' : '#e0e0e0',
      }"
    >
      <span class="tab-title">{{ tab.label }}</span>
    </button>
  </div>
  <slot></slot>
</template>

<script>
export default {
  components: {},
  props: {
    tabs: Array,
    active_tab: Number,
    changeTabFunc: Function,
  },
  data() {
    return {};
  },
  computed: {},
};
</script>

<style scoped>
.tab-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  border-bottom: 3px solid #f2bab0;
  overflow-x: auto;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
  scrollbar-width: none; /* Hide scrollbar on Firefox */
}

.tab-container::-webkit-scrollbar {
  display: none; /* Hide scrollbar on Chrome, Safari */
}

.tab {
  padding: 0.5rem 2rem;
  border: none;
  cursor: pointer;
  color: black;
  font-weight: 600;
  text-align: center;
  border-radius: 20px 20px 0px 0px;
  margin-right: 5px;
  transition: all 0.3s;
  flex-shrink: 0; /* Prevent tabs from shrinking */
}

@media (max-width: 768px) {
  .tab {
    padding: 0.4rem 1rem;
  }
}

@media (max-width: 480px) {
}
</style>
