<template>
  <div v-if="rescore && !bulk_edit" class="unit-header">
    <!-- Unit Tile and link to unit -->
    <div class="unit-link-container">
      <p
        class="h4-style unit-link"
        @click="navigateUnit(unit.collection_unit_id)"
      >
        {{ unit.unit_name }}
      </p>
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
      Last Edited: {{ metricDate() ? metricDate() : 'No Data' }}
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
              <div class="required-tag">*</div>
              <zoa-input
                v-if="rescore"
                zoa-type="number"
                :label="
                  fieldNameCalc(metric.metric_name) +
                  (metric.metric_units == '%'
                    ? ' (' + metric.metric_units + ')'
                    : '')
                "
                v-model="metric.metric_value"
                @change="
                  submitMetricsChanges(
                    metric.collection_unit_metric_definition_id,
                  )
                "
                :config="{ min: 0, step: 'any' }"
              />
              <div v-else>
                <!-- Display the metric name and value -->
                <zoa-input
                  zoa-type="empty"
                  :label="fieldNameCalc(metric.metric_name)"
                  class="comments-title"
                />
                <p class="view-field">{{ metric.metric_value }}</p>
              </div>
            </div>
            <div class="col-md-6 mb-2">
              <div class="required-tag">*</div>
              <zoa-input
                v-if="rescore"
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
              <div v-else>
                <!-- Display the confidence value -->
                <zoa-input
                  zoa-type="empty"
                  label="Confidence"
                  class="comments-title"
                />
                <p class="view-field">{{ metric.confidence_level }}</p>
              </div>
            </div>
          </div>
          <!-- Show message if errors -->
          <SmallMessages
            v-if="
              metric.metric_units == '%' &&
              metric.metric_value != null &&
              metric.metric_value < 0
            "
            message_text="Total percentage is less than 100%"
            message_type="error"
          />
          <SmallMessages
            v-if="
              metric.metric_units == '%' &&
              metric.metric_value != null &&
              metric.metric_value > 100
            "
            message_text="Total percentage exceeds 100%"
            message_type="error"
          />
          <!-- Show saved message if metric came from drafts -->
          <SmallMessages
            v-if="
              metric.is_draft &&
              !bulk_edit &&
              !(
                metric.metric_units == '%' &&
                metric.metric_value != null &&
                metric.metric_value > 100
              )
            "
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
          v-if="rescore"
          class="text-area"
          id="Unit Comment"
          aria-label="Unit Comment"
          rows="7"
          v-model="local_unit.unit_comment"
          @change="handleCommentChange"
        ></textarea>
        <div v-else>
          <p class="view-field">{{ local_unit.unit_comment }}</p>
        </div>
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
      :error="
        rescore && !bulk_edit ? checkCategoryErrors(cat.category_id) : false
      "
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
              <p class="criterion-name">
                {{ crit.criterion_code }} -
                {{ crit.criterion_name.split('/').join(' / ') }}
              </p>
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
                :error="bulk_edit ? [] : checkErrors(crit.criterion_id)"
                :submit="submitRankChanges"
                :rank="rank"
                :ranks="editedRanks[crit.criterion_id]"
                :criterion_id="crit.criterion_id"
              />
              <div v-else>
                <!-- Display the rank value and percentage -->
                <zoa-input
                  zoa-type="empty"
                  :label="`Rank ${rank.rank_value} (%)`"
                  class="comments-title"
                />
                <p class="view-field">
                  <!-- Only show where there are scores -->
                  <strong>{{
                    rank.percentage
                      ? parseFloat((rank.percentage * 100).toFixed(2))
                      : ''
                  }}</strong>
                </p>
              </div>
            </div>
            <!-- {{
              // FOR TESTING PURPOSES ONLY
              editedRanks[crit.criterion_id].reduce((sum, r) => sum + (r.percentage || 0), 0)
            }} -->
          </div>
          <!-- Container for other criterion interations -->
          <div
            class="row"
            v-if="rescore || countCriterionComments(crit.criterion_id) > 0"
          >
            <!-- Show comments asigned to ranks in this criterion -->
            <div>
              <div
                v-if="expanded_criterion_comment == crit.criterion_id"
                class="show-comments"
              >
                <div
                  class="pointer"
                  @click="showCriterionComments(crit.criterion_id)"
                >
                  <i class="bi bi-chevron-up"></i>
                  {{ commentsTitle(crit.criterion_id) }}
                </div>
                <!-- Show warnings / Messages -->
                <RanksWarnings
                  v-if="
                    (bulk_edit &&
                      editedRanks[crit.criterion_id].reduce(
                        (sum, r) => sum + (r.percentage || 0),
                        0,
                      ) > 0) ||
                    !bulk_edit
                  "
                  :criterion_id="crit.criterion_id"
                  :editedRanks="editedRanks"
                  :ranks="ranks"
                  :checkEdited="checkEdited"
                  :checkErrors="checkErrors"
                  :show_success="!bulk_edit"
                />
              </div>
              <div v-else class="show-comments">
                <!-- Show comments asigned to ranks in this criterion -->
                <div
                  class="pointer"
                  @click="showCriterionComments(crit.criterion_id)"
                >
                  <i class="bi bi-chevron-down"></i>
                  {{ commentsTitle(crit.criterion_id) }}
                </div>
                <!-- Show warnings / Messages -->
                <RanksWarnings
                  v-if="
                    (bulk_edit &&
                      editedRanks[crit.criterion_id].reduce(
                        (sum, r) => sum + (r.percentage || 0),
                        0,
                      ) > 0) ||
                    !bulk_edit
                  "
                  :criterion_id="crit.criterion_id"
                  :editedRanks="editedRanks"
                  :ranks="ranks"
                  :checkEdited="checkEdited"
                  :checkErrors="checkErrors"
                  :show_success="!bulk_edit"
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
                    :criterion_name="`${crit.criterion_code}: ${crit.criterion_name.split('/').join(' / ')}`"
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
import CriterionDefModal from './modals/CriterionDefModal.vue';
import EditCommentsModal from './modals/EditCommentsModal.vue';
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
      metrics: [],
      saving_criterion_id: 0,
    };
  },
  watch: {
    unit: {
      immediate: true,
      handler(new_val, old_val) {
        const currentAccordion = this.expanded_accordion;
        this.local_unit = { ...new_val };
        if (this.metrics.length > 0) {
          this.mapMetricsToUnit();
        }
        // Only reinitialize if ranks_json changed
        if (
          !old_val ||
          JSON.stringify(new_val.ranks_json) !==
            JSON.stringify(old_val.ranks_json)
        ) {
          this.initializeEditedRanks(new_val);
        }
        // Keep accordion open on unit change
        this.expanded_accordion = currentAccordion;
      },
      deep: true,
    },
  },
  mounted() {
    this.fetchCriterionData();
    this.fetchCategoryData();
    this.fetchMetrics();
    if (!this.editedRanks || Object.keys(this.editedRanks).length === 0) {
      this.initializeEditedRanks(this.unit);
    }
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
          this.metrics = response;
          this.mapMetricsToUnit();
        });
      }
    },
    mapMetricsToUnit() {
      this.metric_definitions = this.metrics.map((metric) => {
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
      if (!latestDate || latestDate < new Date('2017-01-01')) return null;
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
      const count_comments = this.countCriterionComments(criterion_id);
      if (count_comments == 0) {
        return 'Add comments';
      }
      return `Show comments (${count_comments})`;
    },
    countCriterionComments(criterion_id) {
      if (this.editedRanks[criterion_id]) {
        const ranks_comments = this.editedRanks[criterion_id].filter(
          (rank) =>
            rank.criterion_id == criterion_id &&
            rank.comment !== null &&
            rank.comment.length > 0,
        );
        return ranks_comments.length;
      }
      return 0;
    },
    checkCatComplete(cat) {
      // Get the tracking data in JSON format
      const category_tracking = Array.isArray(this.local_unit.category_tracking)
        ? this.local_unit.category_tracking
        : JSON.parse(this.local_unit.category_tracking);
      // Check there is tracking
      if (category_tracking) {
        // Filter and check if category is complete
        const category = category_tracking.filter((category) => {
          return category.category_id == cat.category_id;
        });
        if (category.length > 0) {
          return category[0].complete == 1;
        }
      }
    },
    changeCatComplete(category_ids_arr, new_val = null) {
      // Set variables
      let submit_change = false;
      let val = null;
      let submit_category_ids_arr = [];
      // Get the tracking data in JSON format
      const category_tracking = Array.isArray(this.local_unit.category_tracking)
        ? this.local_unit.category_tracking
        : JSON.parse(this.local_unit.category_tracking);
      // Go through each category and check if it is included in the array of ids listed
      category_tracking.forEach((category) => {
        if (category_ids_arr.includes(category.category_id)) {
          // If a specific value is set, set the categories completed status to that specific value (either complete or not complete)
          let submit_value =
            new_val != null ? new_val : category.complete == 1 ? 0 : 1;
          // If the new value is true and there is an error - do not submit it
          if (submit_value && this.checkCategoryErrors(category.category_id)) {
            return;
          } else {
            // Add id to the array to be submited and change the values for it
            submit_category_ids_arr.push(category.category_id);

            category.complete = submit_value;
            val = submit_value;
          }

          submit_change = true;
        }
      });
      if (submit_change && submit_category_ids_arr.length > 0) {
        completeCats(
          this.unit.rescore_session_units_id,
          submit_category_ids_arr,
          val,
        ).then(() => {
          // this.fetchUnitsData();
        });
      }
      // this.local_unit.category_tracking = JSON.stringify(category_tracking);
    },

    submitMetricsChanges(collection_unit_metric_definition_id) {
      const edited_metric = this.metric_definitions.find(
        (metric) =>
          metric.collection_unit_metric_definition_id ==
          collection_unit_metric_definition_id,
      );
      if (this.bulk_edit) {
        const return_draft = !(
          edited_metric.metric_value == null ||
          edited_metric.metric_value < 0 ||
          edited_metric.confidence_level == null ||
          (edited_metric.metric_units == '%' &&
            edited_metric.metric_value > 100)
        );
        this.metric_definitions.find(
          (metric) =>
            metric.collection_unit_metric_definition_id ==
            collection_unit_metric_definition_id,
        ).is_draft = return_draft;
        this.returnBulkEdit();
      } else {
        const edited_metric = this.metric_definitions.find(
          (metric) =>
            metric.collection_unit_metric_definition_id ==
            collection_unit_metric_definition_id,
        );
        // Check the the metric value and confidence is valid
        if (
          edited_metric.metric_value >= 0 &&
          edited_metric.confidence_level !== null &&
          !(
            edited_metric.metric_units == '%' &&
            edited_metric.metric_value > 100
          )
        ) {
          // Submit the metric change
          submitDataGeneric('submit-draft-metrics', {
            rescore_session_units_id: this.unit.rescore_session_units_id,
            collection_unit_id: this.unit.collection_unit_id,
            metric_json: [edited_metric],
          }).then(() => {
            // Fetch the updated data after submitting the metrics changes
            this.fetchUnitsData();
          });
        }
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

    async submitRankChanges(ranks, criterion_id) {
      if (this.bulk_edit) {
        this.returnBulkEdit();
      } else {
        try {
          // Check if there are any errors before submitting
          const errors = this.checkErrors(criterion_id);
          // Check if the ranks was actually changed
          const was_changed = this.checkChanged(criterion_id);
          if (
            (errors.length > 0 && !errors.some((e) => e.allow_submit)) ||
            !was_changed
          ) {
            // If there are errors, do not submit
            return;
          } else {
            // Set that this criterion is being saved
            this.saving_criterion_id = criterion_id;
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
            await submitDraftRrank(rank_draft);
            // Fetch the updated data after submitting the rank changes
            await this.fetchUnitsData();
            // Set that this criterion is done saving saved
            this.saving_criterion_id = 0;
          }
        } catch (error) {
          console.error('Submission error:', error);
          this.checkErrors(criterion_id);
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
    // Function to check for errors in a while category
    checkCategoryErrors(category_id) {
      const criterions = this.criterion.filter(
        (criteria) => criteria.category_id == category_id,
      );
      let is_error = false;
      criterions.forEach((criterion) => {
        let errors = this.checkErrors(criterion.criterion_id);
        if (errors.some((error) => error.type == 'error')) {
          is_error = true;
        }
      });
      return is_error;
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
      if (this.checkScoreDecimal(ranks_filtered)) {
        errors.push({
          message: 'Score contains a decimal',
          type: 'error',
        });
      }
      // Check if the score has changed but not saved - only if no other messages and if this criterion is not currently saving
      if (
        this.unit &&
        errors.length == 0 &&
        this.saving_criterion_id !== criterion_id &&
        !this.bulk_edit
      ) {
        // Check that there was a change
        const was_changed = this.checkChanged(criterion_id);
        if (was_changed) {
          errors.push({
            message: 'Change not saved!',
            type: 'error',
            allow_submit: true,
          });
        }
      } else if (
        errors.length == 0 &&
        this.saving_criterion_id === criterion_id
      ) {
        // Show that there is a change and it is saving
        errors.push({
          message: 'Saving change...',
          type: 'warning',
          allow_submit: true,
        });
      }

      return errors;
    },
    checkScoreDecimal(array) {
      return array.some((item) => {
        const value = item['percentage'];
        if (typeof value === 'number' && !isNaN(value)) {
          const percentage = Math.round(value * 100 * 100) / 100;
          return !Number.isInteger(percentage);
        }
        return false;
      });
    },
    checkChanged(criterion_id) {
      // Get filtered ranks
      const ranks_filtered = this.editedRanks[criterion_id] || [];
      // Sort ranks
      const sorted_current = [...ranks_filtered].sort(
        (a, b) => a.rank_id - b.rank_id,
      );
      // Get original data
      const original_data_edited_ranks = this.getInitialEditedRanks(this.unit);
      if (original_data_edited_ranks) {
        const original_data_ranks_filtered =
          original_data_edited_ranks[criterion_id] || [];
        const sorted_original = [...original_data_ranks_filtered].sort(
          (a, b) => a.rank_id - b.rank_id,
        );
        // Check if there is a difference between original data and current data
        for (let i = 0; i < sorted_current.length; i++) {
          const original = sorted_original[i];
          const current = sorted_current[i];
          //Check if the current rank is the same as the original
          if (
            original.percentage !== current.percentage ||
            original.comment !== current.comment
          ) {
            // Change found
            return true;
          }
        }
        // No changes found
        return false;
      }
    },
    checkEdited(ranks) {
      if (ranks == undefined) return false;
      // Check if any rank has been edited
      return ranks.some((rank) => rank.is_draft);
    },
    getInitialEditedRanks(unit) {
      const ranks = unit.ranks_json;
      const grouped = {};
      if (!ranks || ranks.length === 0) return grouped;

      ranks.forEach((rank) => {
        if (!grouped[rank.criterion_id]) grouped[rank.criterion_id] = [];
        grouped[rank.criterion_id].push({ ...rank });
      });

      return grouped;
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
  margin: 0.25rem 0;
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.pointer {
  cursor: pointer;
}

.edit-comments {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
