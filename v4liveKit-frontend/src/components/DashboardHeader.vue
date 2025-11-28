<template>
  <header class="sticky top-0 backdrop-blur-sm z-10 py-4 mb-6">
    <!-- Page Heading -->
    <div class="flex flex-wrap justify-between items-center gap-4">
      <h1 class="text-slate-900 dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">
        Agents
      </h1>
      <router-link
        to="/agents/create"
        class="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 transition-colors"
      >
        <span class="material-symbols-outlined" style="font-size: 20px;">add</span>
        <span class="truncate">Create Agent</span>
      </router-link>
    </div>

    <!-- Toolbar & Search -->
    <div class="flex flex-wrap items-center gap-4 mt-6">
      <div class="flex-1 min-w-[280px]">
        <label class="flex flex-col w-full">
          <div class="flex w-full flex-1 items-stretch rounded-lg h-11">
            <div
              class="text-slate-500 dark:text-slate-400 flex bg-white/80 backdrop-blur-md dark:bg-slate-800/50 items-center justify-center pl-4 rounded-l-lg border border-r-0 border-slate-300 dark:border-slate-700"
            >
              <span class="material-symbols-outlined" style="font-size: 24px;">search</span>
            </div>
            <input
              v-model="searchQuery"
              class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 bg-white/80 backdrop-blur-md dark:bg-slate-800/50 h-full placeholder:text-slate-500 dark:placeholder:text-slate-400 px-4 rounded-l-none border border-l-0 border-slate-300 dark:border-slate-700 text-base font-normal leading-normal"
              placeholder="Search by name or number..."
            />
          </div>
        </label>
      </div>
      <div class="flex gap-3">
        <button
          class="flex h-11 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-white/80 backdrop-blur-md dark:bg-slate-800/50 border border-slate-300 dark:border-slate-700 px-4 hover:bg-slate-50 dark:hover:bg-slate-800"
        >
          <span class="material-symbols-outlined text-slate-700 dark:text-slate-300" style="font-size: 20px;">
            filter_list
          </span>
          <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Status</p>
          <span class="material-symbols-outlined text-slate-500 dark:text-slate-400" style="font-size: 20px;">
            expand_more
          </span>
        </button>
        <button
          class="flex h-11 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-white/80 backdrop-blur-md dark:bg-slate-800/50 border border-slate-300 dark:border-slate-700 px-4 hover:bg-slate-50 dark:hover:bg-slate-800"
        >
          <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Owner</p>
          <span class="material-symbols-outlined text-slate-500 dark:text-slate-400" style="font-size: 20px;">
            expand_more
          </span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const searchQuery = ref('')
</script>
