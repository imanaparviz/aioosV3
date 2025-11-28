<template>
  <aside class="w-64 shrink-0 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col p-4">
    <!-- Logo Area -->
    <div class="flex items-center gap-3 mb-6 pb-4 border-b border-slate-200 dark:border-slate-700">
      <router-link to="/" class="flex items-center gap-3 group">
        <img src="/logo-medium.png" alt="AIOOS" class="w-10 h-10 object-contain group-hover:scale-105 transition-transform" />
        <span class="text-xl font-bold text-slate-900 dark:text-white">AIOOS</span>
      </router-link>
    </div>

    <!-- User Profile -->
    <div class="flex items-center gap-3 mb-8">
      <div
        class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
        data-alt="Admin user avatar"
        style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBugWy-Lmcf4cgArwgE75ayWcOkZBJUfY40RQmp9we9CuHiBA2qYNy7_MnYLy4TVEkuZxZjQv4OvtodeuskG_INBvbIhUbkWr3AGK-GPKfVC90aesdoxYWyfV3spm7txTV6kJkEVAD3uXwDTGKfjzp-vcQ5ylqxIFtXefQ9idlDqctCwwvxBaSEp5e0oGahnrYsFCw4aQQTtc3V7kcuULA6sknEm-_YeRFqbKHNkUo-sDHSLk6eLsmUA2X3NlSdVxF1jl5S3sx11fU2");'
      ></div>
      <div class="flex flex-col">
        <h1 class="text-slate-900 dark:text-white text-base font-medium leading-normal">
          Admin User
        </h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm font-normal leading-normal">
          admin@voicecorp.com
        </p>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex flex-col gap-2 flex-grow">
      <router-link
        to="/dashboard"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">dashboard</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Dashboard</p>
      </router-link>
      <router-link
        to="/agents/create"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">support_agent</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Agents</p>
      </router-link>
      <router-link
        to="/agents/test/widget"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">mic</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Test Agent</p>
      </router-link>
      <router-link
        to="/analytics"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">analytics</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Analytics</p>
      </router-link>
      <router-link
        to="/call-logs"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">phone_in_talk</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Call Logs</p>
      </router-link>
      <router-link
        to="/calendar"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">calendar_month</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Calendar</p>
      </router-link>
      <router-link
        to="/knowledge"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">library_books</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Knowledge Base</p>
      </router-link>
      <router-link
        to="/phone-numbers"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">phone</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Phone Numbers</p>
      </router-link>
      <router-link
        to="/users"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">group</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">User Management</p>
      </router-link>
      <router-link
        to="/teams"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">groups</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Team Management</p>
      </router-link>
      <router-link
        to="/billing"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">receipt_long</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Billing</p>
      </router-link>
      <router-link
        to="/webhooks"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">code</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">API & Webhooks</p>
      </router-link>
      <router-link
        to="/audit-log"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">policy</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Audit Log</p>
      </router-link>
      <router-link
        to="/product-search"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">search</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Product Search</p>
      </router-link>
      <router-link
        to="/settings"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">settings</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Settings</p>
      </router-link>
    </nav>

    <!-- Bottom Links -->
    <div class="flex flex-col gap-1">
      <router-link
        to="/help"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
        active-class="bg-primary/20 dark:bg-primary/30"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">help</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Help</p>
      </router-link>
      <button
        @click="handleLogout"
        class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-left w-full"
      >
        <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">logout</span>
        <p class="text-slate-800 dark:text-slate-200 text-sm font-medium leading-normal">Logout</p>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
