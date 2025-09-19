<template>
  <!-- <div class="progress-header">
    <ProgressBar
      :progress="calcUnitCompletePercentage()"
      class="scoring-progress-bar"
    />
  </div> -->
  <div v-if="unit_scores.length > 0" class="">
    <UnitScores v-if="!add_unit_mode" :unit="unit_scores[0]" :rescore="false" />
    <UnitScores
      v-if="add_unit_mode"
      :unit="unit_scores[0]"
      :rescore="true"
      :bulk_edit="true"
      @newUnit="handleUnitUpdate"
    />
  </div>
  <div v-else class="content row centered">
    No scores recorded for this unit
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';
// import ProgressBar from '../ProgressBar.vue';
import UnitScores from '../UnitScores.vue';

export default {
  name: 'ScoresTab',
  props: {
    unit: Object,
    unit_id: Number,
    add_unit_mode: Boolean,
  },
  components: {
    UnitScores,
    // ProgressBar,
  },
  data() {
    return { unit_scores: [], edited_unit: [], rank_json: [] };
  },
  async mounted() {
    if (this.add_unit_mode) {
      const data = await import('../../utils/ranks_json_temp.json');
      this.rank_json = data.default;
      this.unit_scores = [
        {
          collection_unit_id: 0,
          unit_name: '',
          ranks_json: this.rank_json,
          metric_json: [],
          unit_comment: '',
          unit_comment_date_added: '',
        },
      ];
    } else {
      this.fetchData();
    }
  },
  computed: {
    unit_value: {
      get() {
        return this.unit;
      },
      set(value) {
        this.$emit('updateUnit', value);
      },
    },
  },
  methods: {
    async fetchData() {
      if (!this.add_unit_mode) {
        getGeneric(`unit-scores/${this.unit_id}`).then((response) => {
          this.unit_scores = response.map((unit) => {
            // Parse category tracking JSON
            unit.ranks_json = JSON.parse(unit.ranks_json);
            unit.metric_json = JSON.parse(unit.metric_json);
            return unit;
          });
        });
      }
    },
    handleUnitUpdate(updatedUnit) {
      // Merge the updated ranks into the corresponding unit in your parent data
      this.edited_unit = updatedUnit;
      this.$emit('new_unit', updatedUnit);
      this.calcUnitCompletePercentage();
    },
    calcUnitCompletePercentage() {
      if (!this.edited_unit || !this.edited_unit.ranks_json) {
        return 0;
      }
      const ranks = this.edited_unit.ranks_json;
      console.log('this is the edited ranks:', ranks);
      console.log('this is the total ranks:', this.rank_json);

      const metrics = this.edited_unit.metric_json;
      // Remove C3 from ranks to mark completness
      const filtered_rank_json = this.rank_json.filter(
        (rank) => rank.criterion_id !== 3,
      );
      // Calculate the total completeness based on the number of ranks divided by 5
      const total_completness = filtered_rank_json.length / 5 + 3; // Adding 3 for the metrics - should do this dynamically
      let actual_completness = 0;
      // Go through each rank and see if it has a total score
      ranks.forEach((rank_group) => {
        const percentage_total = rank_group.reduce(
          (sum, r) => sum + (r.percentage || 0),
          0,
        );
        // Check if the total percentage is complete
        if (percentage_total === 1) {
          actual_completness++;
        }
      });
      // Check if the metrics are complete - they are only added ot edited_unit if they are complete
      actual_completness += metrics.length;
      const percentage = (
        (actual_completness / total_completness) * 100 || 0
      ).toFixed(2);
      this.$emit('update:scores_percentage', percentage);
      return percentage;
    },
  },
};
</script>

<style>
.progress-header {
  display: flex;
  justify-content: center;
  margin: 1rem;
}
</style>
