<script setup>
import { RouterView } from 'vue-router'
import HeaderView from './views/HeaderView.vue'
</script>

<template>
  <HeaderView />

  <div class="content">
    <RouterView />
  </div>
</template>

<style scoped lang="scss">
// @import 'fonts';

// body {
//   font-family: 'NHM Wallop Text', sans-serif;
// }

.content {
  display: flex;
  flex-direction: column;
  /* align-items: center; */
  justify-content: center;
  /* height: calc(100vh); */
  text-align: center;
}
</style>
