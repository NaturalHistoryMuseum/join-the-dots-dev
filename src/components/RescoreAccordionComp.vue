<template>
  <div class="accordion-container">
    <!-- Accordion button -->
    <button
      class="accordion"
      :style="{
        borderRadius:
          expanded_accordion == accordion_id ? '10px 10px 0px 0px' : '10px',
        backgroundColor:
          expanded_accordion == accordion_id ? '#f3f3f3' : 'white',
        color: expanded_accordion == accordion_id ? 'black' : 'black',
      }"
      @click="toggleAccordion(accordion_id)"
    >
      <!-- Accordion header -->
      <h6 class="accordion-header">{{ header }}</h6>
      <h6 class="accordion-complete" v-if="rescore">
        {{ complete ? 'Complete' : 'Incomplete' }}
      </h6>
      <zoa-button
        v-if="rescore"
        size="sm"
        class="accordion-btn"
        @click.stop="changeCatComplete"
        >{{ complete ? 'Edit' : 'Mark Complete' }}</zoa-button
      >
      <!-- Arrow button -->
      <div v-if="expanded_accordion == accordion_id" class="accordion-arrow">
        <i class="bi bi-chevron-up accordion-icon"></i>
      </div>
      <div v-else class="accordion-arrow">
        <i class="bi bi-chevron-down accordion-icon"></i>
      </div>
    </button>
    <!-- Accordion content -->
    <transition name="fade">
      <div v-show="expanded_accordion === accordion_id">
        <div class="accordion-content">
          <!-- Insert content -->
          <slot></slot>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: {
    accordion_id: Number,
    toggleAccordion: Function,
    expanded_accordion: Number,
    header: String,
    category_cols: Array,
    rescore: Boolean,
    complete: Boolean,
    changeCatComplete: Function,
  },
  methods: {},
};
</script>

<style scoped>
.accordion {
  border-width: 2px;
  border-radius: 10px;
  border-style: solid;
  border-color: #87999e;
  background-color: white;
  width: 100%;
  display: flex;
  gap: 2rem;
  align-items: center;
  padding: 0.5rem 2rem;
}

.accordion-btn {
  margin-left: auto;
  z-index: 1;
  min-width: 8rem;
}

.accordion-content {
  border-width: 1px;
  border-color: #87999e;
  border-style: solid;
  border-radius: 0px 0px 10px 10px;
  margin-top: -2;
  padding: 0.5rem 2rem;
  text-align: left;
}

.accordion-header {
  padding: 0;
  margin: 0;
  width: 30%;
  text-align: left;
  font-weight: bold;
}

.accordion-complete {
  padding: 0;
  margin: 0;
  /* font-weight: bold; */
}

.accordion-icon {
  font-size: 1.5rem;
}

.accordion-container {
  margin-bottom: 1rem;
}

.accordion-arrow {
  margin-left: auto;
  margin-right: 0;
}
</style>
