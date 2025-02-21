<template>
  <div class="rescore">
    <div class="main-header">
      <div class="row">
        <div class="col-md-6">
          <h1>Rescore</h1>
          <div v-if="units.length > 0">
            <h5>Section: {{ units[0].section_name }}</h5>
            <h5>Units assigned: {{ units.length }}</h5>
            <h5>Units completed: {{ 'xyz' }}</h5>
          </div>
          <div v-else>
            <h5>Section: {{ 'aahhh temp - not loaded' }}</h5>
            <h5>Units assigned: {{ 'aahhh temp - not loaded' }}</h5>
            <h5>Units completed: {{ 'xyz' }}</h5>
          </div>
          <b-progress :value="20" :max="100" class="prog-bar" show-progress></b-progress>
        </div>
        <div class="col-md-6 flash-box">
          <div class="flash-header"><h2>Action Station</h2></div>
          <div class="flash-content">
            <zoa-button label="Bulk Update Scores" />
            <zoa-button label="See History" kind="primary" />
            <zoa-button label="Go to unit" kind="alt" />
          </div>
          <!-- <zoa-flash kind="info" :message="" header="Action Station" /> -->
        </div>
      </div>
    </div>

    <!-- <div v-if="units.length < 0">
      <div v-for="unit in units" :key="unit.unit_id">
        <h3>{{ unit.unit_name }}</h3>
        <p>{{ unit.unit_description }}</p>
      </div>
    </div>
    <div v-else>
      <zoa-tabs
        :class="string"
        :active-position="right"
        :kind="normal"
        :options="unitNames"
        :size="'md'"
      />
    </div> -->

    <CollapsibleTabs :units="units" />
    <!-- <div>
      <b-row class="wrap" ref="wrap">
        <b-tabs vertical pills card content-class="mt-3 tab-scroll">
          <b-tab v-for="unit in units" :key="unit.unit_id" :title="unit.unit_name" active>
            <RescoreComp :unit="unit" />
          </b-tab>
        </b-tabs>
      </b-row>
    </div> -->
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import CollapsibleTabs from '@/components/CollapsibleTabs.vue'
// import RescoreComp from '@/components/RescoreComp.vue'

export default {
  name: 'DeptUnit',
  components: {
    CollapsibleTabs,
    // RescoreComp,
  },
  setup() {
    const route = useRoute()

    // Access query parameters
    const sectionId = ref(null)
    onMounted(() => {
      sectionId.value = route.query.sectionId
    })

    return {
      sectionId,
    }
  },
  data() {
    return {
      expandedCritDetails: 0,
      units: [],
    }
  },
  mounted() {
    this.fetchUnitsData()
  },
  methods: {
    fetchUnitsData() {
      axios
        .get(`http://localhost:5000/api/data/section-units/${this.sectionId}`)
        .then((response) => {
          this.units = response.data
          this.unitNames = this.units.map((unit) => unit.unit_name)
          console.log(response.data)
        })
    },
  },
}
</script>

<style>
/* .home {
  align-items: center;
  padding: 0.5rem 2rem;
}
.main-header {
  margin: 2rem 10rem;
  text-align: left;
} */

.prog-bar {
  margin-top: 1rem;
  width: 20rem;
}

.main-page {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 2rem;
}

/* Ensure tabs scroll horizontally if they exceed container width */
.tab-scroll {
  display: flex;
  overflow-x: auto; /* Enable horizontal scrolling */
  white-space: nowrap; /* Prevent wrapping to multiple lines */
  flex-direction: row;
  flex-wrap: nowrap;
  white-space: nowrap;
  width: 100%;
}

/* Optional: Customize scrollbar appearance */
.tab-scroll::-webkit-scrollbar {
  height: 8px; /* Adjust scrollbar height */
}
.tab-scroll::-webkit-scrollbar-thumb {
  background-color: #c0c0c0; /* Customize scrollbar color */
  border-radius: 4px; /* Rounded corners */
}
.tab-scroll::-webkit-scrollbar-thumb:hover {
  background-color: #a0a0a0; /* Change color on hover */
}

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
</style>
