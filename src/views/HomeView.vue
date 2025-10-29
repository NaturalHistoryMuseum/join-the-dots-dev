<template>
  <div class="main-page">
    <div class="main-header">
      <p class="h1-style">Join the Dots Portal</p>
      <div v-if="currentUser">
        <p v-if="currentUser.name">Welcome, {{ currentUser.name }}</p>
      </div>
      <!-- <HomeStats /> -->
    </div>
    <div class="boader-header">
      <p class="h2-style boader-header-title">Actions</p>
    </div>
    <b-row class="home-cards">
      <div v-if="currentUser.level > 1" class="home-card col-md-4">
        <i class="bi bi-clipboard-check card-icon"></i>
        <p class="h2-style">Rescore</p>
        <p>Perform a rescore on your assigned units.</p>
        <zoa-button
          label="Rescore"
          @click="navigate('/rescore')"
          class="card-btn"
        />
      </div>
      <div v-if="currentUser.level == 1" class="home-card col-md-4">
        <i class="bi bi-file-earmark card-icon"></i>
        <p class="h2-style">About</p>
        <p>Understand the JtD process further</p>
        <zoa-button
          label="Rescore"
          @click="navigate('/about')"
          class="card-btn"
        />
      </div>
      <!-- <div class="padd-card col-md-1"></div> -->
      <div class="home-card col-md-4">
        <i class="bi bi-table card-icon"></i>
        <p class="h2-style">View Units</p>
        <p>
          Explore all units or just your assigned units and make changes to
          them.
        </p>
        <zoa-button
          label="View units"
          @click="navigate('/view-units')"
          class="card-btn"
        />
      </div>
      <!-- <div class="padd-card col-md-1"></div> -->
      <div class="home-card col-md-4">
        <i class="bi bi-graph-up card-icon"></i>
        <p class="h2-style">Reports</p>
        <p>
          Generate reports on your assigned units or whole division's
          performance.
        </p>
        <zoa-button
          label="Reports"
          @click="navigate('/reports')"
          class="card-btn"
        />
      </div>
    </b-row>
  </div>

  <!-- <LoadingChart /> -->
</template>

<script>
// import HomeStats from '@/components/HomeStats.vue';
import { currentUser } from '../services/authService';

export default {
  setup() {
    return { currentUser };
  },
  // components: { HomeStats },
  data() {
    return {};
  },
  mounted() {},

  methods: {
    // Navigate to path
    navigate(path) {
      this.$router.push({ path: path });
    },
    // async getUserAzure() {
    // const response = await api.post(
    //   `auth/azure/user`,
    //   { email: this.currentUser.email },
    //   {
    //     withCredentials: true,
    //   },
    // );
    // },
  },
};
</script>

<style>
.h1-style {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}
.h2-style {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}
.h3-style {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}
.h4-style {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}
.h5-style {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.main-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0;
}
.main-header {
  margin: 2rem 6rem 1rem 6rem;
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
  margin-top: auto;
  align-self: end;
  justify-self: end;
  bottom: 0;
  height: auto;
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
    margin: 2rem 2rem 1rem 2rem;
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
