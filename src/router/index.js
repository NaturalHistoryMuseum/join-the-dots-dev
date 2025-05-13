import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ViewUnit from '../views/ViewUnit.vue'
import ReportsView from '../views/ReportsView.vue'
import AccountView from '../views/AccountView.vue'
import AboutView from '../views/AboutView.vue'
import RescoreView from '../views/RescoreView.vue'
import { currentUser, loadUser } from '../services/authService'
import ViewUnits from '../views/ViewUnits.vue'
import ManageRescoreView from '@/views/ManageRescoreView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false },
      beforeEnter: (to, from, next) => {
        if (currentUser.value) {
          next('/')
        } else {
          next()
        }
      },
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: { requiresAuth: true },
    },
    {
      path: '/reports',
      name: 'reports',
      component: ReportsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/view-units',
      name: 'view units',
      component: ViewUnits,
      meta: { requiresAuth: true },
    },
    {
      path: '/view-unit',
      name: 'view unit',
      component: ViewUnit,
      meta: { requiresAuth: true },
    },
    {
      path: '/account',
      name: 'account',
      component: AccountView,
      meta: { requiresAuth: true },
    },
    {
      path: '/rescore',
      name: 'rescore',
      component: RescoreView,
      meta: { requiresAuth: true },
      // beforeEnter: (to, from, next) => {
      //   console.log(currentUser.value)
      //   checkAuth('admin', from, next)
      // },
    },
    {
      path: '/manage-rescore',
      name: 'manage rescore',
      component: ManageRescoreView,
      meta: { requiresAuth: true },
    },
  ],
})

// Global route guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !currentUser.value) {
    next('/login')
  } else {
    next()
  }
})

// async function checkAuth(role, from, next) {
//   // Ensure user data is loaded
//   if (currentUser.value === null) {
//     await loadUser()
//   }
//   console.log(currentUser.value.role.toLowerCase())
//   // Check access
//   if (!currentUser.value || currentUser.value.role.toLowerCase() !== role) {
//     // Prevent infinite loop by doing nothing if already on "/"
//     if (from.path === '/') {
//       return
//     } else {
//       // Navigate home if unauthorised
//       next('/')
//     }
//   } else {
//     // Proceed if authorised
//     next()
//   }
// }

export default router
