<template>
  <Scatter :data="chartData" :options="options" ref="chartRef" />
</template>

<script setup>
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
} from 'chart.js';
import { onMounted, ref } from 'vue';
import { Scatter } from 'vue-chartjs';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LinearScale,
  PointElement,
  CategoryScale,
);

const chartRef = ref(null);
const labels = ['A', 'B', 'C', 'D'];
const loading = ref(true);
const chartData = ref({
  labels,
  datasets: [
    {
      label: 'Loading...',
      data: [],
      pointBackgroundColor: 'blue',
      pointRadius: 6,
      showLine: false,
    },
  ],
});

const options = {
  scales: {
    x: {
      type: 'category',
      labels,
      grid: {
        drawOnChartArea: false,
      },
    },
    y: {
      min: 0,
      max: 5,
      ticks: { stepSize: 1 },
    },
  },
  animation: false, // Important: turn off built-in animation
  responsive: true,
};

// eslint-disable-next-line no-unused-vars
let animationId;
let t = 0;

function animateWaveDots() {
  const waveData = labels.map((_, i) => ({
    x: i,
    y: 2.5 + Math.sin(t + i * 0.5) * 1.5, // Wave motion centered at 2.5
  }));
  console.log(waveData);
  chartData.value.datasets[0].data = waveData;
  t += 0.05;
  if (loading.value) {
    animationId = requestAnimationFrame(animateWaveDots);
  }
}

onMounted(async () => {
  animateWaveDots();

  // Simulate data fetching (replace with your real Axios call)
  // const response = await axios.get('/api/your-data') // Replace with your real API
  // const realValues = [3, 2, 4, 1] // Replace with response data

  // // Stop animation
  // loading.value = false
  // cancelAnimationFrame(animationId)

  // // Update chart with real data
  // chartData.value.datasets[0].data = realValues.map((y, x) => ({ x, y }))
  // chartData.value.datasets[0].label = 'Real Data'
});
</script>
