<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <DashboardHeader />

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-20">
          <div class="inline-flex items-center justify-center bg-primary/10 text-primary w-20 h-20 rounded-full mb-6 animate-pulse">
            <span class="material-symbols-outlined" style="font-size: 48px;">sync</span>
          </div>
          <h2 class="text-2xl font-bold text-slate-800 dark:text-white">Loading agents...</h2>
          <p class="text-slate-600 dark:text-slate-400 mt-2">Please wait while we fetch your agents from backend.</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50/80 backdrop-blur-md dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 mb-6">
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-red-600 dark:text-red-400">error</span>
            <div>
              <h3 class="font-semibold text-red-900 dark:text-red-100">Error loading agents</h3>
              <p class="text-sm text-red-700 dark:text-red-300 mt-1">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Agents Grid -->
        <div v-else-if="agents.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <AgentCard
            v-for="agent in agents"
            :key="agent.id"
            :agent="agent"
          />
        </div>

        <!-- Empty State (agar agent najd nabashe) -->
        <div v-else class="text-center py-20">
          <div
            class="inline-flex items-center justify-center bg-primary/10 text-primary w-20 h-20 rounded-full mb-6"
          >
            <span class="material-symbols-outlined" style="font-size: 48px;">smart_toy</span>
          </div>
          <h2 class="text-2xl font-bold text-slate-800 dark:text-white">No agents found</h2>
          <p class="text-slate-600 dark:text-slate-400 mt-2 mb-6">
            Get started by creating your first voice agent.
          </p>
          <button
            class="flex mx-auto min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 transition-colors"
          >
            <span class="material-symbols-outlined" style="font-size: 20px;">add</span>
            <span class="truncate">Create Agent</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SidebarNav from '@/components/SidebarNav.vue'
import DashboardHeader from '@/components/DashboardHeader.vue'
import AgentCard from '@/components/AgentCard.vue'
import { getAgents } from '@/services/api'

// State
const agents = ref([])
const loading = ref(true)
const error = ref(null)

// Fetch agents az backend
const fetchAgents = async () => {
  loading.value = true
  error.value = null

  try {
    const data = await getAgents()
    console.log('✅ Agents fetched from backend:', data)

    // Map backend data be format e AgentCard
    agents.value = data.map(agent => ({
      id: agent.id,
      name: agent.name,
      phone: agent.phone || 'Not configured',
      status: agent.status,
      owner: agent.owner || 'System',
      totalCalls: agent.total_calls || 0,
      avgDuration: agent.avg_duration || '0m 0s',
      modified: agent.modified || 'Recently',
      description: agent.description,
      language: agent.language,
      capabilities: agent.capabilities
    }))
  } catch (err) {
    console.error('❌ Failed to fetch agents:', err)
    error.value = 'Failed to load agents. Please check if backend is running.'

    // Fallback be mock data age backend available nabood
    agents.value = [
      {
        id: 'product-search-agent',
        name: 'Product Search Agent',
        phone: 'Not configured',
        status: 'active',
        owner: 'System',
        totalCalls: 0,
        avgDuration: '0m 0s',
        modified: 'Just now',
        description: 'Swedish voice agent for product search',
        language: 'sv',
        capabilities: ['Product search', 'Price inquiries', 'Stock status']
      }
    ]
  } finally {
    loading.value = false
  }
}

// Fetch agents vaghti component mount mishe
onMounted(() => {
  fetchAgents()
})
</script>
