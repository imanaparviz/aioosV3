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
            class="inline-flex items-center justify-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 dark:ring-offset-background-dark"
          >
            <span class="material-symbols-outlined">download</span>
            <span>Export</span>
          </button>
        </div>

        <!-- Filters -->
        <div class="mb-6 rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900/50">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
            <!-- Agent Filter -->
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300" for="agent-filter">
                Agent
              </label>
              <select
                v-model="filters.agent"
                class="w-full rounded-md border-gray-300 bg-white text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                id="agent-filter"
              >
                <option value="">All Agents</option>
                <option value="olivia">Olivia Martin</option>
                <option value="liam">Liam Harris</option>
                <option value="sophia">Sophia King</option>
              </select>
            </div>

            <!-- Department Filter -->
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300" for="department-filter">
                Department
              </label>
              <select
                v-model="filters.department"
                class="w-full rounded-md border-gray-300 bg-white text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white"
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
                class="w-full rounded-md border-gray-300 bg-white text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white"
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
                class="w-full rounded-md border-gray-300 bg-white text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white"
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
                class="w-full rounded-md border-gray-300 bg-white text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white"
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
                  class="w-full rounded-md border-gray-300 bg-white pl-10 text-sm text-gray-900 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                  id="search"
                  placeholder="Search caller ID..."
                  type="search"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-hidden rounded-lg border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900/50">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
              <thead class="bg-gray-50 dark:bg-gray-900">
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
              <tbody class="divide-y divide-gray-200 bg-white dark:divide-gray-800 dark:bg-gray-900/50">
                <tr v-for="log in paginatedLogs" :key="log.id">
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
          <div class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 dark:border-gray-800 dark:bg-gray-900/50 sm:px-6">
            <div class="flex flex-1 justify-between sm:hidden">
              <button
                @click="previousPage"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300"
              >
                Previous
              </button>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300"
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
import { ref, computed } from 'vue'
import SidebarNav from '@/components/SidebarNav.vue'

// Filters
const filters = ref({
  agent: '',
  department: '',
  dateRange: 'Oct 1, 2023 - Oct 31, 2023',
  outcome: '',
  duration: '',
  search: ''
})

// Mock data
const callLogs = ref([
  {
    id: 1,
    callerId: '+1 (555) 123-4567',
    agent: 'Olivia Martin',
    department: 'Support',
    startTime: 'Oct 26, 2023, 10:15 AM',
    duration: '02:35',
    outcome: 'Completed'
  },
  {
    id: 2,
    callerId: '+1 (555) 987-6543',
    agent: 'Liam Harris',
    department: 'Sales',
    startTime: 'Oct 26, 2023, 10:12 AM',
    duration: '05:12',
    outcome: 'Transferred'
  },
  {
    id: 3,
    callerId: '+1 (555) 234-5678',
    agent: 'Sophia King',
    department: 'Support',
    startTime: 'Oct 26, 2023, 10:05 AM',
    duration: '00:45',
    outcome: 'Hung Up'
  },
  {
    id: 4,
    callerId: '+1 (555) 876-5432',
    agent: 'Olivia Martin',
    department: 'Billing',
    startTime: 'Oct 26, 2023, 09:58 AM',
    duration: '01:15',
    outcome: 'Error'
  },
  // Add more mock entries to demonstrate pagination
  ...Array.from({ length: 93 }, (_, i) => ({
    id: i + 5,
    callerId: `+1 (555) ${String(Math.floor(Math.random() * 900) + 100)}-${String(Math.floor(Math.random() * 9000) + 1000)}`,
    agent: ['Olivia Martin', 'Liam Harris', 'Sophia King'][i % 3],
    department: ['Support', 'Sales', 'Billing'][i % 3],
    startTime: `Oct ${26 - Math.floor(i / 10)}, 2023, ${String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')}:${String(Math.floor(Math.random() * 60)).padStart(2, '0')} AM`,
    duration: `0${Math.floor(Math.random() * 5)}:${String(Math.floor(Math.random() * 60)).padStart(2, '0')}`,
    outcome: ['Completed', 'Transferred', 'Hung Up', 'Error'][Math.floor(Math.random() * 4)]
  }))
])

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

const totalLogs = computed(() => callLogs.value.length)
const totalPages = computed(() => Math.ceil(totalLogs.value / itemsPerPage.value))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value)
const endIndex = computed(() => currentPage.value * itemsPerPage.value)

const paginatedLogs = computed(() => {
  return callLogs.value.slice(startIndex.value, endIndex.value)
})

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
const getOutcomeBadgeClass = (outcome) => {
  const classes = {
    'Completed': 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300',
    'Transferred': 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
    'Hung Up': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300',
    'Error': 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300'
  }
  return classes[outcome] || ''
}

const handleExport = () => {
  alert('Export functionality!\n\nIn the full implementation, this would export the call logs to CSV/Excel.')
}

const handlePlayRecording = (log) => {
  console.log('Play recording:', log)
  alert(`Play Recording\n\nCall ID: ${log.callerId}\nAgent: ${log.agent}\n\nThis would play the call recording.`)
}

const handleViewTranscript = (log) => {
  console.log('View transcript:', log)
  alert(`View Transcript\n\nCall ID: ${log.callerId}\nAgent: ${log.agent}\n\nThis would show the call transcript.`)
}

const handleMoreActions = (log) => {
  console.log('More actions:', log)
  alert(`More Actions\n\nCall ID: ${log.callerId}\n\nOptions:\n- Download Recording\n- Share\n- Delete\n- Add to Report`)
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page) => {
  if (page !== '...' && page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
</script>
