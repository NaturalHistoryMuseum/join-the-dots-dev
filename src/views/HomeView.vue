<template>
  <div class="home">
    <div class="home-header">
      <p>Welcome, {{ user.name }} ({{ user.email }})</p>
      <h1>Join the Dots Portal</h1>
      <p>
        Sed dictum tincidunt dolor quis finibus. Donec in tincidunt augue. Curabitur dapibus vel
        mauris nec varius. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
        inceptos himenaeos. Nunc cursus auctor dui, vel cursus nunc cursus a. Aenean eu sem et dui
      </p>
    </div>
    <div class="home-content">
      <div>
        <zoa-button label="Rescore" @click="navRescore" />
      </div>
      <div>
        <zoa-button label="View units" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: [],
    }
  },
  async mounted() {
    // Check localStorage for stored user data
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      // Use stored user data if available
      this.user = JSON.parse(storedUser)
    }
  },
  methods: {
    navRescore() {
      this.$router.push({
        path: '/rescore',
        query: {
          sectionId: '2',
        },
      })
    },
  },
}
</script>

<style>
.home {
  /* display: flex; */
  align-items: center;
  padding: 0.5rem 2rem;
}
.home-header {
  margin: 2rem 6rem;
  text-align: left;
}

.home-content {
  display: grid;
  align-items: stretch;
  overflow: initial;
  width: auto;
  grid-template-rows: auto auto auto;
}
@media (max-width: 768px) {
  .home {
    padding: 0.5rem 1rem;
  }
  .home-header {
    margin: 2rem 2rem;
  }
}

@media (max-width: 480px) {
  .home {
    padding: 0.5rem 0.5rem;
  }
  .home-header {
    margin: 2rem 1rem;
  }
}
</style>
