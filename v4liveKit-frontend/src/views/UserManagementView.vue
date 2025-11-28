<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="mx-auto max-w-7xl p-6 lg:p-8">
        <!-- Page Heading -->
        <header class="sticky top-0 backdrop-blur-sm z-10 py-4 mb-6 flex flex-wrap items-center justify-between gap-4">
          <h1 class="text-4xl font-black leading-tight tracking-[-0.033em] text-slate-900 dark:text-white">
            User Management
          </h1>
          <!-- Mobile Toolbar -->
          <div class="flex gap-2 lg:hidden">
            <button class="p-2 text-slate-600 dark:text-slate-300 rounded-full hover:bg-slate-200 dark:hover:bg-slate-700">
              <span class="material-symbols-outlined">search</span>
            </button>
            <button class="p-2 text-slate-600 dark:text-slate-300 rounded-full hover:bg-slate-200 dark:hover:bg-slate-700">
              <span class="material-symbols-outlined">filter_list</span>
            </button>
            <button
              @click="handleAddUser"
              class="flex cursor-pointer items-center justify-center rounded-full bg-primary text-white size-10"
            >
              <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">add</span>
            </button>
          </div>
        </header>

        <!-- Action Bar (Search, Filters, Add Button) -->
        <div class="mt-6 flex flex-col gap-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 lg:flex-row lg:items-center">
          <!-- Search Bar -->
          <div class="flex-1">
            <label class="flex h-12 w-full flex-col">
              <div class="flex h-full w-full flex-1 items-stretch rounded-lg">
                <div class="flex items-center justify-center rounded-l-lg border-y border-l border-slate-200 bg-slate-50/80 backdrop-blur-md dark:border-slate-700 dark:bg-slate-800/80 pl-4 text-slate-500 dark:text-slate-400">
                  <span class="material-symbols-outlined">search</span>
                </div>
                <input
                  v-model="searchQuery"
                  @input="handleSearch"
                  class="form-input h-full w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg border border-slate-200 bg-white/80 backdrop-blur-md text-slate-900 placeholder:text-slate-500 focus:border-primary focus:outline-0 focus:ring-0 dark:border-slate-700 dark:bg-slate-900/80 dark:text-white dark:placeholder:text-slate-400 pl-2 text-base font-normal leading-normal"
                  placeholder="Search by name or email..."
                />
              </div>
            </label>
          </div>

          <!-- Filter Chips -->
          <div class="flex flex-wrap items-center gap-3">
            <button
              @click="toggleRoleFilter"
              class="flex h-10 shrink-0 items-center justify-center gap-x-2 rounded-full bg-slate-100/80 backdrop-blur-md dark:bg-slate-800/80 pl-4 pr-3 text-slate-700 dark:text-slate-200"
            >
              <p class="text-sm font-medium leading-normal">Role</p>
              <span class="material-symbols-outlined">arrow_drop_down</span>
            </button>
            <button
              @click="toggleStatusFilter"
              class="flex h-10 shrink-0 items-center justify-center gap-x-2 rounded-full bg-slate-100/80 backdrop-blur-md dark:bg-slate-800/80 pl-4 pr-3 text-slate-700 dark:text-slate-200"
            >
              <p class="text-sm font-medium leading-normal">Status</p>
              <span class="material-symbols-outlined">arrow_drop_down</span>
            </button>
          </div>

          <!-- Add User Button (Desktop) -->
          <div class="hidden lg:block">
            <button
              @click="handleAddUser"
              class="flex h-10 cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-full bg-primary px-4 text-sm font-bold leading-normal tracking-[0.015em] text-white"
            >
              <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">add</span>
              <span class="truncate">Add User</span>
            </button>
          </div>
        </div>

        <!-- Data Table -->
        <div class="mt-6 overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 backdrop-blur-md dark:bg-slate-900/80">
          <div class="overflow-x-auto">
            <table class="w-full min-w-[800px] text-left text-sm">
              <thead class="border-b border-slate-200 dark:border-slate-800 bg-slate-50/80 backdrop-blur-md dark:bg-slate-800/50 text-slate-600 dark:text-slate-300">
                <tr>
                  <th class="p-4">
                    <input
                      v-model="selectAll"
                      @change="handleSelectAll"
                      class="form-checkbox rounded border-slate-300 dark:border-slate-600 bg-transparent text-primary focus:ring-primary/50"
                      type="checkbox"
                    />
                  </th>
                  <th class="p-4 font-medium">Name</th>
                  <th class="p-4 font-medium">Email</th>
                  <th class="p-4 font-medium">Role</th>
                  <th class="p-4 font-medium">Status</th>
                  <th class="p-4 font-medium">Last Login</th>
                  <th class="p-4 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
                <tr v-for="user in paginatedUsers" :key="user.id">
                  <td class="p-4">
                    <input
                      v-model="selectedUsers"
                      :value="user.id"
                      class="form-checkbox rounded border-slate-300 dark:border-slate-600 bg-transparent text-primary focus:ring-primary/50"
                      type="checkbox"
                    />
                  </td>
                  <td class="p-4 text-slate-900 dark:text-white font-medium">{{ user.name }}</td>
                  <td class="p-4 text-slate-600 dark:text-slate-300">{{ user.email }}</td>
                  <td class="p-4">
                    <span
                      class="inline-flex items-center rounded-full px-2 py-1 text-xs font-semibold"
                      :class="getRoleBadgeClass(user.role)"
                    >
                      {{ user.role }}
                    </span>
                  </td>
                  <td class="p-4">
                    <span
                      class="inline-flex items-center rounded-full px-2 py-1 text-xs font-semibold"
                      :class="getStatusBadgeClass(user.status)"
                    >
                      {{ user.status }}
                    </span>
                  </td>
                  <td class="p-4 text-slate-600 dark:text-slate-300">{{ user.lastLogin }}</td>
                  <td class="p-4">
                    <button
                      @click="handleUserActions(user)"
                      class="p-1.5 text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
                    >
                      <span class="material-symbols-outlined">more_vert</span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="flex flex-col items-center justify-between gap-4 border-t border-slate-200 dark:border-slate-800 p-4 sm:flex-row">
            <p class="text-sm text-slate-600 dark:text-slate-300">
              Showing <span class="font-semibold">{{ startIndex + 1 }}</span> to
              <span class="font-semibold">{{ Math.min(endIndex, totalUsers) }}</span> of
              <span class="font-semibold">{{ totalUsers }}</span> results
            </p>
            <div class="flex items-center gap-2">
              <button
                @click="previousPage"
                :disabled="currentPage === 1"
                class="flex h-9 w-9 items-center justify-center rounded-full text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span class="material-symbols-outlined">chevron_left</span>
              </button>
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                :class="page === currentPage
                  ? 'flex h-9 w-9 items-center justify-center rounded-full bg-primary text-sm font-semibold text-white'
                  : 'flex h-9 w-9 items-center justify-center rounded-full text-sm font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'"
              >
                {{ page }}
              </button>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="flex h-9 w-9 items-center justify-center rounded-full text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span class="material-symbols-outlined">chevron_right</span>
              </button>
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

