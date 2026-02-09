<template>
  <nav class="navbar">
    <div v-if="currentUser">
      <RouterLink
        v-for="(link, index) in nav_links.filter((link) =>
          link.access_groups.includes(currentUser.role.toLowerCase()),
        )"
        :key="index"
        :to="link.path"
        class="nav-item"
        :class="{ active: isActiveRoute(link.path) }"
      >
        {{ link.name }}
        <span class="hover-bar"></span>
        <span class="active-bar"></span>
      </RouterLink>
    </div>
  </nav>
</template>

<script>
import { useRoute } from 'vue-router';
import { currentUser } from '../services/authService';

export default {
  name: 'NavLinks',
  setup() {
    const route = useRoute();
    const nav_links = [
      {
        name: 'Home',
        path: '/',
        access_groups: ['admin', 'viewer', 'editor', 'manager'],
      },
      {
        name: 'View Units',
        path: '/view-units',
        access_groups: ['admin', 'viewer', 'editor', 'manager'],
      },
      {
        name: 'Rescore',
        path: '/rescore',
        access_groups: ['admin', 'editor', 'manager'],
      },
      {
        name: 'About',
        path: '/about',
        access_groups: ['admin', 'viewer', 'editor', 'manager'],
      },
      {
        name: 'Reporting',
        path: '/reports',
        access_groups: ['admin', 'viewer', 'editor', 'manager'],
      },

      { name: 'Admin', path: '/admin', access_groups: ['admin'] },
    ];

    const isActiveRoute = (path) => route.path === path;

    return {
      nav_links,
      isActiveRoute,
      currentUser,
    };
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  gap: 1rem;
  text-align: right;
  color: white;
  padding: 0;
}

.nav-item {
  position: relative;
  color: #fff;
  text-decoration: none;
  font-size: 16px;
  cursor: pointer;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  font-size: 1rem;
}

.nav-item:hover .hover-bar {
  opacity: 1;
}

.active-bar,
.hover-bar {
  position: absolute;
  bottom: -1.1rem;
  margin: 0 10px;
  left: 0;
  right: 0;
  height: 8px;
  background-color: white;
  opacity: 0;
  transition: opacity 0.3s;
}

.nav-item.active .active-bar {
  opacity: 1;
}

@media (max-width: 768px) {
  .navbar {
    gap: 0.5rem;
  }

  .nav-item {
    font-size: 14px;
  }
  nav a {
    display: inline-block;
    padding: 0 0.5rem;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .navbar {
    gap: 0.25rem;
  }

  .nav-item {
    font-size: 12px;
  }
  .active-bar,
  .hover-bar {
    bottom: -0.8rem;
  }
}
</style>
