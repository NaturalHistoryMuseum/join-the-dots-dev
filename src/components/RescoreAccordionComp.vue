<template>
  <div class="accordion-container">
    <!-- Accordion button -->
    <button
      :class="['accordion', error ? 'accordion-error' : '']"
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
      <p class="accordion-header">{{ header }}</p>
      <p class="accordion-complete" v-if="rescore">
        {{ complete ? 'Complete' : 'Incomplete' }}
      </p>
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
        <div :class="['accordion-content ', error ? 'accordion-error' : '']">
          <!-- Insert content -->
          <slot></slot>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'RescoreAccordionComp',
  props: {
    accordion_id: Number,
    toggleAccordion: Function,
    expanded_accordion: Number,
    header: String,
    category_cols: Array,
    rescore: Boolean,
    complete: Boolean,
    changeCatComplete: Function,
    error: Boolean,
  },
  methods: {},
};
</script>

<style></style>
