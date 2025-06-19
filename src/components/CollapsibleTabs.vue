<template>
  <div class="tab-section">
    <!-- Sidebar -->
    <div
      class="sidebar"
      :style="{
        width: is_collapsed ? collapsed_width : expanded_width,
      }"
    >
      <div class="sidebar-header">
        <!-- Button to show/hide unit names -->
        <zoa-button @click="toggleSidebar" class="toggle-btn">
          <div v-if="is_collapsed"><i class="bi bi-list btn-icon"></i></div>
          <div v-else><i class="bi bi-x-lg btn-icon"></i></div>
        </zoa-button>
        <!-- Button to show/hide completed units from list -->
        <div v-if="!is_collapsed">
          <zoa-button @click="filter_completed = !filter_completed">{{
            filter_completed ? 'Show Completed' : 'Hide Completed'
          }}</zoa-button>
        </div>
      </div>
      <!-- Tabs for each unit -->
      <div
        class="tab-container"
        :style="{
          width: is_collapsed ? collapsed_width : expanded_width,
        }"
      >
        <button
          v-for="(unit, index) in !filter_completed
            ? units
            : units.filter((unit) => !checkUnitCompleted(unit))"
          :key="index"
          @click="active_tab = unit.collection_unit_id"
          :class="[
            'tab',
            active_tab === unit.collection_unit_id ? 'active' : '',
            is_collapsed ? 'icon-only' : '',
          ]"
          :style="{
            backgroundColor:
              active_tab === unit.collection_unit_id ? '#f2bab0' : '#e0e0e0',
            width: is_collapsed ? collapsed_width : expanded_width,
          }"
        >
          <!-- If tab out - display name and whether its completed -->
          <span class="tab-title" v-if="!is_collapsed"
            >{{ unit.unit_name }}
            <div v-if="checkUnitCompleted(unit)">
              <i class="bi bi-check-lg"></i>
            </div>
            <div v-else><i class="bi bi-x-lg"></i></div
          ></span>
        </button>
      </div>
    </div>
    <!-- Content Area -->
    <div class="content">
      <div v-if="units.length">
        <!-- Display the scores for this unit and enable editing for rescore -->
        <UnitScores
          v-if="units.find((unit) => unit.collection_unit_id == active_tab)"
          :unit="units.find((unit) => unit.collection_unit_id == active_tab)"
          :rescore="true"
          :fetchUnitsData="fetchUnitsData"
        />
      </div>
    </div>
  </div>
</template>

<script>
import UnitScores from './UnitScores.vue';

export default {
  props: {
    units: Array,
    rescore_status: Array,
    fetchUnitsData: Function,
  },
  components: {
    UnitScores,
  },
  data() {
    return {
      is_collapsed: false,
      active_tab: this.units.length ? this.units[0].collection_unit_id : 0,
      expanded_width: '300px',
      collapsed_width: '50px',
      filter_completed: false,
    };
  },
  methods: {
    // Function to toggle the sidebar
    toggleSidebar() {
      this.is_collapsed = !this.is_collapsed;
    },
    // Function to navigate to the unit
    navUnit(unitId) {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: unitId,
        },
      });
    },
    // Function to check if all categories in a unit are completed
    checkUnitCompleted(unit) {
      // Get the json object from the unit
      const categories_json = unit.category_tracking;
      // Check if all categories are complete
      const completed = categories_json.every((category) => {
        return category.complete == 1;
      });
      return completed;
    },
  },
  watch: {},
};
</script>

<style scoped>
.tab-section {
  display: flex;
}

.sidebar {
  transition: width 0.3s;
  color: white;
  display: flex;
  flex-direction: column;
  margin: 10px;
  width: 50px;
}
.sidebar-header {
  margin-bottom: 1rem;
}

.toggle-btn {
  padding: 10px;
  border: none;
  cursor: pointer;
  width: 3rem;
}

.tab-container {
  display: flex;
  flex-direction: column;
  width: 15rem;
  z-index: 1;
  border-left: 5px solid #f2bab0;
}

.tab-title {
  /* display: inline-block; */
  display: flex;
  justify-content: space-between;
  padding-right: 1rem;
  font-weight: 600;
}

.tab {
  padding: 10px;
  border: none;
  cursor: pointer;
  color: black;
  font-weight: 600;
  text-align: left;
  border-radius: 0px 20px 20px 0px;
  margin-bottom: 5px;
  transition: all 0.3s;
}

.tab.icon-only {
  text-align: center;
}

.content {
  flex: 1;
  padding: 10px 20px;
}

.btn-icon {
  font-size: 1.3rem;
  color: black;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
