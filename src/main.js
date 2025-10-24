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
import { initApi } from './services/api';
import { loadUser } from './services/authService';

async function init() {
  // Load config
  await loadConfig();
  await initApi();
  // Load user
  await loadUser();

  // Create Vue app
  const app = createApp(App);
  const pinia = createPinia();

  // Register plugins
  app.use(pinia);
  app.use(router);
  app.use(BootstrapVue3);
  app.use(Zoa);

  // Mount app
  app.mount('#app');
}
init();

async function loadConfig() {
  try {
    const res = await fetch('./config.json');
    if (!res.ok) throw new Error('config json not found');
    const config = await res.json();

    window.APP_CONFIG = config;
    return config;
  } catch (err) {
    console.error('Failed to load config json:', err);
    // fallback values
    return {
      API_URL: 'http://localhost:5000/api',
      APP_ENV: 'local',
    };
  }
}
