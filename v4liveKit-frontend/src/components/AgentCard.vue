<template>
  <router-link
    :to="`/agents/${agent.id}?name=${encodeURIComponent(agent.name)}`"
    class="block bg-white/80 dark:bg-slate-900/50 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all flex flex-col cursor-pointer"
  >
    <!-- Header -->
    <div class="p-5">
      <div class="flex justify-between items-start">
        <div class="flex items-center gap-2">
          <span
            class="w-3 h-3 rounded-full"
            :class="{
              'bg-green-500': agent.status === 'active',
              'bg-slate-400': agent.status === 'inactive',
              'bg-orange-400': agent.status === 'warning',
              'bg-red-500': agent.status === 'deactivated'
            }"
          ></span>
          <span
            class="text-sm font-medium"
            :class="{
              'text-green-600 dark:text-green-400': agent.status === 'active',
              'text-slate-600 dark:text-slate-400': agent.status === 'inactive',
              'text-orange-600 dark:text-orange-400': agent.status === 'warning',
              'text-red-600 dark:text-red-400': agent.status === 'deactivated'
            }"
          >
            {{ getStatusLabel(agent.status) }}
          </span>
        </div>
        <span v-if="agent.owner" class="text-xs text-slate-500 dark:text-slate-400">
          Owned by: {{ agent.owner }}
        </span>
      </div>
      <h3 class="text-lg font-bold text-slate-900 dark:text-white mt-3">
        {{ agent.name }}
      </h3>
      <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">
        {{ agent.phone }}
      </p>
    </div>

    <!-- Stats -->
    <div class="px-5 py-4 bg-slate-50/50 dark:bg-slate-800/50">
      <div class="flex justify-around text-center">
        <div>
          <p class="text-xs text-slate-500 dark:text-slate-400">Total Calls</p>
          <p class="text-lg font-bold text-slate-800 dark:text-slate-200">
            {{ formatNumber(agent.totalCalls) }}
          </p>
        </div>
        <div>
          <p class="text-xs text-slate-500 dark:text-slate-400">Avg. Duration</p>
          <p class="text-lg font-bold text-slate-800 dark:text-slate-200">
            {{ agent.avgDuration }}
          </p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="p-5 mt-auto flex justify-between items-center">
      <span class="text-xs text-slate-500 dark:text-slate-400">
        Modified {{ agent.modified }}
      </span>
      <div class="flex items-center gap-2">
        <button
          class="h-8 px-3 text-sm font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700"
        >
          Edit
        </button>
        <button
          class="h-8 w-8 flex items-center justify-center rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700"
        >
          <span class="material-symbols-outlined text-slate-600 dark:text-slate-300" style="font-size: 20px;">
            more_horiz
          </span>
        </button>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  agent: {
    type: Object,
    required: true
  }
})

const getStatusLabel = (status) => {
  const labels = {
    active: 'Active',
    inactive: 'Inactive',
    warning: 'Needs Attention',
    deactivated: 'Deactivated'
  }
  return labels[status] || status
}

const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}
</script>
