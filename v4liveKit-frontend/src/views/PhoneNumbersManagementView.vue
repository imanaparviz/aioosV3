<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-6 lg:p-8">
      <div class="mx-auto max-w-7xl">
        <!-- Page Heading -->
        <div class="flex flex-wrap items-center justify-between gap-4">
          <h1 class="text-text-light dark:text-text-dark text-3xl font-black leading-tight tracking-[-0.033em]">
            Phone Number Management
          </h1>
          <button
            @click="handleAcquireNumber"
            class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-10 px-5 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 transition-colors"
          >
            <span class="material-symbols-outlined mr-2">add</span>
            <span class="truncate">Acquire New Number</span>
          </button>
        </div>

        <!-- Control Bar -->
        <div class="mt-8 flex flex-col gap-4">
          <!-- Search Bar -->
          <div>
            <label class="flex flex-col min-w-40 h-12 w-full">
              <div class="flex w-full flex-1 items-stretch rounded-full h-full">
                <div class="text-text-muted-light dark:text-text-muted-dark flex border-r border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 items-center justify-center pl-4 rounded-l-full">
                  <span class="material-symbols-outlined">search</span>
                </div>
                <input
                  v-model="searchQuery"
                  class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-full text-slate-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border-none bg-white dark:bg-slate-800 h-full placeholder:text-slate-500 dark:placeholder:text-slate-400 px-4 pl-2 text-base font-normal leading-normal"
                  placeholder="Search by number or agent name..."
                />
              </div>
            </label>
          </div>

          <!-- Chips (Filters) -->
          <div class="flex gap-3 flex-wrap">
            <button
              @click="toggleStatusFilter"
              class="flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-full bg-white dark:bg-slate-800 pl-4 pr-3 border border-slate-300 dark:border-slate-700 hover:border-primary/50"
            >
              <p class="text-slate-900 dark:text-white text-sm font-medium leading-normal">Status</p>
              <span class="material-symbols-outlined text-slate-500 dark:text-slate-400">expand_more</span>
            </button>
            <button
              @click="toggleAgentFilter"
              class="flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-full bg-white dark:bg-slate-800 pl-4 pr-3 border border-slate-300 dark:border-slate-700 hover:border-primary/50"
            >
              <p class="text-slate-900 dark:text-white text-sm font-medium leading-normal">Assigned Agent</p>
              <span class="material-symbols-outlined text-slate-500 dark:text-slate-400">expand_more</span>
            </button>
            <button
              @click="toggleRegionFilter"
              class="flex h-9 shrink-0 items-center justify-center gap-x-2 rounded-full bg-white dark:bg-slate-800 pl-4 pr-3 border border-slate-300 dark:border-slate-700 hover:border-primary/50"
            >
              <p class="text-slate-900 dark:text-white text-sm font-medium leading-normal">Region</p>
              <span class="material-symbols-outlined text-slate-500 dark:text-slate-400">expand_more</span>
            </button>
          </div>
        </div>

        <!-- Data Table -->
        <div class="mt-8 overflow-x-auto bg-white dark:bg-slate-900 rounded border border-slate-200 dark:border-slate-800">
          <table class="w-full text-left">
            <thead class="border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th class="p-4 w-12">
                  <input
                    v-model="selectAll"
                    @change="handleSelectAll"
                    class="form-checkbox rounded border-gray-400 text-primary focus:ring-primary/50"
                    type="checkbox"
                  />
                </th>
                <th class="p-4 text-sm font-semibold text-slate-600 dark:text-slate-300">Phone Number</th>
                <th class="p-4 text-sm font-semibold text-slate-600 dark:text-slate-300">Status</th>
                <th class="p-4 text-sm font-semibold text-slate-600 dark:text-slate-300">Assigned Agent</th>
                <th class="p-4 text-sm font-semibold text-slate-600 dark:text-slate-300">Date Acquired</th>
                <th class="p-4 text-sm font-semibold text-slate-600 dark:text-slate-300 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
              <tr v-for="number in filteredNumbers" :key="number.id">
                <td class="p-4">
                  <input
                    v-model="number.selected"
                    class="form-checkbox rounded border-gray-400 text-primary focus:ring-primary/50"
                    type="checkbox"
                  />
                </td>
                <td class="p-4 text-sm font-medium text-slate-900 dark:text-white">{{ number.phone }}</td>
                <td class="p-4">
                  <span
                    class="inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm font-medium"
                    :class="getStatusClass(number.status)"
                  >
                    <span class="h-2 w-2 rounded-full" :class="getStatusDotClass(number.status)"></span>
                    {{ number.status }}
                  </span>
                </td>
                <td class="p-4 text-sm text-slate-900 dark:text-white">
                  {{ number.assignedAgent || '-' }}
                </td>
                <td class="p-4 text-sm text-slate-500 dark:text-slate-400">{{ number.dateAcquired }}</td>
                <td class="p-4 text-right">
                  <button
                    @click="handleActions(number)"
                    class="p-2 text-slate-500 dark:text-slate-400 hover:bg-primary/10 rounded-full"
                  >
                    <span class="material-symbols-outlined">more_horiz</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div class="flex items-center justify-between p-4 border-t border-slate-200 dark:border-slate-800">
            <span class="text-sm text-slate-500 dark:text-slate-400">
              Showing {{ startIndex }}-{{ endIndex }} of {{ totalNumbers }} results
            </span>
            <div class="flex items-center gap-2">
              <button
                @click="previousPage"
                :disabled="currentPage === 1"
                class="flex h-8 w-8 items-center justify-center rounded-full border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:bg-primary/10 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span class="material-symbols-outlined text-base">chevron_left</span>
              </button>
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                class="flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium"
                :class="page === currentPage
                  ? 'border border-primary bg-primary/10 text-primary'
                  : 'border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:bg-primary/10'"
              >
                {{ page }}
              </button>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="flex h-8 w-8 items-center justify-center rounded-full border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:bg-primary/10 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span class="material-symbols-outlined text-base">chevron_right</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State (shown when no results) -->
        <div
          v-if="filteredNumbers.length === 0"
          class="mt-8 flex flex-col items-center justify-center text-center p-12 bg-white dark:bg-slate-900 rounded-lg border-2 border-dashed border-slate-300 dark:border-slate-700"
        >
          <span class="material-symbols-outlined text-6xl text-slate-400 mb-4">phone_disabled</span>
          <h3 class="text-xl font-bold text-slate-900 dark:text-white">No Phone Numbers Yet</h3>
          <p class="mt-2 max-w-sm text-slate-500 dark:text-slate-400">
            Get started by acquiring your first number to assign to your voice agents.
          </p>
          <button
            @click="handleAcquireNumber"
            class="mt-6 flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-10 px-5 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 transition-colors"
          >
            <span class="material-symbols-outlined mr-2">add</span>
            <span class="truncate">Acquire First Number</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import SidebarNav from '@/components/SidebarNav.vue'

