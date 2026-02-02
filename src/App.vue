<script setup>
import { RouterView, useRouter } from 'vue-router';
import FooterView from './views/FooterView.vue';
import HeaderView from './views/HeaderView.vue';
const router = useRouter();

function handleBackPage() {
  router.go(-1);
}
</script>

<template>
  <LoadingOverlay />
  <HeaderView class="header" />
  <div class="content">
    <div class="nav-buttons" v-if="currentUser">
      <zoa-button @click="handleBackPage">
        <i class="bi bi-arrow-left"></i>
        Back
      </zoa-button>
      <zoa-button @click="$router.push('/help')">
        <i class="bi bi-question-circle"></i>
        Help
      </zoa-button>
    </div>
    <main>
      <RouterView />
    </main>
  </div>
  <FooterView class="footer" />
</template>

<script>
import { currentUser } from '../src/services/authService';
import LoadingOverlay from './components/LoadingOverlay.vue';

export default {
  name: 'App',
  setup() {
    return { currentUser };
  },
};
</script>

<style scoped lang="scss">
.content {
  display: flex;
  flex-direction: column;
  text-align: center;
  min-height: 70vh;
  margin-bottom: 1rem;
}

.nav-buttons {
  display: flex;
  justify-content: space-between;
  margin-left: 1rem;
}
</style>
