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
      <h2 class="boader-header-title">Actions</h2>
    </div>
    <b-row class="home-cards">
      <div class="home-card col-md-4">
        <i class="bi bi-clipboard-check card-icon"></i>
        <h2>Rescore</h2>
        <p>Perform a re-scoring on your assigned sections.</p>
        <zoa-button label="Rescore" @click="navRescore" class="card-btn" />
      </div>
      <!-- <div class="padd-card col-md-1"></div> -->
      <div class="home-card col-md-4">
        <i class="bi bi-table card-icon"></i>
        <h2>View Units</h2>
        <p>Explore all units in your section and make changes to them.</p>
        <zoa-button label="View units" @click="navViewUnits" class="card-btn" />
      </div>
      <!-- <div class="padd-card col-md-1"></div> -->
      <div class="home-card col-md-4">
        <i class="bi bi-graph-up card-icon"></i>
        <h2>Reports</h2>
        <p>Generate reports on your section's performance.</p>
        <zoa-button label="Reports" @click="navReports" class="card-btn" />
      </div>
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
        path: '/manage-rescore',
      })
    },
    navViewUnits() {
      this.$router.push({
        path: '/view-units',
      })
    },
    navReports() {
      this.$router.push({
        path: '/reports',
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
  padding: 0;
}
.main-header {
  margin: 2rem 6rem;
  text-align: left;
  width: 90%;
}

.main-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}

.grid-comp {
  margin: 1rem;
  width: 40%;
}
.home-cards {
  width: 100%;
  display: flex;
  justify-items: center;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: stretch;
  /* align-items: center; */
  flex: 1 1 0;
}
.home-card {
  background-color: var(--secondary-col);
  /* margin: 0 5px 10px; */
  display: flex;
  flex-direction: column;
  align-items: start;
  text-align: start;
  padding: 0.5rem;
  color: white;
  border: 5px solid white;
}

.card-icon {
  align-self: start;
  font-size: 2.5rem;
  color: white;
}

.card-btn {
  margin-top: 1rem;
  align-self: end;
  justify-self: end;
  bottom: 0;
  top: auto;
}
.boader-header {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  margin: 1rem 0;
}
.boader-header::after,
.boader-header::before {
  content: '';
  flex: 1;
  border-top: 1px solid black;
  margin: 0 10px;
}
.boader-header-title {
  margin: 0 4rem;
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
  * .home-cards > * {
    flex: 1 1 0;
  }
  */ .boader-header-title {
    margin: 0 2rem;
  }
  .main-page {
    padding: 0;
  }
}

@media (max-width: 480px) {
  .home {
    padding: 0.5rem 0.5rem;
  }
  .main-header {
    margin: 2rem 0.5rem;
    width: 95%;
  }
  .boader-header-title {
    margin: 0 1rem;
  }
}
</style>
