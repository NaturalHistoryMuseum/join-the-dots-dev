<template>
  <div class="tab-section">
    <!-- Sidebar -->
    <div
      class="sidebar"
      :style="{
        width: isCollapsed ? collapsedWidth : expandedWidth,
      }"
    >
      <div class="sidebar-header">
        <zoa-button @click="toggleSidebar" class="toggle-btn">
          <!-- {{ isCollapsed ? <i class="bi bi-list"></i> : '<' }} -->
          <div v-if="isCollapsed"><i class="bi bi-list btn-icon"></i></div>
          <div v-else><i class="bi bi-x-lg btn-icon"></i></div>
        </zoa-button>
        <div v-if="!isCollapsed">
          <zoa-button @click="filter_completed = !filter_completed">{{
            filter_completed ? 'Show Completed' : 'Hide Completed'
          }}</zoa-button>
        </div>
      </div>
      <div
        class="tab-container"
        :style="{
          width: isCollapsed ? collapsedWidth : expandedWidth,
        }"
      >
        <button
          v-for="(unit, index) in !filter_completed
            ? units
            : units.filter((unit) => !checkUnitCompleted(unit))"
          :key="index"
          @click="activeTab = unit.collection_unit_id"
          :class="[
            'tab',
            activeTab === unit.collection_unit_id ? 'active' : '',
            isCollapsed ? 'icon-only' : '',
          ]"
          :style="{
            backgroundColor: activeTab === unit.collection_unit_id ? '#f2bab0' : '#e0e0e0',
            width: isCollapsed ? collapsedWidth : expandedWidth,
          }"
        >
          <span class="tab-title" v-if="!isCollapsed"
            >{{ unit.unit_name }}
            <div v-if="checkUnitCompleted(unit)"><i class="bi bi-check-lg"></i></div>
            <div v-else><i class="bi bi-x-lg"></i></div
          ></span>
        </button>
      </div>
    </div>

    <!-- Content Area -->
    <div class="content">
      <div v-if="units.length">
        <!-- {{ units[activeTab].collection_unit_id }}
        <zoa-button @click="navUnit(units[activeTab].collection_unit_id)">Go to unit</zoa-button> -->
        <!-- <RescoreComp :unit="units[activeTab]" /> -->
        <RescoreCompV2
          :unit="units.find((unit) => unit.collection_unit_id == activeTab)"
          :rescore="true"
          :fetchUnitsData="fetchUnitsData"
        />
      </div>
    </div>
  </div>
</template>

<script>
// import RescoreComp from './RescoreComp.vue'
import RescoreCompV2 from './RescoreCompV2.vue'

export default {
  props: {
    units: Array,
    rescore_status: Array,
    fetchUnitsData: Function,
  },
  components: {
    // RescoreComp,
    RescoreCompV2,
  },
  data() {
    return {
      isCollapsed: false,
      activeTab: this.units.length ? this.units[0].collection_unit_id : 0,
      expandedWidth: '300px',
      collapsedWidth: '50px',
      filter_completed: false,
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
    },
    navUnit(unitId) {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: unitId,
        },
      })
    },
    checkUnitCompleted(unit) {
      const categories_json = JSON.parse(unit.category_tracking)
      const completed = categories_json.every((category) => {
        return category.complete == 1
      })
      return completed
    },
    syncFromProps() {
      this.activeTab = this.units.length ? this.units[0].collection_unit_id : 0
    },
  },
  watch: {
    units: {
      handler() {
        this.syncFromProps()
      },
      deep: false,
    },
  },
}
</script>

<style scoped>
.tab-section {
  display: flex;
  height: 100vh;
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
