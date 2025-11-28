<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="sticky top-0 backdrop-blur-sm z-10 py-4 mb-6">
          <div class="flex flex-wrap justify-between items-center gap-4">
            <h1 class="text-slate-900 dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">
              Analytics Overview
            </h1>
            <div class="flex items-center gap-3">
              <!-- Agent Filter -->
              <div class="relative">
                <select
                  v-model="selectedAgent"
                  @change="handleAgentChange"
                  class="appearance-none h-10 px-4 pr-10 border border-slate-300 dark:border-slate-700 rounded-lg text-sm font-medium text-slate-900 dark:text-white bg-white/80 backdrop-blur-md dark:bg-slate-800/80 hover:bg-slate-50 dark:hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="">All Agents</option>
                  <option v-for="agent in allAgents" :key="agent.id" :value="agent.id">
                    {{ agent.name }}
                  </option>
                </select>
                <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500 dark:text-slate-400">
                  expand_more
                </span>
              </div>

              <!-- Date Range Picker -->
              <button
                @click="toggleDatePicker"
                class="flex h-10 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-white/80 backdrop-blur-md dark:bg-slate-800/50 border border-slate-300 dark:border-slate-700 px-4 hover:bg-slate-50 dark:hover:bg-slate-800"
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
            class="bg-white/80 dark:bg-slate-900/50 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-800 p-5"
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
          <div class="lg:col-span-3 bg-white/80 dark:bg-slate-900/50 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-800 p-6">
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
          <div class="lg:col-span-2 bg-white/80 dark:bg-slate-900/50 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-800 p-6">
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
import { getAnalyticsSummary, getAnalyticsChart, getTopAgents, getAgents } from '@/services/api'

Chart.register(...registerables)

const router = useRouter()

// State
const selectedDateRange = ref('Last 30 Days')
const selectedChartPeriod = ref('Daily')
const selectedAgent = ref('') // Agent filter
const allAgents = ref([]) // List of all agents
const chartCanvas = ref(null)
let chartInstance = null
const isLoading = ref(true)

// Metrics data
const metrics = ref([
  {
    label: 'Total Calls',
    value: '0',
    trend: 0,
    icon: 'call'
  },
  {
    label: 'Average Duration',
    value: '0s',
    trend: 0,
    icon: 'hourglass_top'
  },
  {
    label: 'Success Rate',
    value: '0%',
    trend: 0,
    icon: 'task_alt'
  },
  {
    label: 'Total Cost',
    value: '$0.00',
    trend: 0,
    icon: 'payments'
  }
])

// Top agents data
const topAgents = ref([])

// Chart data
const chartData = ref([])
const chartLabels = ref([])

// Methods
const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const formatDuration = (seconds) => {
  if (!seconds) return '0s'
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.round(seconds % 60)
  if (minutes === 0) return `${remainingSeconds}s`
  return `${minutes}m ${remainingSeconds}s`
}

const toggleDatePicker = () => {
  // In a real app, this would open a date picker
  // For now, we just toggle between 30d and 7d for demo
  if (selectedDateRange.value === 'Last 30 Days') {
    selectedDateRange.value = 'Last 7 Days'
    loadData('7d')
  } else {
    selectedDateRange.value = 'Last 30 Days'
    loadData('30d')
  }
}

const handleViewAllAgents = () => {
  router.push('/dashboard')
}

const loadData = async (range = '30d') => {
  isLoading.value = true
  try {
    // Load all agents list (for dropdown)
    if (allAgents.value.length === 0) {
      const agentsData = await getAgents()
      allAgents.value = agentsData || []
    }

    // If agent filter is selected, we need to fetch raw call_logs and calculate manually
    if (selectedAgent.value) {
      await loadDataForAgent(range, selectedAgent.value)
    } else {
      await loadDataAllAgents(range)
    }

  } catch (error) {
    console.error('Failed to load analytics data:', error)
  } finally {
    isLoading.value = false
  }
}

