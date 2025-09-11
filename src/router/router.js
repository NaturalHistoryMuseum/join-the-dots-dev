import AdminView from '@/views/AdminView.vue';
import AssignmentManagement from '@/views/UnitAssignmentManagement.vue';
import UserManagement from '@/views/UserManagement.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { currentUser, loadUser } from '../services/authService';
import AboutView from '../views/AboutView.vue';
import AccountView from '../views/AccountView.vue';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import ReportsView from '../views/ReportsView.vue';
import RescoreView from '../views/RescoreView.vue';
import ViewUnit from '../views/ViewUnit.vue';
import ViewUnits from '../views/ViewUnits.vue';

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
          next('/');
        } else {
          next();
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
      beforeEnter: (to, from, next) => {
        checkAuth(2, from, next);
      },
    },
    // {
    //   path: '/manage-rescore',
    //   name: 'manage rescore',
    //   component: ManageRescoreView,
    //   meta: { requiresAuth: true },
    //   beforeEnter: (to, from, next) => {
    //     checkAuth(2, from, next);
    //   },
    // },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        checkAuth(4, from, next);
      },
    },
    {
      path: '/manage-unit-permissions',
      name: 'manage unit permissions',
      component: AssignmentManagement,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        checkAuth(2, from, next);
      },
    },
    {
      path: '/user-management',
      name: 'user management',
      component: UserManagement,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        checkAuth(3, from, next);
      },
    },
  ],
});

// Global route guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !currentUser.value) {
    next('/login');
  } else {
    next();
  }
});

async function checkAuth(level, from, next) {
  // Ensure user data is loaded
  if (currentUser.value === null) {
    await loadUser();
  }
  // Check access
  if (!currentUser.value || currentUser.value.level < level) {
    // Prevent infinite loop by doing nothing if already on "/"
    // if (from.path === '/') {
    //   return
    // } else {
    //   // Navigate home if unauthorised
    //   next('/')
    // }
    next('/');
  } else {
    // Proceed if authorised
    next();
  }
}

export default router;
