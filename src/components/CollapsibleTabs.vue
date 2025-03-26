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
          <zoa-button>Hide Completed</zoa-button>
        </div>
      </div>
      <div
        class="tab-container"
        :style="{
          width: isCollapsed ? collapsedWidth : expandedWidth,
        }"
      >
        <button
          v-for="(unit, index) in units"
          :key="index"
          @click="activeTab = index"
          :class="['tab', activeTab === index ? 'active' : '', isCollapsed ? 'icon-only' : '']"
          :style="{
            backgroundColor: activeTab === index ? '#f2bab0' : '#e0e0e0',
            width: isCollapsed ? collapsedWidth : expandedWidth,
          }"
        >
          <span class="tab-title" v-if="!isCollapsed">{{ unit.unit_name }}</span>
        </button>
      </div>
    </div>

    <!-- Content Area -->
    <div class="content">
      <div v-if="units.length">
        <!-- {{ units[activeTab].collection_unit_id }}
        <zoa-button @click="navUnit(units[activeTab].collection_unit_id)">Go to unit</zoa-button> -->
        <!-- <RescoreComp :unit="units[activeTab]" /> -->
        <RescoreCompV2 :unit="units[activeTab]" />
      </div>
    </div>
  </div>
</template>

<script>
import RescoreComp from './RescoreComp.vue'
import RescoreCompV2 from './RescoreCompV2.vue'

export default {
  props: {
    units: Array,
  },
  components: {
    RescoreComp,
    RescoreCompV2,
  },
  data() {
    return {
      isCollapsed: false,
      activeTab: 0,
      expandedWidth: '300px',
      collapsedWidth: '50px',
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
  display: inline-block;
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
