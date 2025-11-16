<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="sticky top-0 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm z-10 py-4 mb-6">
          <div class="flex flex-wrap justify-between items-center gap-4">
            <h1 class="text-slate-900 dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">
              Analytics Overview
            </h1>
            <div class="flex items-center gap-3">
              <button
                @click="toggleDatePicker"
                class="flex h-10 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-white dark:bg-slate-800/50 border border-slate-300 dark:border-slate-700 px-4 hover:bg-slate-50 dark:hover:bg-slate-800"
              >
                <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">calendar_today</span>
                <p class="text-slate-800 dark:text-slate-200 text-sm font-medium">{{ selectedDateRange }}</p>
                <span class="material-symbols-outlined text-slate-500 dark:text-slate-400">expand_more</span>
              </button>
            </div>
          </div>
        </header>

        <!-- Metric Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div
            v-for="metric in metrics"
            :key="metric.label"
            class="bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 p-5"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-primary">{{ metric.icon }}</span>
              </div>
              <p class="text-sm font-medium text-slate-600 dark:text-slate-400">{{ metric.label }}</p>
            </div>
            <p class="text-4xl font-bold text-slate-900 dark:text-white mt-4">{{ metric.value }}</p>
            <div
              class="flex items-center gap-1 text-sm mt-2"
              :class="metric.trend > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
            >
              <span class="material-symbols-outlined" style="font-size: 16px;">
                {{ metric.trend > 0 ? 'arrow_upward' : 'arrow_downward' }}
              </span>
              <span>{{ Math.abs(metric.trend) }}% vs last period</span>
            </div>
          </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
          <!-- Call Volume Chart -->
          <div class="lg:col-span-3 bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 p-6">
            <div class="flex flex-wrap justify-between items-center gap-3 mb-4">
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Call Volume Over Time</h3>
              <div class="flex items-center gap-2 rounded-lg bg-slate-100 dark:bg-slate-800 p-1 text-sm">
                <button
                  v-for="period in ['Daily', 'Weekly', 'Monthly']"
                  :key="period"
                  @click="selectedChartPeriod = period"
                  class="px-3 py-1 rounded-md transition-colors"
                  :class="selectedChartPeriod === period
                    ? 'bg-white dark:bg-slate-700 shadow-sm text-primary font-semibold'
                    : 'text-slate-600 dark:text-slate-300'"
                >
                  {{ period }}
                </button>
              </div>
            </div>
            <div class="h-80">
              <canvas ref="chartCanvas"></canvas>
            </div>
          </div>

          <!-- Top Agents -->
          <div class="lg:col-span-2 bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 p-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Top Agents by Call Volume</h3>
              <button class="text-sm text-primary hover:underline" @click="handleViewAllAgents">
                View All
              </button>
            </div>
            <div class="space-y-4">
              <div
                v-for="(agent, index) in topAgents"
                :key="agent.name"
                class="flex items-center gap-4"
              >
                <p class="w-6 text-slate-500 dark:text-slate-400 font-medium text-sm">{{ index + 1 }}.</p>
                <div class="flex-1">
                  <p class="text-sm font-medium text-slate-800 dark:text-slate-200">{{ agent.name }}</p>
                  <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 mt-1">
                    <div
                      class="bg-primary h-2 rounded-full transition-all duration-300"
                      :style="{ width: agent.percentage + '%' }"
                    ></div>
                  </div>
                </div>
                <p class="text-sm font-bold text-slate-800 dark:text-slate-200">
                  {{ formatNumber(agent.calls) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Chart, registerables } from 'chart.js'
import SidebarNav from '@/components/SidebarNav.vue'

Chart.register(...registerables)

const router = useRouter()

// State
const selectedDateRange = ref('Last 30 Days')
const selectedChartPeriod = ref('Daily')
const chartCanvas = ref(null)
let chartInstance = null

// Metrics data
const metrics = ref([
  {
    label: 'Total Calls',
    value: '27,684',
    trend: 12.5,
    icon: 'call'
  },
  {
    label: 'Average Duration',
    value: '2m 18s',
    trend: -3.2,
    icon: 'hourglass_top'
  },
  {
    label: 'Success Rate',
    value: '92.1%',
    trend: 1.8,
    icon: 'task_alt'
  },
  {
    label: 'Total Cost',
    value: '$4,152.60',
    trend: 8.1,
    icon: 'payments'
  }
])

// Top agents data
const topAgents = ref([
  { name: 'Customer Support Bot', calls: 5821, percentage: 95 },
  { name: 'Sales Outreach Agent', calls: 4980, percentage: 80 },
  { name: 'Appointment Reminder', calls: 3120, percentage: 65 },
  { name: 'Internal Helpdesk', calls: 1530, percentage: 40 },
  { name: 'Onboarding Assistant', calls: 890, percentage: 25 }
])

// Chart data
const chartData = {
  daily: [500, 550, 600, 580, 620, 700, 750, 720, 800, 850, 900, 880, 920, 950, 1000, 980, 1020, 1100, 1150, 1120, 1200, 1250, 1300, 1280, 1320, 1400, 1450, 1420, 1500, 1550],
  weekly: [3500, 4200, 4800, 5100],
  monthly: [27684, 24500, 22100]
}

const chartLabels = {
  daily: Array.from({ length: 30 }, (_, i) => (i + 1).toString()),
  weekly: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
  monthly: ['This Month', 'Last Month', '2 Months Ago']
}

// Methods
const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const toggleDatePicker = () => {
  alert('Date picker would open here!\n\nIn the full implementation, this would show a date range picker.')
}

const handleViewAllAgents = () => {
  router.push('/dashboard')
}

const createChart = () => {
  if (!chartCanvas.value) return

  const isDarkMode = document.documentElement.classList.contains('dark')
  const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
  const textColor = isDarkMode ? '#cbd5e1' : '#475569'

  const period = selectedChartPeriod.value.toLowerCase()
  const data = chartData[period]
  const labels = chartLabels[period]

  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total Calls',
        data: data,
        borderColor: '#4182ec',
        backgroundColor: 'rgba(65, 130, 236, 0.1)',
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 5,
        pointBackgroundColor: '#4182ec',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: textColor
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: gridColor,
            borderDash: [3, 3]
          },
          ticks: {
            color: textColor
          }
        }
      }
    }
  })
}

// Watch for chart period changes
watch(selectedChartPeriod, () => {
  createChart()
})

// Lifecycle
onMounted(() => {
  createChart()

  // Watch for dark mode changes
  const observer = new MutationObserver(() => {
    createChart()
  })
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>