// State
const searchQuery = ref('')
const selectAll = ref(false)
const currentPage = ref(1)
const itemsPerPage = 4

// Phone numbers data
const phoneNumbers = ref([
  {
    id: 1,
    phone: '+1 (555) 123-4567',
    status: 'Assigned',
    assignedAgent: 'Eleanor Vance',
    dateAcquired: '2023-10-26',
    selected: false
  },
  {
    id: 2,
    phone: '+1 (555) 987-6543',
    status: 'Available',
    assignedAgent: null,
    dateAcquired: '2023-10-25',
    selected: false
  },
  {
    id: 3,
    phone: '+1 (555) 234-5678',
    status: 'Assigned',
    assignedAgent: 'Marcus Thorne',
    dateAcquired: '2023-10-22',
    selected: false
  },
  {
    id: 4,
    phone: '+1 (555) 876-5432',
    status: 'Released',
    assignedAgent: null,
    dateAcquired: '2023-10-20',
    selected: false
  },
  {
    id: 5,
    phone: '+1 (555) 345-6789',
    status: 'Assigned',
    assignedAgent: 'Sarah Connor',
    dateAcquired: '2023-10-18',
    selected: false
  },
  {
    id: 6,
    phone: '+1 (555) 456-7890',
    status: 'Available',
    assignedAgent: null,
    dateAcquired: '2023-10-15',
    selected: false
  },
  {
    id: 7,
    phone: '+1 (555) 567-8901',
    status: 'Assigned',
    assignedAgent: 'John Smith',
    dateAcquired: '2023-10-12',
    selected: false
  },
  {
    id: 8,
    phone: '+1 (555) 678-9012',
    status: 'Available',
    assignedAgent: null,
    dateAcquired: '2023-10-10',
    selected: false
  }
])

// Computed
const filteredNumbers = computed(() => {
  let filtered = phoneNumbers.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(number =>
      number.phone.toLowerCase().includes(query) ||
      (number.assignedAgent && number.assignedAgent.toLowerCase().includes(query))
    )
  }

  return filtered
})

const totalNumbers = computed(() => filteredNumbers.value.length)
const totalPages = computed(() => Math.ceil(totalNumbers.value / itemsPerPage))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage + 1)
const endIndex = computed(() => Math.min(currentPage.value * itemsPerPage, totalNumbers.value))

const visiblePages = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i++) {
    pages.push(i)
  }
  return pages.slice(0, 5) // Show first 5 pages
})

// Methods
const getStatusClass = (status) => {
  switch (status) {
    case 'Assigned':
      return 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400'
    case 'Available':
      return 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
    case 'Released':
      return 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'
    default:
      return 'bg-gray-100 dark:bg-gray-900/30 text-gray-600 dark:text-gray-400'
  }
}

const getStatusDotClass = (status) => {
  switch (status) {
    case 'Assigned':
      return 'bg-green-600 dark:bg-green-400'
    case 'Available':
      return 'bg-blue-600 dark:bg-blue-400'
    case 'Released':
      return 'bg-red-600 dark:bg-red-400'
    default:
      return 'bg-gray-600 dark:bg-gray-400'
  }
}

const handleSelectAll = () => {
  phoneNumbers.value.forEach(number => {
    number.selected = selectAll.value
  })
}

const handleAcquireNumber = () => {
  alert('Acquire New Number\n\nThis would open a modal or form to purchase a new phone number from your provider.')
}

const handleActions = (number) => {
  alert(`Actions for ${number.phone}\n\nOptions:\n- Edit\n- Release\n- Assign to Agent\n- View Details`)
}

const toggleStatusFilter = () => {
  alert('Status Filter\n\nThis would show a dropdown with options:\n- All\n- Assigned\n- Available\n- Released')
}

const toggleAgentFilter = () => {
  alert('Assigned Agent Filter\n\nThis would show a dropdown of all agents to filter by.')
}

const toggleRegionFilter = () => {
  alert('Region Filter\n\nThis would show a dropdown of regions:\n- US\n- Canada\n- UK\n- etc.')
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
  currentPage.value = page
}
</script>
