<template>
  <div class="boader-header">
    <h2 class="boader-header-title">Statistics</h2>
  </div>
  *Not live data
  <div v-if="currentUser.level == 1" class="row">
    <div class="col-md-8">
      <!-- Table -->
      <b-table
        id="summary-table"
        class="summary-table"
        striped
        hover
        responsive
        :items="stats.category_percent"
      ></b-table>
      <p v-if="!stats.category_percent">loading...</p>
    </div>
    <div class="col-md-4 stats-summary">
      <!-- <h4>Stats Summary</h4> -->
      <div class="stats-card">
        <h4>Units Count:</h4>
        <h4>{{ stats.total_units }}</h4>
      </div>
      <div class="stats-card">
        <h4>Units Count:</h4>
        <h4>{{ stats.total_units }}</h4>
      </div>
    </div>
  </div>
  <div v-if="currentUser.level == 2" class="row">
    <div class="stats-numbers">
      <!-- <h4>Stats Summary</h4> -->
      <div class="stats-card">
        <h4>Last Rescored:</h4>
        <h4>{{ stats.last_rescored_formatted }}</h4>
      </div>
      <div class="stats-card">
        <h4>Assigned Units:</h4>
        <h4>{{ stats.unit_count }}</h4>
      </div>
      <div class="stats-card">
        <h4>Last Rescored:</h4>
        <h4>{{ stats.last_rescored_formatted }}</h4>
      </div>
      <div class="stats-card">
        <h4>Your Unit Count:</h4>
        <h4>{{ stats.unit_count }}</h4>
      </div>
    </div>
    <div class="row">
      <div class="col-md-9 stats-chart">
        <Bubble id="my-chart-id" :options="chart_options" :data="chart_data" />
      </div>
      <div class="col-md-3 stats-pie">
        <Pie :data="pie_one" :options="chartOptions" />
        <Pie :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
  <div v-if="currentUser.level == 3" class="row">
    <div class="stats-numbers">
      <!-- <h4>Stats Summary</h4> -->
      <div class="stats-card">
        <h4>Division Units:</h4>
        <h4>{{ 200 }}</h4>
      </div>
      <div class="stats-card">
        <h4>Rescored this Year:</h4>
        <h4>{{ 40 + ' (20%)' }}</h4>
      </div>
      <div class="stats-card">
        <h4>Left to Rescore:</h4>
        <h4>{{ 160 + ' (80%)' }}</h4>
      </div>
      <div class="stats-card">
        <h4>Deadline:</h4>
        <h4>{{ '2026-04-01' }}</h4>
      </div>
    </div>
    <div class="row">
      <div class="col-md-9 stats-chart">
        <Bubble id="my-chart-id" :options="chart_options" :data="chart_data" />
      </div>
      <div class="col-md-3 stats-pie">
        <Doughnut :data="pie_two" :options="chartOptions" />
        <Pie :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script>
