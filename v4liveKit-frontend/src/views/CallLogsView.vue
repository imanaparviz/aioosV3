<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-4 md:p-6 lg:p-8">
      <div class="mx-auto max-w-7xl">
        <!-- Header -->
        <div class="mb-6 flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
          <div class="flex flex-col gap-1">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Call Logs</h1>
            <p class="text-gray-600 dark:text-gray-400">Review and manage all recorded calls.</p>
          </div>
          <button
            @click="handleExport"
            :disabled="isExporting"
            class="inline-flex items-center justify-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 dark:ring-offset-background-dark disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="material-symbols-outlined">{{ isExporting ? 'hourglass_top' : 'download' }}</span>
            <span>{{ isExporting ? 'Exporting...' : 'Export' }}</span>
          </button>
        </div>

        <!-- Filters -->
        <div class="mb-6 rounded-lg border border-gray-200 bg-white/80 backdrop-blur-md p-4 dark:border-gray-800 dark:bg-gray-900/50">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
            <!-- Agent Filter -->
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300" for="agent-filter">
                Agent
              </label>
              <select
                v-model="filters.agent"
                @change="applyFilters"
                class="w-full rounded-md border-gray-300 bg-white/80 backdrop-blur-md text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800/80 dark:text-white"
                id="agent-filter"
              >
                <option value="">All Agents</option>
                <option v-for="agent in agents" :key="agent.id" :value="agent.id">
                  {{ agent.name }}
                </option>
              </select>
            </div>

            <!-- Department Filter -->
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300" for="department-filter">
                Department
              </label>
              <select
                v-model="filters.department"
                @change="applyFilters"
                class="w-full rounded-md border-gray-300 bg-white/80 backdrop-blur-md text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800/80 dark:text-white"
                id="department-filter"
              >
                <option value="">All Departments</option>
                <option value="sales">Sales</option>
                <option value="support">Support</option>
                <option value="billing">Billing</option>
              </select>
            </div>

            <!-- Date Range Filter -->
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300" for="date-range-filter">
                Date Range
              </label>
              <input
                v-model="filters.dateRange"
                @change="applyFilters"
                class="w-full rounded-md border-gray-300 bg-white/80 backdrop-blur-md text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800/80 dark:text-white"
                id="date-range-filter"
                placeholder="Select date range"
                type="text"
              />
            </div>

            <!-- Outcome Filter -->
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300" for="outcome-filter">
                Outcome
              </label>
              <select
                v-model="filters.outcome"
                @change="applyFilters"
                class="w-full rounded-md border-gray-300 bg-white/80 backdrop-blur-md text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800/80 dark:text-white"
                id="outcome-filter"
              >
                <option value="">All Outcomes</option>
                <option value="completed">Completed</option>
                <option value="transferred">Transferred</option>
                <option value="hung_up">Hung Up</option>
                <option value="error">Error</option>
              </select>
            </div>

            <!-- Duration Filter -->
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300" for="duration-filter">
                Duration
              </label>
              <select
                v-model="filters.duration"
                @change="applyFilters"
                class="w-full rounded-md border-gray-300 bg-white/80 backdrop-blur-md text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800/80 dark:text-white"
                id="duration-filter"
              >
                <option value="">Any Duration</option>
                <option value="short">&lt; 1 min</option>
                <option value="medium">1-5 min</option>
                <option value="long">&gt; 5 min</option>
              </select>
            </div>

            <!-- Search -->
            <div class="flex flex-col gap-1.5 xl:col-span-1">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300" for="search">
                Search
              </label>
              <div class="relative">
                <span class="material-symbols-outlined pointer-events-none absolute inset-y-0 left-3 flex items-center text-gray-500">
                  search
                </span>
                <input
                  v-model="filters.search"
                  @input="debouncedSearch"
                  class="w-full rounded-md border-gray-300 bg-white/80 backdrop-blur-md pl-10 text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800/80 dark:text-white"
                  id="search"
                  placeholder="Search caller ID..."
                  type="search"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="flex items-center justify-center py-12">
          <div class="text-center">
            <span class="material-symbols-outlined animate-spin text-4xl text-primary">refresh</span>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">Loading call logs...</p>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="!isLoading && callLogs.length === 0" class="rounded-lg border border-gray-200 bg-white/80 backdrop-blur-md p-12 text-center dark:border-gray-800 dark:bg-gray-900/50">
          <span class="material-symbols-outlined text-6xl text-gray-400">call</span>
          <h3 class="mt-4 text-lg font-semibold text-gray-900 dark:text-white">No call logs found</h3>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            {{ filters.search || filters.agent || filters.outcome ? 'Try adjusting your filters' : 'Make a test call to see data here' }}
          </p>
        </div>

        <!-- Table -->
        <div v-else class="overflow-hidden rounded-lg border border-gray-200 bg-white/80 backdrop-blur-md dark:border-gray-800 dark:bg-gray-900/50">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
              <thead class="bg-gray-50/80 backdrop-blur-md dark:bg-gray-900">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">
                    Caller ID
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">
                    Agent
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">
                    Department
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">
                    Start Time
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">
                    Duration
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">
                    Outcome
                  </th>
                  <th class="relative px-6 py-3" scope="col">
                    <span class="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 bg-white/80 backdrop-blur-md dark:divide-gray-800 dark:bg-gray-900/50">
                <tr v-for="log in callLogs" :key="log.id">
                  <td class="whitespace-nowrap px-6 py-4 text-sm font-medium">
                    <router-link
                      :to="`/call-logs/${log.id}`"
                      class="text-primary hover:text-primary/80 hover:underline"
                    >
                      {{ log.callerId }}
                    </router-link>
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {{ log.agent }}
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {{ log.department }}
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {{ log.startTime }}
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {{ log.duration }}
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm">
                    <span
                      class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                      :class="getOutcomeBadgeClass(log.outcome)"
                    >
                      {{ log.outcome }}
                    </span>
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-right text-sm font-medium">
                    <div class="flex items-center justify-end gap-4">
                      <button
                        @click="handlePlayRecording(log)"
                        class="text-gray-500 hover:text-primary dark:text-gray-400 dark:hover:text-primary"
                        title="Play recording"
                      >
                        <span class="material-symbols-outlined">play_circle</span>
                      </button>
                      <button
                        @click="handleViewTranscript(log)"
                        class="text-gray-500 hover:text-primary dark:text-gray-400 dark:hover:text-primary"
                        title="View transcript"
                      >
                        <span class="material-symbols-outlined">description</span>
                      </button>
                      <button
                        @click="handleMoreActions(log)"
                        class="text-gray-500 hover:text-primary dark:text-gray-400 dark:hover:text-primary"
                        title="More actions"
                      >
                        <span class="material-symbols-outlined">more_vert</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="flex items-center justify-between border-t border-gray-200 bg-white/80 backdrop-blur-md px-4 py-3 dark:border-gray-800 dark:bg-gray-900/50 sm:px-6">
            <div class="flex flex-1 justify-between sm:hidden">
              <button
                @click="previousPage"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center rounded-md border border-gray-300 bg-white/80 backdrop-blur-md px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800/80 dark:text-gray-300"
              >
                Previous
              </button>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white/80 backdrop-blur-md px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800/80 dark:text-gray-300"
              >
                Next
              </button>
            </div>
            <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700 dark:text-gray-400">
                  Showing
                  <span class="font-medium">{{ startIndex + 1 }}</span>
                  to
                  <span class="font-medium">{{ Math.min(endIndex, totalLogs) }}</span>
                  of
                  <span class="font-medium">{{ totalLogs }}</span>
                  results
                </p>
              </div>
              <div>
                <nav aria-label="Pagination" class="isolate inline-flex -space-x-px rounded-md shadow-sm">
                  <button
                    @click="previousPage"
                    :disabled="currentPage === 1"
                    class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:ring-gray-700 dark:hover:bg-gray-800"
                  >
                    <span class="sr-only">Previous</span>
                    <span class="material-symbols-outlined">chevron_left</span>
                  </button>

                  <button
                    v-for="page in visiblePages"
                    :key="page"
                    @click="goToPage(page)"
                    :class="page === currentPage
                      ? 'relative z-10 inline-flex items-center bg-primary px-4 py-2 text-sm font-semibold text-white'
                      : 'relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 dark:text-gray-300 dark:ring-gray-700 dark:hover:bg-gray-800'"
                  >
                    {{ page === '...' ? '...' : page }}
                  </button>

                  <button
                    @click="nextPage"
                    :disabled="currentPage === totalPages"
                    class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:ring-gray-700 dark:hover:bg-gray-800"
                  >
                    <span class="sr-only">Next</span>
                    <span class="material-symbols-outlined">chevron_right</span>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import SidebarNav from '@/components/SidebarNav.vue'
