<template>
  <div class="main-page">
    <div class="main-header">
      <div v-if="currentUser">
        <p>Welcome, {{ currentUser.name }}</p>
      </div>
      <h1>Join the Dots Portal</h1>

      <p>
        Sed dictum tincidunt dolor quis finibus. Donec in tincidunt augue. Curabitur dapibus vel
        mauris nec varius. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
        inceptos himenaeos. Nunc cursus auctor dui, vel cursus nunc cursus a. Aenean eu sem et dui
      </p>
    </div>
    <!-- <div class="main-content">
      <div class="grid-comp">
        <zoa-button label="Rescore" @click="navRescore" />
      </div>
      <div class="grid-comp">
        <zoa-button label="View units" />
      </div>
    </div> -->
    <div class="boader-header">
      <h2>Actions</h2>
    </div>
    <b-row>
      <b-col class="home-card">
        <i class="bi bi-clipboard-check card-icon"></i>
        <h2>Rescore</h2>
        <p>Perform a re-scoring on your assigned sections.</p>
        <zoa-button label="Rescore" @click="navRescore" class="card-btn" />
      </b-col>
      <b-col class="home-card">
        <i class="bi bi-table card-icon"></i>
        <h2>View Units</h2>
        <p>Explore all units in your section and make changes to them.</p>
        <zoa-button label="View units" class="card-btn" />
      </b-col>
      <b-col class="home-card">3 of 3</b-col>
    </b-row>
  </div>
</template>

<script>
import { currentUser } from '../services/authService'

export default {
  setup() {
    return { currentUser }
  },
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
.main-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem 2rem;
}
.main-header {
  margin: 2rem 6rem;
  text-align: left;
}

.main-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}

.grid-comp {
  margin: 1rem;
  width: 40%;
}

.home-card {
  background-color: var(--secondary-col);
  margin: 0 1rem;
  display: flex;
  flex-direction: column;
  align-items: start;
  text-align: start;
  padding: 0.5rem;
  color: white;
}

.card-icon {
  align-self: start;
  font-size: 2.5rem;
  color: white;
}

.card-btn {
  margin-top: 1rem;
  align-self: end;
}
.boader-header {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.boader-header::after .boader-header::before {
  /* content: '';
  flex: 1;
  display: block;
  border-bottom: 2px solid black;
  position: absolute;
  /* z-index: -1; */
  /* top: 50%; */
  content: '';
  flex: 1;
  border-top: 1px solid black; /* You can change the color or thickness */
  margin: 0 10px;
}
.h2 {
  display: inline-block;
  padding: 0 10px;
}

@media (max-width: 768px) {
  .home {
    padding: 0.5rem 1rem;
  }
  .main-header {
    margin: 2rem 2rem;
  }
}

@media (max-width: 480px) {
  .home {
    padding: 0.5rem 0.5rem;
  }
  .main-header {
    margin: 2rem 1rem;
  }
}
</style>
