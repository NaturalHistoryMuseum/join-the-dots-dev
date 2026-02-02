<template>
  <div
    v-if="loadingStore.isLoading"
    class="loading-overlay d-flex justify-content-center align-items-center"
  >
    <!-- <img :src="loading_gif" alt="Loading..." class="loading-gif" />
      -->
    <div class="loading-msg">
      <b-spinner variant="light"></b-spinner>
      <h1 class="h2-style">Please wait, loading...</h1>
    </div>
  </div>
</template>

<script setup>
import { useLoadingStore } from '@/stores/loadingStore';

const loadingStore = useLoadingStore();
// const loading_gif = '/src/assets/dino-running.gif';
</script>

<script>
export default {
  name: 'LoadingOverlay',
  mounted() {
    document.addEventListener('focusin', this.focusIn);
  },
  methods: {
    // Prevents interaction with page elements when loading
    focusIn(event) {
      const loadingStore = useLoadingStore();
      if (loadingStore.isLoading) {
        event.target.blur();
      }
    },
  },
};
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.7); /* Dark semi-transparent background */
  z-index: 1050; /* Higher than modal */
}

.loading-msg {
  color: white;
  font-size: 1.5rem;
  text-align: center;
}
</style>
