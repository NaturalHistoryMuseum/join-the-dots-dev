<template>
  <div class="accordion-container">
    <button
      class="accordion"
      :style="{
        borderRadius: expandedAccordion == accordionId ? '10px 10px 0px 0px' : '10px',
        backgroundColor: expandedAccordion == accordionId ? '#f3f3f3' : 'white',
        // backgroundColor:
        //   expandedAccordion == accordionId ? category_cols[accordionId].col : 'white',
        color: expandedAccordion == accordionId ? 'black' : 'black',
        // borderColor: category_cols[accordionId].col,
      }"
      @click="toggleAccordion(accordionId)"
    >
      <h6 class="accordion-header">{{ header }}</h6>
      <h6 class="accordion-complete">Incomplete</h6>
      <zoa-button size="sm" class="accordion-btn" @click.stop="markComplete"
        >Mark Complete</zoa-button
      >
      <div v-if="expandedAccordion == accordionId">
        <i class="bi bi-chevron-up accordion-icon"></i>
      </div>
      <div v-else>
        <i class="bi bi-chevron-down accordion-icon"></i>
      </div>
    </button>
    <transition name="fade">
      <div v-show="expandedAccordion === accordionId">
        <div class="accordion-content">
          <slot></slot>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: {
    accordionId: Number,
    toggleAccordion: Function,
    expandedAccordion: Number,
    header: String,
    category_cols: Array,
  },
  methods: {
    markComplete() {
      console.log(`Marking accordion ${this.accordionId} as complete`)
    },
  },
}
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
  z-index: 10;
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
  width: 20%;
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
</style>