// State
const searchQuery = ref('')
const selectAll = ref(false)
const selectedUsers = ref([])

// Mock Users Data
const users = ref([
  {
    id: 1,
    name: 'Alex Johnson',
    email: 'alex.johnson@example.com',
    role: 'Admin',
    status: 'Active',
    lastLogin: '2024-05-20 10:30 AM'
  },
  {
    id: 2,
    name: 'Maria Garcia',
    email: 'maria.garcia@example.com',
    role: 'User',
    status: 'Active',
    lastLogin: '2024-05-19 02:15 PM'
  },
  {
    id: 3,
    name: 'Chen Wei',
    email: 'chen.wei@example.com',
    role: 'Subuser',
    status: 'Inactive',
    lastLogin: '2024-04-10 09:00 AM'
  },
  {
    id: 4,
    name: 'David Miller',
    email: 'david.miller@example.com',
    role: 'User',
    status: 'Active',
    lastLogin: '2024-05-21 11:45 AM'
  }
])

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

const totalUsers = computed(() => users.value.length)
const totalPages = computed(() => Math.ceil(totalUsers.value / itemsPerPage.value))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value)
const endIndex = computed(() => currentPage.value * itemsPerPage.value)

const paginatedUsers = computed(() => {
  return users.value.slice(startIndex.value, endIndex.value)
})

const visiblePages = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i++) {
    pages.push(i)
  }
  return pages
})

// Methods
const getRoleBadgeClass = (role) => {
  const classes = {
    'Admin': 'bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300',
    'User': 'bg-purple-100 dark:bg-purple-900/50 text-purple-800 dark:text-purple-300',
    'Subuser': 'bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200'
  }
  return classes[role] || ''
}

const getStatusBadgeClass = (status) => {
  const classes = {
    'Active': 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300',
    'Inactive': 'bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200'
  }
  return classes[status] || ''
}

const handleSearch = () => {
  console.log('Searching for:', searchQuery.value)
  // In real implementation, filter users
}

const toggleRoleFilter = () => {
  alert('Role Filter\n\nFilter options:\n- All Roles\n- Admin\n- User\n- Subuser\n\nThis would show a dropdown menu.')
}

const toggleStatusFilter = () => {
  alert('Status Filter\n\nFilter options:\n- All Statuses\n- Active\n- Inactive\n\nThis would show a dropdown menu.')
}

const handleAddUser = () => {
  alert('Add New User\n\nThis would open a modal or form to:\n- Enter name\n- Enter email\n- Assign role\n- Set initial status\n\nIn the full implementation, this would create a new user.')
}

const handleSelectAll = () => {
  if (selectAll.value) {
    selectedUsers.value = users.value.map(u => u.id)
  } else {
    selectedUsers.value = []
  }
}

const handleUserActions = (user) => {
  console.log('User actions for:', user)
  alert(`User Actions: ${user.name}\n\nAvailable actions:\n- Edit User\n- Change Role\n- Deactivate/Activate\n- Reset Password\n- Delete User\n\nThis would show a dropdown menu.`)
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
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
</script>
