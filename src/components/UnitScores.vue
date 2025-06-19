<template>
  <div v-if="rescore && !bulk_edit" class="unit-header">
    <!-- Unit Tile and link to unit -->
    <div class="unit-link-container">
      <h4 class="unit-link" @click="navigateUnit(unit.collection_unit_id)">
        {{ unit.unit_name }}
      </h4>
    </div>
    <!-- Button for managing whole units complete status -->
    <zoa-button
      class="complete-btn"
      @click="changeCatComplete([0, 1, 2, 3, 4], 1)"
    >
      Mark Unit Complete
    </zoa-button>
  </div>
  <!-- Date the whole unit was last edited -->
  <div v-if="!bulk_edit" class="date-title">
    Last Edited: {{ overallDate() }}
  </div>
  <!-- Accordion for the Metrics and Comments -->
  <RescoreAccordionComp
    :accordion_id="0"
    :toggleAccordion="toggleAccordion"
    :expanded_accordion="expanded_accordion"
    header="Unit Measures / Unit Comment"
    :category_cols="category_cols"
    :rescore="rescore && !bulk_edit"
    :complete="
      rescore && !bulk_edit ? checkCatComplete({ category_id: 0 }) : false
    "
    :changeCatComplete="() => changeCatComplete([0])"
  >
    <div v-if="!bulk_edit" class="date-title">
      Last Edited: {{ metricDate() }}
    </div>
    <!-- Metrics Section -->
    <div class="row">
      <!-- Loop through each metric -->
      <div class="col-md-6" v-if="metric_definitions.length > 0">
        <div
          v-for="metric in metric_definitions"
          :key="metric.collection_unit_metric_definition_id"
        >
          <!-- Add each metrics value field and confidence field -->
          <div class="row">
            <div class="col-md-6">
              <zoa-input
                zoa-type="number"
                :label="fieldNameCalc(metric.metric_name)"
                v-model="metric.metric_value"
                @change="
                  submitMetricsChanges(
                    metric.collection_unit_metric_definition_id,
                  )
                "
              />
            </div>
            <div class="col-md-6 mb-2">
              <zoa-input
                zoa-type="dropdown"
                label="Confidence"
                label-position="above"
                @change="
                  submitMetricsChanges(
                    metric.collection_unit_metric_definition_id,
                  )
                "
                :config="{
                  options: confidence_options,
                  itemName: 'value',
                  itemNamePlural: 'data',
                  enableSearch: true,
                }"
                v-model="metric.confidence_level"
              />
            </div>
          </div>
          <!-- Show saved message if metric came from drafts -->
          <SmallMessages
            v-if="metric.is_draft && !bulk_edit"
            message_text="Change Saved"
            message_type="success"
          />
        </div>
      </div>
      <!-- Unit Comments -->
      <div class="col-md-6">
        <zoa-input
          zoa-type="empty"
          label="Unit Comment"
          class="comments-title"
        />
        <textarea
          class="text-area"
          rows="7"
          v-model="local_unit.unit_comment"
          @change="handleCommentChange"
        ></textarea>
        <!-- Saved message if comment is in drafts -->
        <SmallMessages
          message_text="Change Saved"
          message_type="success"
          v-if="local_unit.unit_comment_is_draft && !bulk_edit"
        />
      </div>
    </div>
  </RescoreAccordionComp>
  <!-- Loop through each category and display an accordion for each one -->
  <div v-for="cat in categories" :key="cat.category_id">
    <RescoreAccordionComp
      :accordion_id="cat.category_id"
      :toggleAccordion="toggleAccordion"
      :expanded_accordion="expanded_accordion"
      :header="cat.description"
      :category_cols="category_cols"
      :rescore="rescore && !bulk_edit"
      :complete="rescore && !bulk_edit ? checkCatComplete(cat) : false"
      :changeCatComplete="() => changeCatComplete([cat.category_id])"
    >
      <div class="">
        <!-- last edited date for this whole category -->
        <div v-if="!bulk_edit" class="date-title">
          Last Edited: {{ groupCategoryDate(cat) }}
        </div>
        <!-- Loop through each criterion in the category -->
        <div
          v-for="crit in criterion.filter(
            (criteria) => criteria.category_id == cat.category_id,
          )"
          :key="crit.criterion_id"
        >
          <div class="criterion-row">
            <div class="criterion-title">
              <!-- Modal pop up for the criteria with its info -->
              <CriterionDefModal :crit="crit" :unit="unit" />
              <!-- Criterion Title -->
              <h6 class="criterion-name">
                {{ crit.criterion_name.split('/').join(' / ') }}
              </h6>
            </div>
            <!-- Loop through each rank in the criterion -->
            <div
              v-for="rank in editedRanks[crit.criterion_id]"
              :key="rank.rank_id"
              class="criterion-rank"
            >
              <!-- Allow for percentage input for this rank -->
              <PercentageInput
                v-if="rescore"
                v-model="rank.percentage"
                :label="`Rank ${rank.rank_value} (%)`"
                :error="checkErrors(crit.criterion_id)"
                :submit="submitRankChanges"
                :rank="rank"
                :ranks="editedRanks[crit.criterion_id]"
                :criterion_id="crit.criterion_id"
              />
              <div v-else>
                <!-- Display the rank value and percentage -->
                <p>{{ `Rank ${rank.rank_value} (%)` }}</p>
                <p>{{ rank.percentage ? rank.percentage * 100 : '0' }}</p>
              </div>
            </div>
            <!-- {{
              // FOR TESTING PURPOSES ONLY
              editedRanks[crit.criterion_id].reduce((sum, r) => sum + (r.percentage || 0), 0)
            }} -->
          </div>
          <!-- Container for other criterion interations -->
          <div class="row">
            <!-- Show comments asigned to ranks in this criterion -->
            <div class="show-comments">
              <div
                v-if="expanded_criterion_comment == crit.criterion_id"
                class="show-comments"
              >
                <div @click="showCriterionComments(crit.criterion_id)">
                  <i class="bi bi-chevron-up"></i>
                  {{ commentsTitle(crit.criterion_id) }}
                </div>
                <!-- Show warnings / Messages -->
                <RanksWarnings
                  :criterion_id="crit.criterion_id"
                  :editedRanks="editedRanks"
                  :ranks="ranks"
                  :checkEdited="checkEdited"
                  :checkErrors="checkErrors"
                />
              </div>
              <div v-else class="show-comments">
                <!-- Show comments asigned to ranks in this criterion -->
                <div @click="showCriterionComments(crit.criterion_id)">
                  <i class="bi bi-chevron-down"></i>
                  {{ commentsTitle(crit.criterion_id) }}
                </div>
                <!-- Show warnings / Messages -->
                <RanksWarnings
                  :criterion_id="crit.criterion_id"
                  :editedRanks="editedRanks"
                  :ranks="ranks"
                  :checkEdited="checkEdited"
                  :checkErrors="checkErrors"
                />
              </div>
            </div>
            <!-- Pop out of the comments -->
            <transition name="fade">
              <div
                v-if="expanded_criterion_comment == crit.criterion_id"
                class="row comments-list"
              >
                <div class="col-md-10">
                  <!-- Only show the ranks with comments assigned to them -->
                  <div
                    v-for="rank in editedRanks[crit.criterion_id].filter(
                      (rank) => rank.comment !== null,
                    )"
                    :key="rank.rank_id"
                  >
                    <!-- Display comment -->
                    <div class="">
                      <p class="view-comment">
                        Rank {{ rank.rank_value }} - {{ rank.comment }}
                      </p>
                    </div>
                  </div>
                </div>
                <div
                  class="col-md-2 edit-comments"
                  v-if="rescore && !bulk_edit"
                >
                  <!-- Modal pop out to edit the comments for each rank in this criterion -->
                  <EditCommentsModal
                    v-if="rescore && !bulk_edit"
                    :criterion_id="crit.criterion_id"
                    :ranks="editedRanks[crit.criterion_id]"
                    :submit="submitRankChanges"
                  />
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </RescoreAccordionComp>
  </div>
