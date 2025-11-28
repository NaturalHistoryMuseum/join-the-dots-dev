<template>
  <div v-if="criterion.length > 0">
    <div
      v-for="edited_unit in this.edited_units"
      :key="edited_unit.collection_unit_id"
      class="unit-changes-container"
    >
      <div
        class="edited-unit"
        v-if="
          (edited_unit.metric_json &&
            edited_unit.metric_json.filter((metric) => metric.is_draft).length >
              0) ||
          (edited_unit.unit_comment && edited_unit.unit_comment_is_draft) ||
          (edited_unit.editedRanks &&
            Object.values(edited_unit.editedRanks).some((ranks) =>
              ranks.some((rank) => rank.is_draft),
            ))
        "
      >
        <AccordionGeneric
          :accordion_open="expanded_accordion == edited_unit.collection_unit_id"
          :accordion_title="'Unit Name: ' + edited_unit.unit_name"
          :accordion_open_function="toggleAccordion"
          :accordion_id="edited_unit.collection_unit_id"
          class="accordion-edit-unit"
        >
          <div
            v-if="
              edited_unit.metric_json &&
              edited_unit.metric_json.filter((metric) => metric.is_draft)
                .length > 0
            "
            class="change-container"
          >
            <p class="h4-style">Metrics</p>
            <div
              v-for="(metric, index) in edited_unit.metric_json.filter(
                (metric) => metric.is_draft,
              )"
              :key="index"
              class="change-item"
            >
              <div class="changed-container metric">
                <div class="changed-item">
                  <p>{{ fieldNameCalc(metric.metric_name) }}:</p>
                  <p>{{ metric.metric_value }}</p>
                </div>
                <div class="changed-item">
                  <p>Confidence:</p>
                  <p>{{ metric.confidence_level }}</p>
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="edited_unit.unit_comment && edited_unit.unit_comment_is_draft"
            class="change-container"
          >
            <p class="h4-style">Unit Comment</p>
            <p class="change-item">{{ edited_unit.unit_comment }}</p>
          </div>
          <div
            v-if="edited_unit.editedRanks && edited_unit.editedRanks"
            class="change-container"
          >
            <p class="h4-style">Scores</p>
            <div
              v-for="(crit, index) in edited_unit.editedRanks"
              :key="index"
              class="change-item"
            >
              <div v-if="crit.some((rank) => rank.is_draft)">
                <p class="h5-style">
                  {{
                    criterion.find(
                      (criteria) =>
                        crit[0].criterion_id == criteria.criterion_id,
                    ).criterion_code
                  }}
                  -
                  {{
                    criterion.find(
                      (criteria) =>
                        crit[0].criterion_id == criteria.criterion_id,
                    ).criterion_name
                  }}
                </p>
                <div class="changed-container">
                  <div
                    v-for="(rank, rankIndex) in crit"
                    :key="rankIndex"
                    class="changed-item"
                  >
                    <p>{{ `Rank ${rank.rank_value} (%)` }}</p>
                    <p>{{ rank.percentage ? rank.percentage * 100 : '0' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </AccordionGeneric>
      </div>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';
import fieldNameCalc from '@/utils/utils';
import AccordionGeneric from './AccordionGeneric.vue';

export default {
  name: 'ReviewUnitChanges',
  components: { AccordionGeneric },
  props: {
    units: Array,
  },
  data() {
    return {
      criterion: [],
      editedRanks: [],
      expanded_accordion: 0,
    };
  },
  mounted() {
    this.fetchCriterionData();
    this.addEditRanks();
  },
  methods: {
    fieldNameCalc,
    fetchCriterionData() {
      getGeneric('criterion').then((response) => {
        this.criterion = response;
      });
    },
    addEditRanks() {
      this.edited_units = this.units.map((unit) => ({
        ...unit,
        editedRanks: this.initializeEditedRanks(unit),
      }));
    },
    initializeEditedRanks(unit) {
      this.units.forEach;
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

      return grouped;
    },
    toggleAccordion(accord_id) {
      if (this.expanded_accordion === accord_id) {
        this.expanded_accordion = null;
      } else {
        this.expanded_accordion = accord_id;
      }
    },
  },
};
</script>

<style scoped>
.unit-changes-container {
  text-align: left;
  margin: 1rem 2rem;
}

.change-container {
  margin-left: 2rem;
}

.change-item {
  margin-left: 2rem;
}
.edited-unit {
  display: flex;
  justify-content: center;
  align-items: center;
}
.accordion-edit-unit {
  width: 80%;
}
</style>
