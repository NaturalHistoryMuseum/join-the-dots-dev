<template>
  <div v-if="unit_scores.length > 0" class="">
    <UnitScores :unit="unit_scores[0]" :rescore="false" />
  </div>
  <div v-else class="content row centered">
    No scores recorded for this unit
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';
import UnitScores from '../UnitScores.vue';

export default {
  name: 'ScoresTab',
  props: {
    unit: Object,
    unit_id: Number,
  },
  components: {
    UnitScores,
  },
  data() {
    return { unit_scores: [] };
  },
  mounted() {
    this.fetchData();
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
      getGeneric(`unit-scores/${this.unit_id}`).then((response) => {
        this.unit_scores = response.map((unit) => {
          // Parse category tracking JSON
          unit.ranks_json = JSON.parse(unit.ranks_json);
          unit.metric_json = JSON.parse(unit.metric_json);
          return unit;
        });
      });
    },
  },
};
</script>

<style></style>
