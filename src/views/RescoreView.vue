<template>
  <div class="rescore" v-show="!loading">
    <div class="row" v-if="!rescore_saved">
      <div class="col-md-3"></div>
      <StepperComp
        :steps="steps"
        :current_step="current_step"
        class="col-md-6"
      />
      <div class="col-md-3"></div>
    </div>
    <div
      class="stepper-navigation"
      v-if="rescore_session_id && !rescore_saved && units.length > 0"
    >
      <zoa-button
        v-if="current_step > 1"
        label="Previous"
        @click="current_step--"
        class="stepper-btn left-btn"
      />
      <div v-else></div>
      <zoa-button
        v-if="current_step < steps.length"
        label="Continue"
        @click="current_step++"
        class="stepper-btn right-btn"
      />
    </div>
    <div v-if="current_step === 1">
      <ManageRescoreView
        @update:current_step="current_step++"
        :open_rescore="open_rescore"
        :fetchUnitsData="getData"
      />
    </div>
    <div v-if="current_step === 2">
      <EditRescoreView
        :rescore_session_id="rescore_session_id"
        :units="units"
        :fetchUnitsData="getData"
      />
    </div>
    <div v-if="current_step === 3">
      <ReviewRescoreView
        :rescore_session_id="rescore_session_id"
        :units="units"
        @update:rescore_saved="rescore_saved = true"
      />
    </div>
  </div>
  <div v-show="loading">loading...</div>
</template>

<script>
import StepperComp from '@/components/StepperComp.vue';
import { currentUser } from '@/services/authService';
import { getGeneric } from '@/services/dataService';
import EditRescoreView from '../components/rescore/EditRescoreView.vue';
import ManageRescoreView from '../components/rescore/ManageRescoreView.vue';
import ReviewRescoreView from '../components/rescore/ReviewRescoreView.vue';

export default {
  name: 'RescoreView',
  components: {
    StepperComp,
    ManageRescoreView,
    EditRescoreView,
    ReviewRescoreView,
  },
  data() {
    return {
      units: [],
      steps: [
        {
          step: 1,
          title: 'Select Units',
          description: 'Choose the units you want to rescore.',
        },
        {
          step: 2,
          title: 'Edit Scores',
          description: 'Adjust the scores for the selected units.',
        },
        {
          step: 3,
          title: 'Review Changes',
          description: 'Review your changes before submiting.',
        },
      ],
      current_step: 1,
      rescore_session_id: null,
      open_rescore: {},
      loading: true,
      rescore_saved: false,
    };
  },
  setup() {
    return { currentUser };
  },
  created() {
    this.rescore_session_id = this.$route.query.rescore_session_id || null;
  },
  mounted() {
    this.getData();
  },
  methods: {
    async getData() {
      // If user is admin and has requested a specific rescore - fetch that
      if (this.currentUser.role_id === 4 && this.rescore_session_id) {
        await this.fetchRescoreUnits();
      } else {
        // Else see if there is an open rescore
        await this.fetchUnitsData();
      }
      this.loading = false;
    },
    async fetchUnitsData() {
      const rescoreResp = await getGeneric('open-rescore');
      // Check if there is an open rescore session
      this.open_rescore = rescoreResp.length > 0 ? rescoreResp[0] : {};
      if (
        Object.keys(this.open_rescore).length > 0 &&
        !this.rescore_session_id
      ) {
        // Set the rescore session id
        this.rescore_session_id = this.open_rescore.rescore_session_id;
        // Fetch units in this rescore session
        this.fetchRescoreUnits();
      }
    },
    async fetchRescoreUnits() {
      await getGeneric(`rescore-units/${this.rescore_session_id}`).then(
        (response) => {
          this.units = response.map((unit) => {
            // Parse category tracking JSON
            unit.category_tracking = JSON.parse(unit.category_tracking) || null;
            unit.ranks_json = JSON.parse(unit.ranks_json) || null;
            unit.metric_json = JSON.parse(unit.metric_json) || null;
            return unit;
          });
        },
      );
      if (this.units.length > 0) {
        // Move to the editing page after loading
        this.current_step = 2;
      }
    },
  },
};
</script>

<style scoped>
.rescore-title {
  align-self: center;
}
.stepper-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}

.left-btn {
  margin-left: 30%;
}

.right-btn {
  margin-right: 30%;
}
</style>
