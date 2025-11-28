<template>
  <div class="flex min-h-screen">
    <!-- Sidebar Navigation -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-4 sm:p-6 lg:p-8">
      <div class="max-w-7xl mx-auto">
        <!-- Breadcrumbs -->
        <div class="flex flex-wrap gap-2 mb-4">
          <router-link
            to="/dashboard"
            class="text-subtext-light dark:text-subtext-dark hover:text-primary text-base font-medium"
          >
            Agents
          </router-link>
          <span class="text-subtext-light dark:text-subtext-dark text-base font-medium">/</span>
          <span class="text-text-light dark:text-text-dark text-base font-medium">{{ agentName }}</span>
        </div>

        <!-- Page Heading -->
        <div class="flex flex-wrap items-start justify-between gap-4 mb-6">
          <div class="flex min-w-72 flex-col gap-3">
            <p class="text-4xl font-black leading-tight tracking-[-0.033em]">{{ agentName }}</p>
            <p class="text-subtext-light dark:text-subtext-dark text-base font-normal">
              View and manage agent details and performance.
            </p>
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="handleTestAgent"
              class="flex min-w-[84px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold"
            >
              <span>Test Agent</span>
            </button>
            <button
              @click="handleEditAgent"
              class="flex min-w-[84px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 bg-surface-light dark:bg-surface-dark border border-border-light dark:border-border-dark text-text-light dark:text-text-dark text-sm font-bold"
            >
              <span>Edit</span>
            </button>
          </div>
        </div>

        <!-- Status Badges -->
        <div class="flex gap-3 flex-wrap pr-4 mb-8">
          <div class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-success/20 text-success pl-2 pr-3">
            <span class="material-symbols-outlined text-base">check_circle</span>
            <p class="text-sm font-medium">{{ agentStatus }}</p>
          </div>
          <div class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-primary/20 text-primary pl-2 pr-3">
            <span class="material-symbols-outlined text-base">layers</span>
            <p class="text-sm font-medium">{{ agentTemplate }}</p>
          </div>
          <div class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-primary/20 text-primary pl-2 pr-3">
            <span class="material-symbols-outlined text-base">phone</span>
            <p class="text-sm font-medium">{{ agentPhone }}</p>
          </div>
        </div>

        <!-- Live Status & Metrics Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <!-- Live Status Panel -->
          <div class="lg:col-span-1 bg-surface-light/80 dark:bg-surface-dark/80 backdrop-blur-md p-6 rounded-xl border border-border-light dark:border-border-dark flex flex-col justify-center items-center text-center">
            <span class="material-symbols-outlined text-4xl text-subtext-light dark:text-subtext-dark mb-2">
              phone_in_talk
            </span>
            <p class="font-bold text-lg">Live Status: {{ liveStatus }}</p>
            <p class="text-subtext-light dark:text-subtext-dark">{{ liveStatusDetail }}</p>
            <p class="text-sm mt-2">{{ liveStatusDuration }}</p>
          </div>

          <!-- Key Metrics Cards -->
          <div class="lg:col-span-2 grid grid-cols-2 md:grid-cols-3 gap-6">
            <div class="bg-surface-light/80 dark:bg-surface-dark/80 backdrop-blur-md p-6 rounded-xl border border-border-light dark:border-border-dark">
              <h3 class="text-subtext-light dark:text-subtext-dark text-sm font-medium mb-2">Total Calls (24h)</h3>
              <p class="text-3xl font-bold">{{ metrics.totalCalls }}</p>
              <div class="flex items-center text-sm mt-1" :class="metrics.totalCallsTrend > 0 ? 'text-success' : 'text-danger'">
                <span class="material-symbols-outlined text-base">
                  {{ metrics.totalCallsTrend > 0 ? 'arrow_upward' : 'arrow_downward' }}
                </span>
                <span>{{ Math.abs(metrics.totalCallsTrend) }}%</span>
              </div>
            </div>

            <div class="bg-surface-light/80 dark:bg-surface-dark/80 backdrop-blur-md p-6 rounded-xl border border-border-light dark:border-border-dark">
              <h3 class="text-subtext-light dark:text-subtext-dark text-sm font-medium mb-2">Avg. Call Duration</h3>
              <p class="text-3xl font-bold">{{ metrics.avgDuration }}</p>
              <div class="flex items-center text-sm mt-1" :class="metrics.avgDurationTrend > 0 ? 'text-danger' : 'text-success'">
                <span class="material-symbols-outlined text-base">
                  {{ metrics.avgDurationTrend > 0 ? 'arrow_upward' : 'arrow_downward' }}
                </span>
                <span>{{ Math.abs(metrics.avgDurationTrend) }}%</span>
              </div>
            </div>

            <div class="bg-surface-light/80 dark:bg-surface-dark/80 backdrop-blur-md p-6 rounded-xl border border-border-light dark:border-border-dark">
              <h3 class="text-subtext-light dark:text-subtext-dark text-sm font-medium mb-2">Success Rate</h3>
              <p class="text-3xl font-bold">{{ metrics.successRate }}%</p>
              <div class="flex items-center text-sm mt-1" :class="metrics.successRateTrend > 0 ? 'text-success' : 'text-danger'">
                <span class="material-symbols-outlined text-base">
                  {{ metrics.successRateTrend > 0 ? 'arrow_upward' : 'arrow_downward' }}
                </span>
                <span>{{ Math.abs(metrics.successRateTrend) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Chart -->
        <div class="bg-surface-light/80 dark:bg-surface-dark/80 backdrop-blur-md p-6 rounded-xl border border-border-light dark:border-border-dark mb-8">
          <div class="flex flex-wrap justify-between items-center mb-4 gap-4">
            <h3 class="text-lg font-bold">Call Volume</h3>
            <div class="flex items-center gap-1 bg-background-light dark:bg-background-dark p-1 rounded-lg border border-border-light dark:border-border-dark">
              <button
                v-for="period in ['24h', '7d', '30d']"
                :key="period"
                @click="selectedPeriod = period"
                class="px-3 py-1 text-sm font-medium rounded-md transition-colors"
                :class="selectedPeriod === period ? 'bg-surface-light dark:bg-surface-dark' : 'text-subtext-light dark:text-subtext-dark'"
              >
                {{ period }}
              </button>
            </div>
          </div>
          <!-- Chart Placeholder -->
          <div class="h-80 flex items-center justify-center bg-background-light dark:bg-background-dark rounded-lg">
            <div class="text-center">
              <span class="material-symbols-outlined text-6xl text-subtext-light dark:text-subtext-dark mb-2">
                analytics
              </span>
              <p class="text-subtext-light dark:text-subtext-dark">Chart visualization would be rendered here</p>
              <p class="text-sm text-subtext-light dark:text-subtext-dark mt-1">
                (Integration with Chart.js or similar library)
              </p>
            </div>
          </div>
        </div>

        <!-- Recent Calls Table -->
        <div>
          <h3 class="text-lg font-bold mb-4">Recent Calls</h3>
          <div class="bg-surface-light/80 dark:bg-surface-dark/80 backdrop-blur-md rounded-xl border border-border-light dark:border-border-dark overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm">
                <thead class="bg-background-light dark:bg-background-dark text-subtext-light dark:text-subtext-dark uppercase tracking-wider">
                  <tr>
                    <th class="p-4 font-medium">Call ID</th>
                    <th class="p-4 font-medium">From</th>
                    <th class="p-4 font-medium">Timestamp</th>
                    <th class="p-4 font-medium">Duration</th>
                    <th class="p-4 font-medium">Status</th>
                    <th class="p-4 font-medium"></th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-border-light dark:divide-border-dark">
                  <tr v-for="call in recentCalls" :key="call.id">
                    <td class="p-4">#{{ call.id }}</td>
                    <td class="p-4">{{ call.from }}</td>
                    <td class="p-4">{{ call.timestamp }}</td>
                    <td class="p-4">{{ call.duration }}</td>
                    <td class="p-4">
                      <span
                        class="inline-flex items-center px-2 py-1 text-xs font-medium rounded-full"
                        :class="{
                          'bg-success/20 text-success': call.status === 'Completed',
                          'bg-danger/20 text-danger': call.status === 'Failed',
                          'bg-warning/20 text-warning': call.status === 'Ongoing'
                        }"
                      >
                        {{ call.status }}
                      </span>
                    </td>
                    <td class="p-4 text-right">
                      <button
                        @click="handleViewCallDetails(call)"
                        class="text-primary hover:underline font-medium"
                      >
                        Details
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="p-4 flex justify-between items-center text-sm border-t border-border-light dark:border-border-dark">
              <span class="text-subtext-light dark:text-subtext-dark">
                Showing {{ paginationStart }}-{{ paginationEnd }} of {{ totalCalls }} calls
              </span>
              <div class="flex gap-1">
                <button
                  @click="handlePreviousPage"
                  :disabled="currentPage === 1"
                  class="px-3 py-1 border border-border-light dark:border-border-dark rounded-md hover:bg-primary/10 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <button
                  @click="handleNextPage"
                  :disabled="paginationEnd >= totalCalls"
                  class="px-3 py-1 border border-border-light dark:border-border-dark rounded-md hover:bg-primary/10 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'

const route = useRoute()
const router = useRouter()

// Agent basic info
const agentName = ref(route.query.name || 'Support Agent Alpha')
const agentStatus = ref('Active')
const agentTemplate = ref('Customer Support Template')
const agentPhone = ref('+1 (555) 123-4567')

// Live status
const liveStatus = ref('On a Call')
const liveStatusDetail = ref('with +1 (555) 987-6543')
const liveStatusDuration = ref('Duration: 02:34')

// Metrics
const metrics = ref({
  totalCalls: '1,204',
  totalCallsTrend: 5.2,
  avgDuration: '3m 15s',
  avgDurationTrend: -1.8,
  successRate: 92,
  successRateTrend: 0.5
})

// Chart period selection
const selectedPeriod = ref('24h')

// Recent calls data
const recentCalls = ref([
  {
    id: '82021',
    from: '+1 (555) 876-5432',
    timestamp: '2 min ago',
    duration: '4m 12s',
    status: 'Completed'
  },
  {
    id: '82020',
    from: '+1 (555) 234-5678',
    timestamp: '15 min ago',
    duration: '2m 05s',
    status: 'Completed'
  },
  {
    id: '82019',
    from: '+1 (555) 345-6789',
    timestamp: '28 min ago',
    duration: '1m 30s',
    status: 'Failed'
  },
  {
    id: '82018',
    from: '+1 (555) 456-7890',
    timestamp: '1 hour ago',
    duration: '5m 55s',
    status: 'Completed'
  }
])

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(4)
const totalCalls = ref(56)

const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage.value + 1)
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage.value, totalCalls.value))

// Actions
const handleTestAgent = () => {
  alert('Test Agent feature!\n\nThis will initiate a test call to the agent.')
}

const handleEditAgent = () => {
  router.push(`/agents/configure?id=${route.params.id}`)
}

const handleViewCallDetails = (call) => {
  console.log('View call details:', call)
  alert(`Call Details: #${call.id}\n\nFrom: ${call.from}\nDuration: ${call.duration}\nStatus: ${call.status}\n\nThis will open a detailed call view in the full implementation.`)
}

const handlePreviousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    // In real implementation, fetch new data
  }
}

const handleNextPage = () => {
  if (paginationEnd.value < totalCalls.value) {
    currentPage.value++
    // In real implementation, fetch new data
  }
}
</script>
