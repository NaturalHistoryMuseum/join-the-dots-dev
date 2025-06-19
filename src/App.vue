<script setup>
import { RouterView } from 'vue-router'
import HeaderView from './views/HeaderView.vue'
import LoadingOverlay from './components/LoadingOverlay.vue'
import FooterView from './views/FooterView.vue'
</script>

<template>
  <LoadingOverlay />
  <HeaderView class="header" />

  <div class="content">
    <RouterView />
  </div>
  <FooterView class="footer" />
</template>

<style scoped lang="scss">
// @import 'fonts';

// body {
//   font-family: 'NHM Wallop Text', sans-serif;
// }

.content {
  display: flex;
  flex-direction: column;
  text-align: center;
  min-height: 70vh;
  margin-bottom: 1rem;
}
</style>