</template>

<script>
import {
  completeCats,
  getGeneric,
  submitDataGeneric,
  submitDraftRrank,
} from '@/services/dataService';
import fieldNameCalc from '@/utils/utils';
import CriterionDefModal from './CriterionDefModal.vue';
import EditCommentsModal from './EditCommentsModal.vue';
import PercentageInput from './PercentageInput.vue';
import RanksWarnings from './RanksWarnings.vue';
import RescoreAccordionComp from './RescoreAccordionComp.vue';
import SmallMessages from './SmallMessages.vue';

export default {
  name: 'UnitScores',
  props: {
    unit: Object,
    rescore: Boolean,
    bulk_edit: Boolean,
    fetchUnitsData: Function,
  },
  components: {
    RescoreAccordionComp,
    CriterionDefModal,
    EditCommentsModal,
    PercentageInput,
    RanksWarnings,
    SmallMessages,
  },
  setup() {},
  data() {
    return {
      expanded_accordion: null,
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
      local_unit: { ...this.unit },
      expanded_criterion_comment: null,
      ranks: this.unit.ranks_json,
      editedRanks: {},
      metric_definitions: [],
    };
  },
  watch: {
    unit: {
      immediate: true,
      handler(newVal) {
        this.local_unit = { ...newVal };
        this.initializeEditedRanks(newVal);
        this.fetchMetrics();
        this.expanded_accordion = null;
      },
      deep: true,
    },
  },
  mounted() {
    this.fetchCriterionData();
    this.fetchCategoryData();
    // this.fetchMetrics()
  },
  methods: {
    fieldNameCalc,
    fetchCriterionData() {
      getGeneric('criterion').then((response) => {
        this.criterion = response;
      });
    },
    fetchCategoryData() {
      getGeneric('category').then((response) => {
        this.categories = response;
      });
    },
    fetchMetrics() {
      if (this.local_unit.metric_json) {
        getGeneric('metric-definitions').then((response) => {
          this.metric_definitions = response.map((metric) => {
            const this_metric = this.local_unit.metric_json.find(
              (met) =>
                metric.collection_unit_metric_definition_id ==
                met.collection_unit_metric_definition_id,
            ) || { metric_value: null, confidence_level: null };
            return {
              ...metric,
              metric_value: this_metric.metric_value,
              confidence_level: this_metric.confidence_level,
              is_draft: this_metric.is_draft || false,
            };
          });
        });
      }
    },
    toggleAccordion(accord_id) {
      if (this.expanded_accordion === accord_id) {
        this.expanded_accordion = null;
      } else {
        this.expanded_accordion = accord_id;
      }
    },
    navigateUnit(unit_id) {
      this.$router.push({ path: '/view-unit', query: { unit_id: unit_id } });
    },
    groupCategoryDate(category) {
      if (!this.unit) return null;
      const ranks_json = this.ranks;

      const filteredCriterion = this.criterion.filter(
        (criterion) => criterion.category_id == category.category_id,
      );
      const criterionArr = filteredCriterion.map(
        (criterion) => criterion.criterion_id,
      );

      const ranks = ranks_json.filter((rank) =>
        criterionArr.includes(rank.criterion_id),
      );
      let latestDate = null;
      ranks.forEach((rank) => {
        const date = new Date(rank.date_assessed);
        if (!latestDate || date > latestDate) {
          latestDate = date;
        }
      });
      if (!latestDate) return null;
      let finalDate = latestDate.toISOString().split('T')[0];
      return finalDate;
    },
    metricDate() {
      if (!this.unit) return null;
      const comment_date = this.unit.unit_comment_date_added;
      const metric_json = this.unit.metric_json;
      let latestDate = null;
      metric_json.forEach((metric) => {
        const date = new Date(metric.date_from);
        if (!latestDate || date > latestDate) {
          latestDate = date;
        }
      });
      if (!latestDate || comment_date > latestDate) {
        latestDate = comment_date;
      }
      if (!latestDate) return null;
      const finalDate = latestDate.toISOString().split('T')[0];
      return finalDate;
    },
    overallDate() {
      if (!this.categories.length > 0) return;
      const metricDate = this.metricDate();
      let latestDate = null;
      this.categories.forEach((cat) => {
        const catDate = this.groupCategoryDate(cat);
        if (catDate && (!latestDate || catDate > latestDate)) {
          latestDate = catDate;
        }
      });
      if (!latestDate || metricDate > latestDate) {
        latestDate = metricDate;
      }
      return latestDate;
    },
    showCriterionComments(criterion_id) {
      if (this.expanded_criterion_comment === criterion_id) {
        this.expanded_criterion_comment = null;
      } else {
        this.expanded_criterion_comment = criterion_id;
      }
    },
    commentsTitle(criterion_id) {
      if (this.editedRanks) {
        const ranks_comments = this.editedRanks[criterion_id].filter(
          (rank) =>
            rank.criterion_id == criterion_id &&
            rank.comment !== null &&
            rank.comment.length > 0,
        );
        if (ranks_comments.length == 0) {
          return 'Add comments';
        }
        return `Show comments (${ranks_comments.length})`;
      }
    },
    checkCatComplete(cat) {
      const category_tracking = this.local_unit.category_tracking;
      const category = category_tracking.filter((category) => {
        return category.category_id == cat.category_id;
      });
      if (category.length > 0) {
        return category[0].complete == 1;
      }
    },
    changeCatComplete(category_ids_arr, new_val = null) {
      let submit_change = false;
      let val = null;
      const category_tracking = this.unit.category_tracking;
      category_tracking.forEach((category) => {
        if (category_ids_arr.includes(category.category_id)) {
          if (new_val != null) {
            category.complete = new_val;
            val = new_val;
          } else {
            category.complete = category.complete == 1 ? 0 : 1;
            val = category.complete;
          }
          submit_change = true;
        }
      });
      if (submit_change) {
        completeCats(
          this.unit.rescore_session_units_id,
          category_ids_arr,
          val,
        ).then(() => {
          this.fetchUnitsData();
        });
      }
      this.local_unit.category_tracking = JSON.stringify(category_tracking);
    },

    submitMetricsChanges(collection_unit_metric_definition_id) {
      if (this.bulk_edit) {
        const currentMetric = this.metric_definitions.find(
          (metric) =>
            metric.collection_unit_metric_definition_id ==
            collection_unit_metric_definition_id,
        );
        if (
          currentMetric.metric_value == null ||
          currentMetric.confidence_level == null
        )
          return;
        this.metric_definitions.find(
          (metric) =>
            metric.collection_unit_metric_definition_id ==
            collection_unit_metric_definition_id,
        ).is_draft = true;
        this.returnBulkEdit();
      } else {
        submitDataGeneric('submit-draft-metrics', {
          rescore_session_units_id: this.unit.rescore_session_units_id,
          collection_unit_id: this.unit.collection_unit_id,
          metric_json: this.metric_definitions.filter(
            (metric) =>
              metric.collection_unit_metric_definition_id ==
              collection_unit_metric_definition_id,
          ),
        }).then(() => {
          // Fetch the updated data after submitting the metrics changes
          this.fetchUnitsData();
        });
      }
    },
    returnBulkEdit() {
      this.$emit('newUnit', {
        ...this.local_unit,
        metric_json: this.metric_definitions.filter(
          (metric) => metric.is_draft,
        ),
        ranks_json: this.getEditedRanksPerGroups(),
      });
    },

    submitRankChanges(ranks, criterion_id) {
      if (this.bulk_edit) {
        this.returnBulkEdit();
      } else {
        // Check if there are any errors before submitting
        const errors = this.checkErrors(criterion_id);
        if (errors.length > 0) {
          // If there are errors, do not submit
          return;
        } else {
          // If no errors, proceed to submit the rank changes
          const category_draft_id = this.getCatDraftId(criterion_id);
          const rank_draft = {
            rescore_session_units_id: this.unit.rescore_session_units_id,
            collection_unit_id: this.unit.collection_unit_id,
            criterion_id: criterion_id,
            category_draft_id: category_draft_id,
            ranks: ranks.map((rank) => ({
              rank_id: rank.rank_id,
              percentage: rank.percentage || 0,
              comment: rank.comment || null,
            })),
          };
          submitDraftRrank(rank_draft).then(() => {
            // Fetch the updated data after submitting the rank changes
            this.fetchUnitsData();
          });
        }
      }
    },
    getEditedRanksPerGroups() {
      // Get only the ranks that have been edited
      let new_ranks = [];
      for (const value of Object.entries(this.editedRanks)) {
        const criterion = value[1];
        const percentage_total = criterion.reduce(
          (sum, r) => sum + (r.percentage || 0),
          0,
        );
        if (percentage_total == 1) {
          let temp_ranks = criterion.map((rank) => ({
            ...rank,
            criterion_name: this.criterion.find(
              (c) => c.criterion_id === rank.criterion_id,
            ).criterion_name,
            category_id: this.criterion.find(
              (c) => c.criterion_id === rank.criterion_id,
            ).category_id,
          }));
          new_ranks.push(temp_ranks);
        }
      }
      return new_ranks;
    },
    getCatDraftId(criterion_id) {
      const category_tracking = this.unit.category_tracking;
      // Find the category for the criterion
      const category = category_tracking.find(
        (cat) =>
          cat.category_id ===
          this.criterion.find((c) => c.criterion_id === criterion_id)
            .category_id,
      );
      return category.category_draft_id;
    },
    // Function to check for errors in ranks
    checkErrors(criterion_id) {
      const errors = [];
      // const ranks_filtered = this.getRanksByCriterion(criterion_id)
      const ranks_filtered = this.editedRanks[criterion_id] || [];
      // Check if there are any ranks with errors
      if (ranks_filtered.some((r) => r.percentage < 0)) {
        errors.push({
          message: 'Percentage must be between 0 and 100',
          type: 'error',
        });
      }
      const percentage_total = ranks_filtered.reduce(
        (sum, r) => sum + (r.percentage || 0),
        0,
      );
      // Check if the total percentage exceeds 100%
      if (percentage_total > 1) {
        errors.push({
          message: 'Total percentage exceeds 100%',
          type: 'error',
        });
      } else if (percentage_total < 1) {
        errors.push({
          message: 'Total percentage is less than 100%',
          type: 'warning',
        });
      }
      return errors;
    },
    checkEdited(ranks) {
      // Check if any rank has been edited
      return ranks.some((rank) => rank.is_draft);
    },
    initializeEditedRanks(unit) {
      const ranks = unit.ranks_json;
      const grouped = {};
      if (!ranks || ranks.length === 0) {
        this.editedRanks = {};
        return;
      }
      if (ranks && !Array.isArray(ranks) && typeof ranks === 'object') {
        this.editedRanks = ranks;
        return;
      }
      ranks.forEach((rank) => {
        if (!grouped[rank.criterion_id]) grouped[rank.criterion_id] = [];
        grouped[rank.criterion_id].push({ ...rank }); // make a copy
      });

      this.editedRanks = grouped;
    },
    handleCommentChange() {
      if (this.bulk_edit) {
        this.returnBulkEdit();
      } else {
        submitDataGeneric('submit-draft-comment', {
          rescore_session_units_id: this.unit.rescore_session_units_id,
          unit_comment: this.local_unit.unit_comment,
        }).then(() => {
          // Fetch the updated data after submitting the comment changes
          this.fetchUnitsData();
        });
      }
    },
  },
  computed: {},
};
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
  padding: 0.5rem 0rem;
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
  font-weight: bold;
}

.unit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.unit-link-container {
  display: flex;
  justify-content: center;
  width: 80%;
}

.unit-link {
  cursor: pointer;
  font-weight: bold;
  font-size: 1.5rem;
  text-decoration: underline 2px;
  margin: 0;
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

.view-comment {
  margin: 0 1.5rem;
}

.show-comments {
  cursor: pointer;
  margin: 0.25rem 0;
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.edit-comments {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
