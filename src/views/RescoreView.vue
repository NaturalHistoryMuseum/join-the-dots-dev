<template>
  <div class="rescore">
    <div class="main-header">
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

    <!-- <div v-if="units.length < 0">
      <div v-for="unit in units" :key="unit.unit_id">
        <h3>{{ unit.unit_name }}</h3>
        <p>{{ unit.unit_description }}</p>
      </div>
    </div>
    <div v-else>
      <zoa-tabs
        :class="string"
        :delay="delay"
        :active-position="activePosition"
        :initial-value="initialValue"
        :kind="kind"
        :options="unitNames"
        :size="size"
      />
    </div> -->
    <!-- <zoa-modal
      :kind="kind"
      :header="header"
      :message="message"
      :class="rootClass"
      :button-args="buttonArgs"
    /> -->

    <!-- <zoa-modal class="modal-btn">
      <template v-slot:button><i class="bi bi-info-circle"></i> Open Modal</template>
      <template v-slot:header>Header of model right???</template>
      <div class="flex flex-col gap-4">This is the body of the modal.</div>
    </zoa-modal> -->
    <div>
      <b-row class="wrap" ref="wrap">
        <b-tabs vertical card content-class="mt-3 tab-scroll">
          <b-tab v-for="unit in units" :key="unit.unit_id" :title="unit.unit_name" active>
            <div v-for="cat in categories" :key="cat.category_id">
              <div class="category-cont">
                <div
                  class="category-head"
                  :style="{ backgroundColor: category_cols[cat.category_id - 1].col }"
                >
                  <div class="category-txt">{{ cat.description }}</div>
                </div>

                <div class="crit-cont">
                  <div
                    v-for="crit in criterion.filter(
                      (criteria) => criteria.category_id == cat.category_id,
                    )"
                    :key="crit.criterion_id"
                  >
                    <div
                      class="criterion-cont"
                      :style="{
                        backgroundColor: category_cols[cat.category_id - 1].col + '40',
                      }"
                    >
                      <div class="criterion-txt">
                        <div class="criterion-name">
                          <button class="icon-btn" @click="toggleCritDetails(crit.criterion_id)">
                            <div v-if="expandedCritDetails == crit.criterion_id">
                              <i class="bi bi-chevron-up"></i>
                            </div>
                            <div v-else>
                              <i class="bi bi-chevron-down"></i>
                            </div>
                          </button>
                          {{ crit.criterion_name }}
                          <zoa-modal class="modal-btn">
                            <template v-slot:button><i class="bi bi-info-circle"></i></template>
                            <template v-slot:header> Defintions </template>
                            <div class="flex flex-col gap-4">
                              <div>
                                <p class="desc-title">{{ crit.criterion_name }}:</p>
                                <p>{{ crit.definition }}</p>
                                <div
                                  v-for="ranks in JSON.parse(unit.ranks_json).filter(
                                    (rank) => rank.criterion_id == crit.criterion_id,
                                  )"
                                  :key="ranks.rank_id"
                                >
                                  <p class="desc-title">{{ ranks.rank_value }}:</p>
                                  <p>{{ ranks.definition }}</p>
                                </div>
                              </div>
                            </div>
                          </zoa-modal>
                          <!-- <button class="icon-btn" @click="crit.criterion_id">
                            <i class="bi bi-info-circle"></i>
                          </button> -->
                        </div>
                        <transition name="fade">
                          <div
                            class="criterion-desc"
                            v-if="expandedCritDetails === crit.criterion_id"
                          >
                            <p class="desc-title">Definition:</p>
                            <p>{{ crit.definition }}</p>
                          </div>
                        </transition>
                      </div>
                      <div class="rank-cont">
                        <div
                          v-for="ranks in JSON.parse(unit.ranks_json).filter(
                            (rank) => rank.criterion_id == crit.criterion_id,
                          )"
                          :key="ranks.rank_id"
                        >
                          <div class="header-cont">rank - {{ ranks.rank_value }}</div>
                          <div class="percent-cont">
                            <input
                              type="number"
                              v-model="ranks.percentage"
                              :min="0"
                              :max="1"
                              :step="0.1"
                            />
                            <!-- {{ ranks.percentage }} -->
                            <!-- <zoa-input
                        zoa-type="number"
                        :class="rootClass"
                        :label="label"
                        :label-position="labelPosition"
                        :help="help"
                        :help-position="helpPosition"
                        :disabled="disabled"
                        :options="{ delay, placeholder, min, max, step }"
                      /> -->
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </b-tab>
        </b-tabs>
      </b-row>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'DeptUnit',
  setup() {
    const route = useRoute()

    // Access query parameters
    const sectionId = ref(null)
    //const section = ref(null)

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
      criterion: [],
      categories: [],
      category_cols: [
        { category_id: 1, col: '#4f2f4e' },
        { category_id: 2, col: '#0a458c' },
        { category_id: 3, col: '#580b09' },
        { category_id: 4, col: '#325948' },
      ],
    }
  },
  mounted() {
    this.fetchUnitsData()
    this.fetchCriterionData()
    this.fetchCategoryData()
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
    fetchCriterionData() {
      axios.get(`http://localhost:5000/api/data/criterion`).then((response) => {
        this.criterion = response.data

        console.log('criterion data : ', response.data)
      })
    },
    fetchCategoryData() {
      axios.get(`http://localhost:5000/api/data/category`).then((response) => {
        this.categories = response.data
        console.log('category data : ', response.data)
      })
    },
    toggleCritDetails(crit_id) {
      if (this.expandedCritDetails === crit_id) {
        this.expandedCritDetails = 0
      } else {
        this.expandedCritDetails = crit_id
      }
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

.category-cont {
  display: flex;
  flex-direction: row;
  justify-content: center;
  /* gap: 1rem; */
}

.category-head {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
}
.category-txt {
  transform: rotate(-90deg);
  color: white;
  white-space: nowrap;
}

.criterion-cont {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  /* border-color: black;
  border-style: solid;
  border-width: 1px; */
  border-top: 1px solid white;
  padding: 0 1rem;
}

.criterion-txt {
  display: flex;
  align-items: start;
  justify-content: center;
  flex-direction: column;
  word-wrap: break-word;
  white-space: normal;
  margin: 0.5rem;
  width: 20rem;
  text-align: left;
}

.criterion-name {
  font-weight: bold;
}

.criterion-desc {
  font-size: small;
}

.desc-title {
  font-weight: bold;
  margin-bottom: 0;
  margin-top: 0.3rem;
}
.rank-cont {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  padding: 0.5rem 0;
}

/* .header-cont {
} */

/* Handle transition of ciretion details */
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.3s ease,
    max-height 0.3s ease;
  overflow: hidden;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
}

.wrap {
  overflow: hidden;
  width: 100%;
  flex-direction: row;
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

/* Zoe model */
.modal-btn {
  margin: auto;
  z-index: 10;
}
</style>
