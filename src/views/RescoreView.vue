<template>
  <div class="rescore">
    <div class="main-header">
      <div class="row">
        <!-- Rescore Details -->
        <div class="col-md-6">
          <h1>Rescore</h1>
          <div v-if="units.length > 0">
            <h5>Section: {{ units[0].section_name }}</h5>
            <h5>Units assigned: {{ units.length }}</h5>
            <h5>Units completed: {{ countUnitsCompleted(units) }}</h5>
          </div>
        </div>
        <!-- Actions button group -->
        <div class="col-md-6 actions">
          <div class="actions-group">
            <zoa-button @click="toggleActions()" class="const-btn"
              >Actions <i class="bi bi-three-dots-vertical"></i
            ></zoa-button>
            <transition name="fade">
              <div v-show="show_actions" class="action-btns">
                <zoa-button kind="primary">Bulk update</zoa-button>
                <zoa-button kind="alt">See History</zoa-button>
                <zoa-button kind="primary">Other Action</zoa-button>
                <zoa-button kind="alt">Third Action</zoa-button>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Collapsible Tabs to show units -->
    <CollapsibleTabs :units="units" :fetchUnitsData="fetchUnitsData" />
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import CollapsibleTabs from '@/components/CollapsibleTabs.vue'
import { getGeneric } from '@/services/dataService'

export default {
  name: 'DeptUnit',
  components: {
    CollapsibleTabs,
  },
  setup() {
    const route = useRoute()

    // Access query parameters
    const rescore_session_id = ref(null)
    onMounted(() => {
      rescore_session_id.value = route.query.rescore_session_id
    })

    return {
      rescore_session_id,
    }
  },
  data() {
    return {
      units: [],
      show_actions: false,
    }
  },
  mounted() {
    this.fetchUnitsData()
  },
  methods: {
    fetchUnitsData() {
      // Fetch units in this rescore session
      getGeneric(`rescore-units/${this.rescore_session_id}`).then((response) => {
        this.units = response
      })
    },
    // Function to toggle the visibility of the actions button group
    toggleActions() {
      this.show_actions = !this.show_actions
    },
    // Function to count the number of completed units
    countUnitsCompleted(units) {
      let completed_count = 0
      // Loop through each unit and check if all categories are complete
      units.forEach((unit) => {
        const categories_json = JSON.parse(unit.category_tracking)
        const completed = categories_json.every((category) => {
          return category.complete == 1
        })
        if (completed) {
          completed_count++
        }
      })
      return completed_count
    },
  },
}
</script>

<style>
.prog-bar {
  margin-top: 1rem;
  width: 20rem;
}

/* .main-page {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 2rem;
} */

.flash-box {
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  border-color: #0dedf7;
  padding: 0px !important;
}
.flash-header {
  background-color: #e6fdfd;
  border-radius: 10px 10px 0 0;
  width: 100%;
  padding: 0.5rem;
  text-align: center;
  font-weight: 600;
}

.flash-content {
  padding: 1rem;
}

.actions {
  display: flex;
  justify-content: flex-end;
  align-items: start;
  gap: 1rem;
}

.action-btns {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
}

.const-btn {
  margin-left: auto;
  /* margin-bottom: 0.5rem; */
}
.actions-group {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>