// Load data for all agents (uses existing backend functions)
const loadDataAllAgents = async (range) => {
  // 1. Fetch Summary
  const summary = await getAnalyticsSummary(range)

  if (summary) {
    metrics.value = [
      {
        label: 'Total Calls',
        value: formatNumber(summary.total_calls || 0),
        trend: summary.call_trend || 0,
        icon: 'call'
      },
      {
        label: 'Average Duration',
        value: formatDuration(summary.avg_duration_seconds || 0),
        trend: 0,
        icon: 'hourglass_top'
      },
      {
        label: 'Success Rate',
        value: (summary.success_rate || 0) + '%',
        trend: 0,
        icon: 'task_alt'
      },
      {
        label: 'Total Cost',
        value: '$' + (summary.total_cost || 0),
        trend: 0,
        icon: 'payments'
      }
    ]
  }

  // 2. Fetch Top Agents
  const agents = await getTopAgents()
  const maxCalls = Math.max(...agents.map(a => a.call_count), 1)
  topAgents.value = agents.map(a => ({
    name: a.agent_name,
    calls: a.call_count,
    percentage: Math.round((a.call_count / maxCalls) * 100)
  }))

  // 3. Fetch Chart Data
  const period = selectedChartPeriod.value.toLowerCase()
  const chartRawData = await getAnalyticsChart(period)

  // Format labels based on period
  chartLabels.value = chartRawData.map(d => {
    const timestamp = d.hour || d.day // hourly data has 'hour', daily has 'day'
    const date = new Date(timestamp)

    if (period === 'daily') {
      // Hourly format: "2:00 PM"
      return date.toLocaleTimeString(undefined, {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      })
    } else {
      // Daily format: "Nov 24"
      return date.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric'
      })
    }
  })
  chartData.value = chartRawData.map(d => d.count)

  createChart()
}

// Load data for specific agent (uses call_logs API with filter)
const loadDataForAgent = async (range, agentId) => {
  const { getCallLogs } = await import('@/services/api')

  // Calculate date range
  const now = new Date()
  const startDate = new Date(now)
  if (range === '7d') {
    startDate.setDate(now.getDate() - 7)
  } else if (range === '90d') {
    startDate.setDate(now.getDate() - 90)
  } else {
    startDate.setDate(now.getDate() - 30)
  }

  // Fetch call logs for this agent
  const response = await getCallLogs({
    agent_id: agentId,
    date_from: startDate.toISOString().split('T')[0],
    date_to: now.toISOString().split('T')[0],
    limit: 1000 // Get all calls for accurate stats
  })

  const calls = response.calls || []

  // Calculate metrics manually
  const totalCalls = calls.length
  const completedCalls = calls.filter(c => c.status === 'completed').length
  const totalDuration = calls.reduce((sum, c) => sum + (c.duration_seconds || 0), 0)
  const avgDuration = totalCalls > 0 ? totalDuration / totalCalls : 0
  const successRate = totalCalls > 0 ? (completedCalls / totalCalls) * 100 : 0
  const totalCost = calls.reduce((sum, c) => sum + (c.cost || 0), 0)

  metrics.value = [
    {
      label: 'Total Calls',
      value: formatNumber(totalCalls),
      trend: 0,
      icon: 'call'
    },
    {
      label: 'Average Duration',
      value: formatDuration(avgDuration),
      trend: 0,
      icon: 'hourglass_top'
    },
    {
      label: 'Success Rate',
      value: Math.round(successRate) + '%',
      trend: 0,
      icon: 'task_alt'
    },
    {
      label: 'Total Cost',
      value: '$' + totalCost.toFixed(2),
      trend: 0,
      icon: 'payments'
    }
  ]

  // Top agents: Only show the selected agent
  const selectedAgentData = allAgents.value.find(a => a.id === agentId)
  topAgents.value = selectedAgentData ? [{
    name: selectedAgentData.name,
    calls: totalCalls,
    percentage: 100
  }] : []

  // Chart data: Group calls by hour (daily) or day (weekly/monthly)
  const period = selectedChartPeriod.value.toLowerCase()
  const callsByTime = {}

  calls.forEach(call => {
    if (!call.start_time) return

    const date = new Date(call.start_time)
    let key

    if (period === 'daily') {
      // Group by hour for intraday chart
      key = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours()).toISOString()
    } else {
      // Group by day
      key = call.start_time.split('T')[0]
    }

    callsByTime[key] = (callsByTime[key] || 0) + 1
  })

  const sortedTimes = Object.keys(callsByTime).sort()
  chartLabels.value = sortedTimes.map(t => {
    const date = new Date(t)

    if (period === 'daily') {
      // Hourly format: "2:00 PM"
      return date.toLocaleTimeString(undefined, {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      })
    } else {
      // Daily format: "Nov 24"
      return date.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric'
      })
    }
  })
  chartData.value = sortedTimes.map(t => callsByTime[t])

  createChart()
}

