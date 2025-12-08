<template>
  <div class="stepper-container">
    <div v-for="(step, index) in steps" :key="step.step" class="step">
      <div class="step-line" v-if="index !== 0"></div>
      <button
        class="step-number"
        :class="{ 'selected-step': current_step === step.step }"
        @click="step_value = step.step"
      >
        {{ step.step }}
      </button>
      <div class="step-title">{{ step.title }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StepperComp',
  props: {
    steps: {
      type: Array,
      required: true,
    },
    current_step: {
      type: Number,
      required: true,
    },
  },
  emits: ['update:current_step'],
  computed: {
    step_value: {
      get() {
        return this.current_step;
      },
    },
  },
};
</script>

<style scoped>
/* Stepper */
.stepper-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4rem;
  position: relative;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 7rem;
}

.step-number {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  border: 2px solid #ff5957;
  background-color: white;
  color: black;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}
.selected-step {
  background-color: #ff5957;
  color: black;
}

.step-title {
  margin-top: 8px;
  font-size: 14px;
  color: #333;
  text-align: center;
}

.step-line {
  position: absolute;
  top: 1.5rem;
  left: -100%;
  width: 140%;
  height: 2px;
  background-color: #ff5957;
  z-index: 0;
}
.step-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 1rem;
}
</style>
