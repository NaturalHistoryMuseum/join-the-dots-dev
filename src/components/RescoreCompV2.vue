<template>
  <div class="unit-header">
    <h4 class="unit-link" @click="navigateUnit(unit.collection_unit_id)">{{ unit.unit_name }}</h4>
    <zoa-button class="complete-btn">Mark Unit Complete</zoa-button>
  </div>
  <RescoreAccordionComp
    :accordionId="0"
    :toggleAccordion="toggleAccordion"
    :expandedAccordion="expandedAccordion"
    header="Unit Measures / Comments"
    :category_cols="category_cols"
  >
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-md-6">
            <zoa-input
              zoa-type="number"
              label="No. of Curatorial Units"
              v-model="localUnit.curatorial_unit_count"
            />
          </div>
          <div class="col-md-6">
            <SelectComp
              :options="confidence_options"
              label="Confidence"
              help=""
              :multi="false"
              :value="localUnit.curatorial_unit_count_confidence"
            />
            <!-- <zoa-input
              zoa-type="dropdown"
              label="Confidence"
              v-model="localUnit.curatorial_unit_count_confidence"
            /> -->
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <zoa-input zoa-type="number" label="No. of Items" v-model="localUnit.item_count" />
          </div>
          <div class="col-md-6">
            <!-- <zoa-input
              zoa-type="dropdown"
              label="Confidence"
              v-model="localUnit.item_count_confidence"
            /> -->
            <SelectComp
              :options="confidence_options"
              label="Confidence"
              help=""
              :multi="false"
              :value="localUnit.item_count_confidence"
            />
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <zoa-input
              zoa-type="number"
              label="Barcode Percentage"
              v-model="localUnit.barcoded_percentage"
            />
          </div>
          <div class="col-md-6">
            <!-- <zoa-input
              zoa-type="dropdown"
              label="Confidence"
              v-model="localUnit.barcoded_percentage_confidence"
            /> -->
            <SelectComp
              :options="confidence_options"
              label="Confidence"
              help=""
              :multi="false"
              :value="localUnit.barcoded_percentage_confidence"
            />
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <zoa-input zoa-type="empty" label="Comments" class="comments-title" />
        <textarea class="text-area" rows="7" v-model="localUnit.unit_comment"></textarea>
      </div>
    </div>
  </RescoreAccordionComp>
  <div v-for="cat in categories" :key="cat.category_id">
    <div class="">
      <div class="">
        <RescoreAccordionComp
          :accordionId="cat.category_id"
          :toggleAccordion="toggleAccordion"
          :expandedAccordion="expandedAccordion"
          :header="cat.description"
          :category_cols="category_cols"
        >
          <div class="">
            <div
              v-for="crit in criterion.filter(
                (criteria) => criteria.category_id == cat.category_id,
              )"
              :key="crit.criterion_id"
            >
              <div class="criterion-row">
                <div class="criterion-title">
                  <CriterionDefModal :crit="crit" :unit="unit" />
                  <h6 class="criterion-name">{{ crit.criterion_name }}</h6>
                </div>
                <div
                  v-for="ranks in JSON.parse(unit.ranks_json).filter(
                    (rank) => rank.criterion_id == crit.criterion_id,
                  )"
                  :key="ranks.rank_id"
                  class="criterion-rank"
                >
                  <zoa-input
                    zoa-type="number"
                    :label="'Rank ' + ranks.rank_value"
                    v-model="ranks.percentage"
                  />
                </div>
              </div>
            </div>
          </div>
        </RescoreAccordionComp>
      </div>
    </div>
  </div>
</template>

<script>
import RescoreAccordionComp from './RescoreAccordionComp.vue'
import CriterionDefModal from './CriterionDefModal.vue'
import SelectComp from './SelectComp.vue'
import { getGeneric } from '@/services/dataService'

export default {
  name: 'DeptUnit',
  props: {
    unit: Object,
  },
  components: {
    RescoreAccordionComp,
    CriterionDefModal,
    SelectComp,
  },
  setup() {},
  data() {
    return {
      expandedAccordion: null,
      criterion: [],
      categories: [],
      category_cols: [
        { category_id: 0, col: '#f3f3f3' },
        { category_id: 1, col: '#290340' },
        { category_id: 2, col: '#24087d' },
        { category_id: 3, col: '#651604' },
        { category_id: 4, col: '#00ad00' },
      ],
      confidence_options: [
        { value: 'Precise', order: 0 },
        { value: 'High', order: 1 },
        { value: 'Medium', order: 2 },
        { value: 'Low', order: 3 },
      ],
      localUnit: { ...this.unit },
    }
  },
  watch: {
    unit: {
      handler(newVal) {
        this.localUnit = { ...newVal }
      },
      deep: true,
    },
  },
  mounted() {
    this.fetchCriterionData()
    this.fetchCategoryData()
  },
  methods: {
    fetchCriterionData() {
      getGeneric('criterion').then((response) => {
        this.criterion = response
      })
    },
    fetchCategoryData() {
      getGeneric('category').then((response) => {
        this.categories = response
      })
    },
    toggleAccordion(accord_id) {
      if (this.expandedAccordion === accord_id) {
        this.expandedAccordion = null
      } else {
        this.expandedAccordion = accord_id
      }
    },
    navigateUnit(unit_id) {
      this.$router.push({ path: '/view-unit', query: { unit_id: unit_id } })
    },
  },
  computed: {
    percentageValue: {
      get() {
        return this.ranks.percentage * 100 // Convert decimal to percentage
      },
      set(value) {
        this.ranks.percentage = value / 100 // Convert percentage back to decimal
      },
    },
  },
}
</script>

<style>
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

/* Zoe model */
.modal-btn {
  margin: auto;
  z-index: 10;
}

.text-area {
  width: 100%;
  height: 50%;
  border-radius: 10px;
  padding: 8px 16px;
}

.criterion-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 1rem;
}
.criterion-title {
  width: 25%;
  display: flex;
  align-items: center;
  justify-content: left;
  gap: 1rem;
}
.criterion-rank {
  width: 12%;
}
.criterion-name {
  margin: 0;
}

.unit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.unit-link {
  cursor: pointer;
  font-weight: bold;
  font-size: 1.5rem;
  text-decoration: underline 2px;
  margin: 0;
  flex: 1;
}

.unit-link:hover {
  color: #24087d;
  text-decoration: underline 3px;
}

.complete-btn {
  /* align-self: right; */
  margin-left: auto;
}
</style>
