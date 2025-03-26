import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ViewUnit from '../views/ViewUnit.vue'
import ReportsView from '../views/ReportsView.vue'
import AccountView from '../views/AccountView.vue'
import AboutView from '../views/AboutView.vue'
import RescoreView from '../views/RescoreView.vue'
import { currentUser, loadUser } from '../services/authService'
import ViewUnits from '../views/ViewUnits.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
    },
    {
      path: '/reports',
      name: 'reports',
      component: ReportsView,
    },
    {
      path: '/view-units',
      name: 'view units',
      component: ViewUnits,
    },
    {
      path: '/view-unit',
      name: 'view unit',
      component: ViewUnit,
    },
    {
      path: '/account',
      name: 'account',
      component: AccountView,
    },
    {
      path: '/rescore',
      name: 'rescore',
      component: RescoreView,
      beforeEnter: (to, from, next) => {
        console.log(currentUser.value)
        checkAuth('admin', from, next)
      },
    },
  ],
})

async function checkAuth(role, from, next) {
  // Ensure user data is loaded
  if (currentUser.value === null) {
    await loadUser()
  }
  console.log(currentUser.value.role.toLowerCase())
  // Check access
  if (!currentUser.value || currentUser.value.role.toLowerCase() !== role) {
    // Prevent infinite loop by doing nothing if already on "/"
    if (from.path === '/') {
      return
    } else {
      // Navigate home if unauthorised
      next('/')
    }
  } else {
    // Proceed if authorised
    next()
  }
}

export default router
