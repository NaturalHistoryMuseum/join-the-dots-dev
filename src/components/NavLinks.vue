<template>
  <nav class="navbar">
    <RouterLink
      v-for="(link, index) in navLinks"
      :key="index"
      :to="link.path"
      class="nav-item"
      :class="{ active: isActiveRoute(link.path) }"
    >
      {{ link.name }}
      <span class="hover-bar"></span>
      <span class="active-bar"></span>
    </RouterLink>
  </nav>
</template>

<script>
import { useRoute } from 'vue-router'

export default {
  name: 'NavLinks',
  setup() {
    const route = useRoute()

    const navLinks = [
      { name: 'Home', path: '/' },
      { name: 'About', path: '/about' },
      { name: 'Reports', path: '/reports' },
    ]

    const isActiveRoute = (path) => route.path === path

    return {
      navLinks,
      isActiveRoute,
    }
  },
}
</script>

<style scoped>
.navbar {
  display: flex;
  gap: 1rem;
  text-align: right;
  /* margin-top: 0.5rem; */
  color: white;
  padding: 0;
}

.nav-item {
  position: relative;
  color: #fff;
  text-decoration: none;
  font-size: 16px;
  /* padding: 8px; */
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
  /* bottom: -12px; */
  bottom: -1.1rem;
  margin: 0 10px;
  left: 0;
  right: 0;
  height: 6px;
  background-color: white;
  opacity: 0;
  transition: opacity 0.3s;
}

.nav-item.active .active-bar {
  opacity: 1;
}

@media (max-width: 768px) {
  .navbar {
    gap: 0.5rem; /* Reduce gap for smaller screens */
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
