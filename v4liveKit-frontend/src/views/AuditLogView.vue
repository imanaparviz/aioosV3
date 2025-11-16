<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-6 lg:p-10 overflow-y-auto bg-slate-50 dark:bg-background-dark">
      <div class="flex flex-col h-full">
        <!-- Header -->
        <header class="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div class="flex flex-col gap-1">
            <h1 class="text-slate-900 dark:text-white text-3xl lg:text-4xl font-black leading-tight tracking-[-0.033em]">
              Audit Log
            </h1>
            <p class="text-slate-600 dark:text-slate-400 text-base">
              Track all significant actions taken within the platform.
            </p>
          </div>
          <button
            @click="handleExportLog"
            class="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90"
          >
            <span class="material-symbols-outlined !text-[18px]">download</span>
            <span>Export Log</span>
          </button>
        </header>

        <!-- Search and Filters -->
        <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div class="relative w-full max-w-sm">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500">
              search
            </span>
            <input
              v-model="searchQuery"
              class="w-full h-10 pl-10 pr-4 border border-slate-200 dark:border-slate-800 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-primary"
              placeholder="Search by user, action, resource..."
              type="text"
            />
          </div>
          <div class="flex items-center gap-4">
            <button
              @click="showFilters = !showFilters"
              class="px-4 py-2 text-sm font-medium rounded-lg text-slate-600 dark:text-slate-400 hover:bg-primary/10 hover:text-primary flex items-center gap-2"
            >
              <span class="material-symbols-outlined text-base">filter_list</span>
              <span>Filters</span>
            </button>
            <button
              @click="showDateRange = !showDateRange"
              class="px-4 py-2 text-sm font-medium rounded-lg text-slate-600 dark:text-slate-400 hover:bg-primary/10 hover:text-primary flex items-center gap-2"
            >
              <span class="material-symbols-outlined text-base">date_range</span>
              <span>Date Range</span>
            </button>
          </div>
        </div>

        <!-- Audit Log Table -->
        <div class="flex-1 flex flex-col">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden flex-1 flex flex-col">
            <div class="overflow-x-auto flex-1">
              <table class="w-full text-left">
                <thead>
                  <tr class="bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800">
                    <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400">
                      <div class="flex items-center gap-1 cursor-pointer hover:text-primary" @click="toggleSort">
                        Timestamp
                        <span class="material-symbols-outlined text-base">arrow_downward</span>
                      </div>
                    </th>
                    <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400">User</th>
                    <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400">Action Type</th>
                    <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400">Resource Affected</th>
                    <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400">Details</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="log in paginatedLogs"
                    :key="log.id"
                    class="border-b border-slate-200 dark:border-slate-800 last:border-b-0 hover:bg-slate-50 dark:hover:bg-slate-800/30"
                  >
                    <!-- Timestamp -->
                    <td class="p-4 align-top text-sm text-slate-900 dark:text-white whitespace-nowrap">
                      {{ log.timestamp }}
                    </td>

                    <!-- User -->
                    <td class="p-4 align-top">
                      <div class="flex items-center gap-3">
                        <div
                          class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-8"
                          :style="`background-image: url('${log.user.avatar}');`"
                          :alt="log.user.name"
                        ></div>
                        <div>
                          <p class="font-medium text-slate-900 dark:text-white">{{ log.user.name }}</p>
                          <p class="text-sm text-slate-600 dark:text-slate-400">{{ log.user.email }}</p>
                        </div>
                      </div>
                    </td>

                    <!-- Action Type -->
                    <td class="p-4 align-top">
                      <span
                        class="inline-flex items-center px-2 py-1 text-xs font-medium rounded-md"
                        :class="getActionBadgeClass(log.actionType)"
                      >
                        {{ log.actionType }}
                      </span>
                    </td>

                    <!-- Resource -->
                    <td class="p-4 align-top text-sm text-slate-600 dark:text-slate-400">
                      {{ log.resource }}
                    </td>

                    <!-- Details -->
                    <td class="p-4 align-top text-sm text-slate-600 dark:text-slate-400">
                      {{ log.details }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination Footer -->
            <div class="p-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <p class="text-sm text-slate-600 dark:text-slate-400">
                Showing {{ (currentPage - 1) * logsPerPage + 1 }} to {{ Math.min(currentPage * logsPerPage, filteredLogs.length) }} of {{ filteredLogs.length }} entries
              </p>
              <div class="flex items-center gap-2">
                <button
                  @click="goToPage(currentPage - 1)"
                  :disabled="currentPage === 1"
                  class="flex items-center justify-center size-8 rounded-lg hover:bg-primary/10 text-slate-500 dark:text-slate-400 hover:text-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span class="material-symbols-outlined text-xl">chevron_left</span>
                </button>

                <!-- Page Numbers -->
                <button
                  v-for="page in displayedPages"
                  :key="page"
                  @click="goToPage(page)"
                  class="flex items-center justify-center size-8 rounded-lg text-sm font-medium"
                  :class="page === currentPage
                    ? 'bg-primary/10 text-primary'
                    : 'hover:bg-primary/10 text-slate-500 dark:text-slate-400 hover:text-primary'"
                >
                  {{ page }}
                </button>

                <span v-if="totalPages > 5" class="text-slate-500 dark:text-slate-400">...</span>

                <button
                  v-if="totalPages > 5"
                  @click="goToPage(totalPages)"
                  class="flex items-center justify-center size-8 rounded-lg hover:bg-primary/10 text-slate-500 dark:text-slate-400 hover:text-primary text-sm font-medium"
                >
                  {{ totalPages }}
                </button>

                <button
                  @click="goToPage(currentPage + 1)"
                  :disabled="currentPage === totalPages"
                  class="flex items-center justify-center size-8 rounded-lg hover:bg-primary/10 text-slate-500 dark:text-slate-400 hover:text-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span class="material-symbols-outlined text-xl">chevron_right</span>
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
import SidebarNav from '@/components/SidebarNav.vue'

const searchQuery = ref('')
const showFilters = ref(false)
const showDateRange = ref(false)
const currentPage = ref(1)
const logsPerPage = 5

// Mock audit log data
const auditLogs = ref([
  {
    id: 1,
    timestamp: '2023-10-27 14:30:15 UTC',
    user: {
      name: 'Admin User',
      email: 'admin@voicecorp.com',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBugWy-Lmcf4cgArwgE75ayWcOkZBJUfY40RQmp9we9CuHiBA2qYNy7_MnYLy4TVEkuZxZjQv4OvtodeuskG_INBvbIhUbkWr3AGK-GPKfVC90aesdoxYWyfV3spm7txTV6kJkEVAD3uXwDTGKfjzp-vcQ5ylqxIFtXefQ9idlDqctCwwvxBaSEp5e0oGahnrYsFCw4aQQTtc3V7kcuULA6sknEm-_YeRFqbKHNkUo-sDHSLk6eLsmUA2X3NlSdVxF1jl5S3sx11fU2'
    },
    actionType: 'Agent Created',
    resource: 'Agent ID: AG-98765',
    details: 'Agent "Clara" created. IP: 192.168.1.1'
  },
  {
    id: 2,
    timestamp: '2023-10-27 13:45:22 UTC',
    user: {
      name: 'Alice Johnson',
      email: 'alice.j@voicecorp.com',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDZvZqTs0XbbQPhfuXsEtpg0RgbdK7vda6UaSIidcC52g7Icjqf_J7WcxBNgFgJ2QWLUkQmHR3apkqUNZVy9mFJO45cVtOTXXpfaFHUEsLa80vPk9wn2ySogsR0RC7RWCBNvGSVz-41Niqmc9kRlEOrXrIzQ3mTDc9sxG_Ppmk4Azqrsvx6s8rnG1LxPFpPkuVzUaRSLhfzx-BZkM2nxJyJMZBO1aYXgp9Dj4KQdBOv4JC_hxXQreTfQuT8i-c8N0_hA41n7NTqC6oU'
    },
    actionType: 'Settings Updated',
    resource: 'User ID: USR-12345',
    details: "Permissions changed from 'Editor' to 'Admin'."
  },
  {
    id: 3,
    timestamp: '2023-10-27 11:05:00 UTC',
    user: {
      name: 'Bob Williams',
      email: 'bob.w@voicecorp.com',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAbwhnkamiubIn5UYkQyj8m-cZ88KrwFmjW62ZGrKTIxFkBNC4gMf7ctx7l0P4FwHtXsmF08xuuV71PekShK6nx5U0RRv6mFIk8Dx1aovhmxCftK5Lw8spHo-HYtyAeKI6mfT4nS6qyk1STX7B4RKeMAV2Wp519iyr8A9s80Hne8OavbmUhBfq5YxzhDLRqvOF0GMsjHOQNpZclhZObJEDcE_maqcX2KsVKbU7DVw40j7KfvYwSwnJMYujG46E4gw6oMa2ig0byt3CO'
    },
    actionType: 'User Login',
    resource: 'User ID: USR-67890',
    details: 'Successful login from IP: 203.0.113.25'
  },
  {
    id: 4,
    timestamp: '2023-10-26 18:20:45 UTC',
    user: {
      name: 'System',
      email: 'automated@process',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBezwgNmOs5HFKLMN1GLXLf8HNIAEbepSSTqvESemyoztZ3OIM9ISbKSUEMdse-tKsCzPlGQyPK5rTpNFiiaxXPydf8Qdk20Sxo8iAJ3QZCs_NXTpG4MbsCL71Eb0eGYPv2fJcf7oa9_c89grLKY3jbc9FpLv9zuIctVFZoOLwQG3F-m4bDBAoviMIGiE_z5Dv7ltZI3AtOzdsKf2n3CTKOUB5bCXX8LgSxxxEhdevvN25YLMo3gF8sKu4CkBdHQz4tHEmWdKSpyGur'
    },
    actionType: 'Report Generated',
    resource: 'Report ID: REP-ABCDE',
    details: 'Monthly usage report for October 2023.'
  },
  {
    id: 5,
    timestamp: '2023-10-26 09:15:10 UTC',
    user: {
      name: 'Admin User',
      email: 'admin@voicecorp.com',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBugWy-Lmcf4cgArwgE75ayWcOkZBJUfY40RQmp9we9CuHiBA2qYNy7_MnYLy4TVEkuZxZjQv4OvtodeuskG_INBvbIhUbkWr3AGK-GPKfVC90aesdoxYWyfV3spm7txTV6kJkEVAD3uXwDTGKfjzp-vcQ5ylqxIFtXefQ9idlDqctCwwvxBaSEp5e0oGahnrYsFCw4aQQTtc3V7kcuULA6sknEm-_YeRFqbKHNkUo-sDHSLk6eLsmUA2X3NlSdVxF1jl5S3sx11fU2'
    },
    actionType: 'User Deleted',
    resource: 'User ID: USR-54321',
    details: "User 'charlie.d@voicecorp.com' was deleted."
  },
  {
    id: 6,
    timestamp: '2023-10-25 16:30:00 UTC',
    user: {
      name: 'Alice Johnson',
      email: 'alice.j@voicecorp.com',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDZvZqTs0XbbQPhfuXsEtpg0RgbdK7vda6UaSIidcC52g7Icjqf_J7WcxBNgFgJ2QWLUkQmHR3apkqUNZVy9mFJO45cVtOTXXpfaFHUEsLa80vPk9wn2ySogsR0RC7RWCBNvGSVz-41Niqmc9kRlEOrXrIzQ3mTDc9sxG_Ppmk4Azqrsvx6s8rnG1LxPFpPkuVzUaRSLhfzx-BZkM2nxJyJMZBO1aYXgp9Dj4KQdBOv4JC_hxXQreTfQuT8i-c8N0_hA41n7NTqC6oU'
    },
    actionType: 'Agent Updated',
    resource: 'Agent ID: AG-11223',
    details: 'Agent "David" configuration updated.'
  },
  {
    id: 7,
    timestamp: '2023-10-25 14:20:33 UTC',
    user: {
      name: 'Bob Williams',
      email: 'bob.w@voicecorp.com',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAbwhnkamiubIn5UYkQyj8m-cZ88KrwFmjW62ZGrKTIxFkBNC4gMf7ctx7l0P4FwHtXsmF08xuuV71PekShK6nx5U0RRv6mFIk8Dx1aovhmxCftK5Lw8spHo-HYtyAeKI6mfT4nS6qyk1STX7B4RKeMAV2Wp519iyr8A9s80Hne8OavbmUhBfq5YxzhDLRqvOF0GMsjHOQNpZclhZObJEDcE_maqcX2KsVKbU7DVw40j7KfvYwSwnJMYujG46E4gw6oMa2ig0byt3CO'
    },
    actionType: 'API Key Created',
    resource: 'Key ID: KEY-99887',
    details: 'New production API key generated.'
  },
  {
    id: 8,
    timestamp: '2023-10-25 10:15:22 UTC',
    user: {
      name: 'Admin User',
      email: 'admin@voicecorp.com',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBugWy-Lmcf4cgArwgE75ayWcOkZBJUfY40RQmp9we9CuHiBA2qYNy7_MnYLy4TVEkuZxZjQv4OvtodeuskG_INBvbIhUbkWr3AGK-GPKfVC90aesdoxYWyfV3spm7txTV6kJkEVAD3uXwDTGKfjzp-vcQ5ylqxIFtXefQ9idlDqctCwwvxBaSEp5e0oGahnrYsFCw4aQQTtc3V7kcuULA6sknEm-_YeRFqbKHNkUo-sDHSLk6eLsmUA2X3NlSdVxF1jl5S3sx11fU2'
    },
    actionType: 'Team Created',
    resource: 'Team ID: TM-44556',
    details: 'Team "Sales Team Alpha" created.'
  }
])

// Filtered logs based on search
const filteredLogs = computed(() => {
  if (!searchQuery.value) return auditLogs.value

  const query = searchQuery.value.toLowerCase()
  return auditLogs.value.filter(log =>
    log.user.name.toLowerCase().includes(query) ||
    log.user.email.toLowerCase().includes(query) ||
    log.actionType.toLowerCase().includes(query) ||
    log.resource.toLowerCase().includes(query) ||
    log.details.toLowerCase().includes(query)
  )
})

// Pagination
const totalPages = computed(() => Math.ceil(filteredLogs.value.length / logsPerPage))

const paginatedLogs = computed(() => {
  const start = (currentPage.value - 1) * logsPerPage
  const end = start + logsPerPage
  return filteredLogs.value.slice(start, end)
})

const displayedPages = computed(() => {
  const pages = []
  const maxPagesToShow = 3

  for (let i = 1; i <= Math.min(maxPagesToShow, totalPages.value); i++) {
    pages.push(i)
  }

  return pages
})

// Methods
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const toggleSort = () => {
  auditLogs.value.reverse()
}

const getActionBadgeClass = (actionType) => {
  const types = {
    'Agent Created': 'bg-primary/10 text-primary',
    'Agent Updated': 'bg-primary/10 text-primary',
    'Settings Updated': 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400',
    'User Login': 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
    'Report Generated': 'bg-indigo-100 text-indigo-600 dark:bg-indigo-900/30 dark:text-indigo-400',
    'User Deleted': 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
    'API Key Created': 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
    'Team Created': 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400'
  }

  return types[actionType] || 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
}

const handleExportLog = () => {
  alert('Export Log\n\nThis would download the audit log as a CSV or JSON file.')
}
</script>