import { getCallLogs, getAgents, exportCallLogs } from '@/services/api'

// State
const callLogs = ref([])
const agents = ref([])
const isLoading = ref(true)
const isExporting = ref(false)

// Filters
const filters = ref({
  agent: '',
  department: '',
  dateRange: '',
  outcome: '',
  duration: '',
  search: ''
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalLogs = ref(0)

const totalPages = computed(() => Math.ceil(totalLogs.value / itemsPerPage.value))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value)
const endIndex = computed(() => currentPage.value * itemsPerPage.value)

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')

    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
      pages.push(i)
    }

    if (current < total - 2) pages.push('...')
    pages.push(total)
  }

  return pages
})

// Methods
const loadCallLogs = async () => {
  isLoading.value = true
  try {
    const params = {
      limit: itemsPerPage.value,
      offset: startIndex.value
    }

    // Apply filters
    if (filters.value.agent) params.agent_id = filters.value.agent
    if (filters.value.department) params.department = filters.value.department
    if (filters.value.outcome) params.status = filters.value.outcome
    if (filters.value.duration) params.duration_filter = filters.value.duration
    if (filters.value.search) params.search = filters.value.search
    // TODO: Add date range parsing

    const response = await getCallLogs(params)
    callLogs.value = response.calls || []
    totalLogs.value = response.total || 0

  } catch (error) {
    console.error('Failed to load call logs:', error)
    callLogs.value = []
    totalLogs.value = 0
  } finally {
    isLoading.value = false
  }
}