// Handle agent filter change
const handleAgentChange = () => {
  const range = selectedDateRange.value === 'Last 30 Days' ? '30d' : '7d'
  loadData(range)
}

const createChart = () => {
  if (!chartCanvas.value) return

  const isDarkMode = document.documentElement.classList.contains('dark')
  const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
  const textColor = isDarkMode ? '#cbd5e1' : '#475569'

  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')

  // Create gradient for professional look
  const gradient = ctx.createLinearGradient(0, 0, 0, 400)
  gradient.addColorStop(0, 'rgba(65, 130, 236, 0.25)')
  gradient.addColorStop(0.5, 'rgba(65, 130, 236, 0.1)')
  gradient.addColorStop(1, 'rgba(65, 130, 236, 0)')

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartLabels.value,
      datasets: [{
        label: 'Calls',
        data: chartData.value,
        borderColor: '#4182ec',
        backgroundColor: gradient,
        borderWidth: 3,
        pointRadius: 4,
        pointHoverRadius: 7,
        pointBackgroundColor: '#4182ec',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverBackgroundColor: '#4182ec',
        pointHoverBorderColor: '#fff',
        pointHoverBorderWidth: 3,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'end',
          labels: {
            boxWidth: 8,
            boxHeight: 8,
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 15,
            color: textColor,
            font: {
              size: 13,
              weight: '600',
              family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
            }
          }
        },
        tooltip: {
          enabled: true,
          backgroundColor: isDarkMode ? 'rgba(15, 23, 42, 0.95)' : 'rgba(255, 255, 255, 0.95)',
          titleColor: textColor,
          bodyColor: textColor,
          borderColor: gridColor,
          borderWidth: 1,
          padding: 12,
          boxPadding: 6,
          usePointStyle: true,
          titleFont: {
            size: 13,
            weight: '600',
            family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
          },
          bodyFont: {
            size: 14,
            weight: '700',
            family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
          },
          callbacks: {
            title: function(context) {
              return context[0].label
            },
            label: function(context) {
              const value = context.parsed.y
              return ` ${value} ${value === 1 ? 'call' : 'calls'}`
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: true,
            color: isDarkMode ? 'rgba(51, 65, 85, 0.3)' : 'rgba(226, 232, 240, 0.8)',
            lineWidth: 1,
            drawBorder: false
          },
          ticks: {
            color: textColor,
            maxTicksLimit: 10,
            font: {
              size: 11,
              weight: '500',
              family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
            },
            padding: 8
          },
          border: {
            display: false
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: isDarkMode ? 'rgba(51, 65, 85, 0.3)' : 'rgba(226, 232, 240, 0.8)',
            lineWidth: 1,
            drawBorder: false
          },
          ticks: {
            color: textColor,
            precision: 0,
            font: {
              size: 11,
              weight: '500',
              family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
            },
            padding: 8,
            callback: function(value) {
              return value >= 1000 ? (value / 1000).toFixed(1) + 'k' : value
            }
          },
          border: {
            display: false
          }
        }
      },
      animation: {
        duration: 750,
        easing: 'easeInOutQuart'
      }
    }
  })
}

// Watch for chart period changes
watch(selectedChartPeriod, () => {
  loadData(selectedDateRange.value === 'Last 30 Days' ? '30d' : '7d')
})

// Lifecycle
onMounted(() => {
  loadData()

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
