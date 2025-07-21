import './assets/global.less';
import './assets/main.css';

import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from './App.vue';
import router from './router/router';

import { Zoa } from '@nhm-data/zoa';
import '@nhm-data/zoa/theme';

// Import Bootstrap and BootstrapVue and Icons CSS files
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';
import 'bootstrap/dist/css/bootstrap.css';

// Import BootstrapVue3
import BootstrapVue3 from 'bootstrap-vue-3';

// Import load user function
import { loadUser } from './services/authService';

async function init() {
  await loadUser();

  const app = createApp(App);

  const pinia = createPinia();
  app.use(pinia);

  app.use(router);
  app.use(BootstrapVue3);
  app.use(Zoa);

  app.mount('#app');
}
init();
