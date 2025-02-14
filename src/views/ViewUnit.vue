<template>
  <div class="main-page">
    <div class="main-header">
      <h1>View Unit</h1>
      <p>Unit ID: {{ unitId }}</p>
      <p>Collection: {{ collection }}</p>
      <p>unit: {{ unit }}</p>
      <TopTabs :unit="unit[0]" />
      <!-- <p>Section: {{ section }}</p> -->
    </div>
  </div>
</template>

<style>
/* .home {
  align-items: center;
  padding: 0.5rem 2rem;
}
.main-header {
  margin: 2rem 10rem;
  text-align: left;
} */
</style>

<script>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
// import axios from 'axios'
import TopTabs from '@/components/TopTabs.vue'
import { getGeneric } from '@/services/dataService'

export default {
  name: 'ViewUnit',
  components: {
    TopTabs,
  },
  setup() {
    const route = useRoute()

    // Access query parameters
    const unitId = ref(null)
    const collection = ref(null)
    //const section = ref(null)

    onMounted(() => {
      unitId.value = route.query.unit_id
      collection.value = route.query.collection
      //section.value = route.query.section
    })

    return {
      unitId,
      collection,
      //section,
    }
  },
  data() {
    return {
      unit: [],
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      this.unit = await getGeneric(`full-unit/${this.unitId}`)
    },
  },
}
</script>
