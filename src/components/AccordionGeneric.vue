<template>
  <div class="accordion-container">
    <!-- Accordion button -->
    <button
      :class="['accordion', accordion_eror ? 'accordion-error' : '']"
      :style="{
        borderRadius: accordion_open ? '10px 10px 0px 0px' : '10px',
        backgroundColor: accordion_open ? '#f3f3f3' : 'white',
        color: accordion_open ? 'black' : 'black',
      }"
      @click="accordion_open_function(accordion_id)"
    >
      <!-- Accordion header -->
      <h6 class="accordion-header">
        {{ accordion_title }}
      </h6>
      <!-- Arrow button -->
      <div v-if="accordion_open" class="accordion-arrow">
        <i class="bi bi-chevron-up accordion-icon"></i>
      </div>
      <div v-else class="accordion-arrow">
        <i class="bi bi-chevron-down accordion-icon"></i>
      </div>
    </button>
    <!-- Accordion content -->
    <transition name="fade">
      <div v-show="accordion_open">
        <div
          :class="[
            'accordion-content ',
            accordion_eror ? 'accordion-error' : '',
          ]"
        >
          <!-- Insert content -->
          <slot></slot>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'AccordionGeneric',
  props: {
    accordion_open: Boolean,
    accordion_title: String,
    accordion_open_function: Function,
    accordion_eror: Boolean,
    accordion_id: Number,
  },
};
</script>

<style>
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

.accordion-error {
  border-color: #fa3608 !important;
  border-width: 1px !important;
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
