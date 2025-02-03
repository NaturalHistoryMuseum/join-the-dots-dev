import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TestView from '../views/TestView.vue'
import ViewUnit from '../views/ViewUnit.vue'
import ReportsView from '../views/ReportsView.vue'
import AccountView from '../views/AccountView.vue'

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
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/reports',
      name: 'reports',
      component: ReportsView,
    },
    {
      path: '/test-page',
      name: 'test page',
      component: TestView,
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
      component: () => import('../views/RescoreView.vue'),
    },
  ],
})

export default router
