<template>
  <SmallMessages :message_text="message_text" :message_type="message_type" />
  <div class="main-page">
    <div class="main-header">
      <h1 class="h1-style">Join the Dots Portal</h1>
      <div v-if="currentUser">
        <p v-if="currentUser.name">Welcome, {{ currentUser.name }}</p>
      </div>
    </div>
    <div class="border-header">
      <h2 class="h2-style border-header-title">Actions</h2>
    </div>
    <b-row class="home-cards">
      <div v-if="currentUser.level > 1" class="home-card col-md-4">
        <i class="bi bi-clipboard-check card-icon"></i>
        <h2 class="h2-style">Rescore</h2>
        <p>Perform a rescore on your assigned units.</p>
        <zoa-button
          label="Rescore"
          @click="navigate('/rescore')"
          class="card-btn"
        />
      </div>
      <div v-if="currentUser.level == 1" class="home-card col-md-4">
        <i class="bi bi-file-earmark card-icon"></i>
        <h2 class="h2-style">About</h2>
        <p>Understand the JtD process further</p>
        <zoa-button
          label="About"
          @click="navigate('/about')"
          class="card-btn"
        />
      </div>
      <div class="home-card col-md-4">
        <i class="bi bi-table card-icon"></i>
        <h2 class="h2-style">View Units</h2>
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
      <div class="home-card col-md-4">
        <i class="bi bi-graph-up card-icon"></i>
        <h2 class="h2-style">Reporting</h2>
        <p>View the JtD Power BI report and export data.</p>
        <zoa-button
          label="Reports"
          @click="navigate('/reports')"
          class="card-btn"
        />
      </div>
    </b-row>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';
import OverlayMessage from '../components/OverlayMessage.vue';
import SmallMessages from '../components/SmallMessages.vue';
import { currentUser } from '../services/authService';

export default {
  components: {
    OverlayMessage,
    SmallMessages,
  },
  setup() {
    return { currentUser };
  },
  data() {
    return { message_text: '', message_type: '' };
  },
  mounted() {
    if (this.currentUser.level == 4) {
      this.checkIssues();
    }
  },
  methods: {
    // Navigate to path
    navigate(path) {
      this.$router.push({ path: path });
    },
    async checkIssues() {
      const issues = await getGeneric('all-issues');
      let num_open_issues = issues.filter(
        (issue) => issue.status !== 'resolved',
      ).length;
      if (num_open_issues > 0) {
        let num_new_issues = issues.filter(
          (issue) => issue.status === 'raised',
        ).length;
        this.message_text = `There are ${num_open_issues} open issues - ${num_new_issues} are new`;
        this.message_type = 'error';
      }
    },
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
.border-header {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  margin: 1rem 0;
}
.border-header::after,
.border-header::before {
  content: '';
  flex: 1;
  border-top: 1px solid black;
  margin: 0 10px;
}
.border-header-title {
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
  */ .border-header-title {
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
  .border-header-title {
    margin: 0 1rem;
  }
}
</style>
