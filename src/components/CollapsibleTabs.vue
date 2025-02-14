<template>
  <div class="tab-section">
    <!-- Sidebar -->
    <div class="sidebar">
      <button @click="toggleSidebar" class="toggle-btn">
        {{ isCollapsed ? '>' : '<' }}
      </button>
      <div class="tab-container">
        <button
          v-for="(unit, index) in units"
          :key="index"
          @click="activeTab = index"
          :class="['tab', activeTab === index ? 'active' : '', isCollapsed ? 'icon-only' : '']"
          :style="{
            backgroundColor: activeTab === index ? '#f2bab0' : '#87999e',
            width: isCollapsed ? '50px' : '220px',
          }"
        >
          <span class="tab-title" v-if="!isCollapsed">{{ unit.unit_name }}</span>
        </button>
      </div>
    </div>

    <!-- Content Area -->
    <div class="content">
      <div v-if="units.length">
        {{ units[activeTab].collection_unit_id }}
        <RescoreComp :unit="units[activeTab]" />
      </div>
    </div>
  </div>
</template>

<script>
import RescoreComp from './RescoreComp.vue'

export default {
  props: {
    units: Array,
  },
  components: {
    RescoreComp,
  },
  data() {
    return {
      isCollapsed: false,
      activeTab: 0,
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
    },
  },
}
</script>

<style scoped>
.tab-section {
  display: flex;
  /* height: 100vh; */
  z-index: 0;
}

.sidebar {
  transition: width 0.3s;
  /* background-color: #1f2937; */
  color: white;
  display: flex;
  flex-direction: column;
  padding: 10px;
  width: 50px;
}

/* .collapsed {
  width: 60px;
}

.expanded {
  width: 180px;
} */

.toggle-btn {
  background-color: #87999e;
  padding: 10px;
  border: none;
  cursor: pointer;
  margin-bottom: 10px;
  color: black;
}

.tab-container {
  display: flex;
  flex-direction: column;
  width: 15rem;
  z-index: 1;
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

/* .tab.active {
  opacity: 0.75;
  background-color: #f2bab0;
} */
/* .active {
  background-color: #f2bab0;
} */

.content {
  flex: 1;
  padding: 20px;
  /* background-color: #f3f4f6; */
}
</style>
