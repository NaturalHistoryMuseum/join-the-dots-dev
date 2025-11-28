<template>
  <div class="progress-container">
    <div
      class="progress-bar"
      :style="{
        width: progress + '%',
        backgroundColor: barColor,
      }"
    >
      {{ Math.round(progress) }}%
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
  progress: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 100,
  },
});

// Helper to interpolate between two hex colors
function interpolateColor(color1, color2, factor) {
  let c1 = parseInt(color1.slice(1), 16);
  let c2 = parseInt(color2.slice(1), 16);

  let r1 = (c1 >> 16) & 0xff,
    g1 = (c1 >> 8) & 0xff,
    b1 = c1 & 0xff;

  let r2 = (c2 >> 16) & 0xff,
    g2 = (c2 >> 8) & 0xff,
    b2 = c2 & 0xff;

  const r = Math.round(r1 + factor * (r2 - r1));
  const g = Math.round(g1 + factor * (g2 - g1));
  const b = Math.round(b1 + factor * (b2 - b1));

  return `rgb(${r}, ${g}, ${b})`;
}

const barColor = computed(() => {
  if (props.progress <= 50) {
    const factor = props.progress / 50; // 0 at 0, 1 at 50
    return interpolateColor('#fa3608', '#ffe600', factor);
  } else {
    const factor = (props.progress - 50) / 50; // 0 at 50, 1 at 100
    return interpolateColor('#ffe600', '#30ff2e', factor);
  }
});
</script>

<style scoped>
.progress-container {
  height: 24px;
  background-color: #eee;
  border-radius: 12px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  transition:
    width 0.3s ease,
    background-color 0.3s ease;
}
</style>
