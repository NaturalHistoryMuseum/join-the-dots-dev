<template>
  <div v-if="rescore" class="unit-header">
    <h4 class="unit-link" @click="navigateUnit(unit.collection_unit_id)">{{ unit.unit_name }}</h4>
    <zoa-button class="complete-btn" @click="changeCatComplete([0, 1, 2, 3, 4], 1)"
      >Mark Unit Complete</zoa-button
    >
  </div>
  <div class="date-title">Last Edited: {{ overallDate() }}</div>
  <RescoreAccordionComp
    :accordionId="0"
    :toggleAccordion="toggleAccordion"
    :expandedAccordion="expandedAccordion"
    header="Unit Measures / Comments"
    :category_cols="category_cols"
    :rescore="rescore"
    :complete="rescore ? checkCatComplete({ category_id: 0 }) : false"
    :changeCatComplete="() => changeCatComplete([0])"
  >
    <div class="date-title">Last Edited: {{ metricDate() }}</div>

    <div class="row">
      <div class="col-md-6">
        <div v-for="metric in JSON.parse(unit.metric_json)" :key="metric.collection_unit_metric_id">
          <div class="row">
            <div class="col-md-6">
              <zoa-input
                zoa-type="number"
                :label="fieldNameCalc(metric.metric_name)"
                v-model="metric.metric_value"
              />
            </div>
            <div class="col-md-6">
              <SelectComp
                :options="confidence_options"
                label="Confidence"
                help=""
                :multi="false"
                :value="metric.confidence_level"
              />
            </div>
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
          :rescore="rescore"
          :complete="rescore ? checkCatComplete(cat) : false"
          :changeCatComplete="() => changeCatComplete([cat.category_id])"
        >
          <div class="">
            <div class="date-title">Last Edited: {{ groupCategoryDate(cat) }}</div>

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
                  <!-- <zoa-input
                    zoa-type="number"
                    :label="'Rank ' + ranks.rank_value"
                    v-model="ranks.percentage"
                  /> -->
                  <PercentageInput
                    v-model="ranks.percentage"
                    :label="`Rank ${ranks.rank_value} (%)`"
                  />

                  <!-- {{ ranks.comment }} -->
                </div>
              </div>

              <div class="row">
                <div class="show-comments" @click="showCriterionComments(crit.criterion_id)">
                  <div v-if="expanded_criterion_comment == crit.criterion_id" class="show-comments">
                    <i class="bi bi-chevron-up"></i> {{ commentsTitle(crit.criterion_id) }}
                  </div>
                  <div v-else class="show-comments">
                    <i class="bi bi-chevron-down"></i> {{ commentsTitle(crit.criterion_id) }}
                  </div>
                </div>
                <transition name="fade">
                  <div v-if="expanded_criterion_comment == crit.criterion_id" class="row">
                    <div class="col-md-10">
                      <div
                        v-for="rank in JSON.parse(unit.ranks_json).filter(
                          (rank) => rank.criterion_id == crit.criterion_id && rank.comment !== null,
                        )"
                        :key="rank.rank_id"
                      >
                        <div class="">
                          <p class="view-field">Rank {{ rank.rank_value }} - {{ rank.comment }}</p>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-2 edit-comments">
                      <EditCommentsModal :crit="crit" :unit="unit" />
                    </div>
                  </div>
                </transition>
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
import { completeCats, getGeneric } from '@/services/dataService'
import fieldNameCalc from '@/utils/utils'
import EditCommentsModal from './EditCommentsModal.vue'
import PercentageInput from './PercentageInput.vue'

export default {
  name: 'DeptUnit',
  props: {
    unit: Object,
    rescore: Boolean,
    fetchUnitsData: Function,
  },
  components: {
    RescoreAccordionComp,
    CriterionDefModal,
    SelectComp,
    EditCommentsModal,
    PercentageInput,
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
      expanded_criterion_comment: null,
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
    fieldNameCalc,
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
    groupCategoryDate(category) {
      if (!this.unit) return null
      const ranks_json = JSON.parse(this.unit.ranks_json)

      const filteredCriterion = this.criterion.filter(
        (criterion) => criterion.category_id == category.category_id,
      )
      const criterionArr = filteredCriterion.map((criterion) => criterion.criterion_id)

      const ranks = ranks_json.filter((rank) => criterionArr.includes(rank.criterion_id))
      let latestDate = null
      ranks.forEach((rank) => {
        const date = new Date(rank.date_assessed)
        if (!latestDate || date > latestDate) {
          latestDate = date
        }
      })
      if (!latestDate) return null
      let finalDate = latestDate.toISOString().split('T')[0]
      return finalDate
    },
    metricDate() {
      if (!this.unit) return null
      const comment_date = this.unit.unit_comment_date_added
      const metric_json = JSON.parse(this.unit.metric_json)
      let latestDate = null
      metric_json.forEach((metric) => {
        const date = new Date(metric.date_from)
        if (!latestDate || date > latestDate) {
          latestDate = date
        }
      })
      if (!latestDate || comment_date > latestDate) {
        latestDate = comment_date
      }
      const finalDate = latestDate.toISOString().split('T')[0]
      return finalDate
    },
    overallDate() {
      if (!this.categories.length > 0) return
      const metricDate = this.metricDate()
      let latestDate = null
      this.categories.forEach((cat) => {
        const catDate = this.groupCategoryDate(cat)
        if (catDate && (!latestDate || catDate > latestDate)) {
          latestDate = catDate
        }
      })
      if (!latestDate || metricDate > latestDate) {
        latestDate = metricDate
      }
      return latestDate
    },
    showCriterionComments(criterion_id) {
      if (this.expanded_criterion_comment === criterion_id) {
        this.expanded_criterion_comment = null
      } else {
        this.expanded_criterion_comment = criterion_id
      }
    },
    commentsTitle(criterion_id) {
      const ranks_comments = JSON.parse(this.unit.ranks_json).filter(
        (rank) =>
          rank.criterion_id == criterion_id && rank.comment !== null && rank.comment.length > 0,
      )
      if (ranks_comments.length == 0) {
        return 'Add comments'
      }
      return `Show comments (${ranks_comments.length})`
    },
    checkCatComplete(cat) {
      const category_tracking = JSON.parse(this.localUnit.category_tracking)
      const category = category_tracking.filter((category) => {
        return category.category_id == cat.category_id
      })
      if (category.length > 0) {
        return category[0].complete == 1
      }
    },
    changeCatComplete(category_ids_arr, new_val = null) {
      let submit_change = false
      let val = null
      const category_tracking = JSON.parse(this.unit.category_tracking)
      category_tracking.forEach((category) => {
        if (category_ids_arr.includes(category.category_id)) {
          if (new_val != null) {
            category.complete = new_val
            val = new_val
          } else {
            category.complete = category.complete == 1 ? 0 : 1
            val = category.complete
          }
          submit_change = true
        }
      })
      if (submit_change) {
        completeCats(this.unit.rescore_session_units_id, category_ids_arr, val).then(() => {
          this.fetchUnitsData()
        })
      }
      this.localUnit.category_tracking = JSON.stringify(category_tracking)
    },
  },
  computed: {},
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

.date-title {
  text-align: right;
  margin-top: 1rem;
}

.view-field {
  margin: 0 1.5rem;
  /* height: 1rem; */
}

.show-comments {
  cursor: pointer;
  margin: 0.25rem 0;
}

.edit-comments {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
