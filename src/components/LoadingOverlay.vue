<template>
  <div
    v-if="loadingStore.isLoading"
    class="loading-overlay d-flex justify-content-center align-items-center"
  >
    <!-- <div class="spinner-border text-light" role="status">
      <span class="">Loading...</span>
    </div> -->

    <img :src="loading_gif" alt="Loading..." class="loading-gif" />
  </div>
</template>

<script setup>
import { useLoadingStore } from '@/stores/loadingStore';

const loadingStore = useLoadingStore();
// const loading_gif = '/src/assets/running-dinosaur.gif'
const loading_gif = '/src/assets/dino-running.gif';
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
</style>