const loadAgents = async () => {
  try {
    agents.value = await getAgents()
  } catch (error) {
    console.error('Failed to load agents:', error)
    agents.value = []
  }
}

const applyFilters = () => {
  currentPage.value = 1
  loadCallLogs()
}

// Debounced search
let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
}

const handleExport = async () => {
  isExporting.value = true
  try {
    await exportCallLogs({
      agent_id: filters.value.agent,
      // Add other filters as needed
    })
  } catch (error) {
    console.error('Export failed:', error)
    alert('Failed to export call logs. Please try again.')
  } finally {
    isExporting.value = false
  }
}

const getOutcomeBadgeClass = (outcome) => {
  const classes = {
    'Completed': 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300',
    'Transferred': 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
    'Hung Up': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300',
    'Error': 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300',
    'Failed': 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300'
  }
  return classes[outcome] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/50 dark:text-gray-300'
}

const handlePlayRecording = (log) => {
  console.log('Play recording:', log)
  // TODO: Implement recording playback
  alert(`Play Recording\n\nCall ID: ${log.callerId}\nAgent: ${log.agent}\n\n[Feature Coming Soon]\n\nThis will play the call recording once LiveKit recording is configured.`)
}

const handleViewTranscript = (log) => {
  console.log('View transcript:', log)
  // TODO: Implement transcript view
  alert(`View Transcript\n\nCall ID: ${log.callerId}\nAgent: ${log.agent}\n\n[Feature Coming Soon]\n\nThis will show the call transcript once STT transcription is saved to database.`)
}

const handleMoreActions = (log) => {
  console.log('More actions:', log)
  // TODO: Implement actions menu
  alert(`More Actions\n\nCall ID: ${log.callerId}\n\n[Feature Coming Soon]\n\nOptions:\n- Download Recording\n- Share Link\n- Delete Call\n- Add to Report\n- Export Transcript`)
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    loadCallLogs()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadCallLogs()
  }
}

const goToPage = (page) => {
  if (page !== '...' && page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadCallLogs()
  }
}

// Lifecycle
onMounted(() => {
  loadAgents()
  loadCallLogs()
})
</script>