import { getStatsGeneric } from '@/services/statsService';
import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
} from 'chart.js';
import { Bubble, Doughnut, Pie } from 'vue-chartjs';
import { currentUser } from '../services/authService';
// import LoadingChart from '@/components/LoadingChart.vue'
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
);
export default {
  setup() {
    return { currentUser };
  },
  components: {
    Bubble,
    Pie,
    Doughnut,
    // LoadingChart,
  },
  data() {
    return {
      stats: [],
      chartData: {
        labels: ['January', 'February', 'March'],
        datasets: [{ data: [40, 20, 12] }],
      },
      pie_one: {
        labels: ['Scored in last year', 'Not scored in last year'],
        datasets: [
          {
            label: 'Scored in last year',
            data: [1, 8],
          },
        ],
      },
      pie_two: {
        labels: ['Scored in last year', 'Not scored in last year'],
        datasets: [
          {
            backgroundColor: ['#41B883', '#E46651'],
            data: [2, 8],
          },
        ],
      },
      chartOptions: {
        responsive: true,
      },
      chart_data: {
        labels: [
          'Condition',
          'Importance & Significance',
          'Information',
          'Outreach',
        ],
        datasets: [
          {
            label: 'Current Dots',
            data: [2, 3, 4.5, 3].map((y, x) => ({ x, y })),
            pointBackgroundColor: '#7C8CF8',
            pointRadius: 15,
            showLine: false,
          },
          {
            label: 'Last Year Dots',
            data: [1.5, 3.3, 4, 2.9].map((y, x) => ({ x, y })),
            pointBackgroundColor: '#f87979',
            pointRadius: 15,
            showLine: false,
          },
        ],
      },
      labels: [
        'Condition',
        'Importance & Significance',
        'Information',
        'Outreach',
      ],
      chart_options: {
        scales: {
          x: {
            type: 'category',
            labels: this.lables,
            grid: {
              drawOnChartArea: false,
            },
          },
          y: {
            beginAtZero: true,
            min: 0,
            max: 5,
          },
        },
        animation: false,
        responseive: true,
        type: 'bubble',
      },
      // chart_data: {
      //   labels: ['Condition', 'Importance & Significance', 'Information', 'Outreach'],
      //   datasets: [
      //     {
      //       label: 'Loading...',
      //       data: [],
      //       pointBackgroundColor: '#7C8CF8',
      //       pointRadius: 15,
      //       showLine: false,
      //     },
      //   ],
      // },
      // loadingDots: true,
      // waveFrame: null,
      // t: 0,
    };
  },
  mounted() {
    // this.startWaveAnimation()
    // Fetch data
    this.fetchData();
  },
  // beforeUnmount() {
  //   cancelAnimationFrame(this.waveFrame)
  // },
  methods: {
    // Navigate to path
    navigate(path) {
      this.$router.push({ path: path });
    },
    // Fetch data
    fetchData() {
      // Fetch data
      getStatsGeneric('home-stats').then((response) => {
        this.stats = response;
        if (this.stats.last_rescored) {
          this.stats.last_rescored_formatted = new Date(
            this.stats.last_rescored,
          )
            .toISOString()
            .split('T')[0];
        }
        if (
          this.stats.scored_in_last_year &&
          this.stats.scored_in_last_year.length > 0
        ) {
          this.pie_one = {
            labels: ['Scored in last year', 'Not scored in last year'],
            datasets: [
              {
                label: 'Scored in last year',
                // data: [1, 8],
                data: [
                  this.stats.scored_in_last_year[0].less_than_year,
                  this.stats.scored_in_last_year[0].older_than_year,
                ],
                backgroundColor: ['#FF6384', '#36A2EB'],
              },
            ],
          };
        }
        // Stop animation and replace dots
        this.loadingDots = false;
        cancelAnimationFrame(this.waveFrame);

        // Replace wave data with real values (adjust below with real data)
        const realValues = [2, 3, 4.5, 3];
        this.chart_data.datasets[0].data = realValues.map((y, x) => ({ x, y }));
        this.chart_data.datasets[0].label = 'Current Dots';
      });
    },

    // startWaveAnimation() {
    //   const update = () => {
    //     this.chart_data.datasets[0].data = this.labels.map((_, i) => ({
    //       x: i,
    //       y: 2.5 + Math.sin(this.t + i * 0.5) * 1.5,
    //       r: 10, // Or make it dynamic if desired
    //     }))
    //     this.t += 0.05
    //     if (this.loadingDots) {
    //       this.waveFrame = requestAnimationFrame(update)
    //     }
    //   }
    //   update()
    // },
  },
};
</script>

<style scoped>
.stats-summary {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  /* justify-content: space-between; */
}
.stats-card {
  background-color: var(--secondary-col);
  margin: 0 5px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
  color: white;
}

.stats-numbers {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 4rem;
  position: relative;
}
</style>
