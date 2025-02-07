import './assets/main.css'
import './assets/global.less'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { Zoa } from '@nhm-data/zoa'
import '@nhm-data/zoa/theme'

// Import Bootstrap and BootstrapVue and Icons CSS files
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

// Import BootstrapVue3
import BootstrapVue3 from 'bootstrap-vue-3'

// Import load user function
import { loadUser } from './services/authService'

loadUser()

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(BootstrapVue3)
app.use(Zoa)

app.mount('#app')
