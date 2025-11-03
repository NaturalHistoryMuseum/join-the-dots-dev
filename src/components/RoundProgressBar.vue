<template>
  <div class="circular-container">
    <svg viewBox="0 0 100 100" class="circular-svg">
      <circle
        class="bg"
        cx="50"
        cy="50"
        r="45"
        fill="none"
        stroke="#eee"
        stroke-width="10"
      />
      <circle
        class="progress"
        cx="50"
        cy="50"
        r="45"
        fill="none"
        :stroke="barColor"
        stroke-width="10"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        transform="rotate(-90 50 50)"
      />
      <text x="50" y="54" text-anchor="middle" font-size="16" fill="#333">
        <!-- {{ progress }}%   -->
      </text>
    </svg>
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

const radius = 45;
const circumference = 2 * Math.PI * radius;

const dashOffset = computed(
  () => circumference - (props.progress / 100) * circumference,
);

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
    const factor = props.progress / 50;
    return interpolateColor('#ff0000', '#ffa500', factor);
  } else {
    const factor = (props.progress - 50) / 50;
    return interpolateColor('#ffa500', '#00ff00', factor);
  }
});
</script>

<style scoped>
.circular-container {
  width: 2.5rem;
  height: 2.5rem;
}
.circular-svg {
  width: 100%;
  height: 100%;
}
</style>
