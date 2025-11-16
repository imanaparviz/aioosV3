<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark">
      <div class="px-4 py-5 sm:px-6 md:px-10 lg:px-20 xl:px-40 flex flex-1 justify-center">
        <div class="flex flex-col w-full max-w-5xl flex-1">
          <!-- Back Button -->
          <div class="flex flex-wrap gap-2 p-4">
            <router-link
              to="/dashboard"
              class="flex items-center gap-2 text-primary text-base font-medium leading-normal hover:underline"
            >
              <span class="material-symbols-outlined text-lg">arrow_back</span>
              <span>Back to Agents List</span>
            </router-link>
          </div>

          <!-- Header -->
          <div class="flex flex-wrap justify-between gap-3 p-4">
            <div class="flex min-w-72 flex-col gap-2">
              <h1 class="text-text-light dark:text-text-dark text-4xl font-black leading-tight tracking-[-0.033em]">
                Create a New Agent
              </h1>
              <p class="text-subtext-light dark:text-subtext-dark text-base font-normal leading-normal">
                Select a template to get started or begin with a blank slate.
              </p>
            </div>
          </div>

          <!-- Templates Grid -->
          <div class="grid grid-cols-1 gap-6 p-4 sm:grid-cols-2 lg:grid-cols-3">
            <AgentTemplateCard
              v-for="template in templates"
              :key="template.id"
              :template="template"
              @select="handleTemplateSelect"
            />
          </div>

          <!-- Start from Scratch (Disabled) -->
          <div class="flex flex-col p-4 mt-6">
            <div
              class="flex flex-col items-center justify-center gap-4 rounded-xl border-2 border-dashed border-border-light/70 dark:border-border-dark/70 bg-card-light/50 dark:bg-card-dark/50 px-6 py-10 text-center opacity-60 cursor-not-allowed"
            >
              <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-gray-200 dark:bg-gray-700">
                <span class="material-symbols-outlined text-3xl text-subtext-light dark:text-subtext-dark">
                  add
                </span>
              </div>
              <div class="flex max-w-md flex-col items-center gap-1">
                <p class="text-text-light dark:text-text-dark text-lg font-bold leading-tight tracking-[-0.015em]">
                  Start from Scratch
                </p>
                <p class="text-subtext-light dark:text-subtext-dark text-sm font-normal leading-normal">
                  Build a custom agent from the ground up without any pre-configured settings.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'
import AgentTemplateCard from '@/components/AgentTemplateCard.vue'

const router = useRouter()

// Templates data
const templates = ref([
  {
    id: 1,
    name: 'Call Router',
    description: 'Directs incoming calls to the correct department or individual based on caller needs.',
    icon: 'route',
    color: 'indigo'
  },
  {
    id: 2,
    name: 'Receptionist',
    description: 'Handles general inquiries, provides information, and forwards calls like a virtual front desk.',
    icon: 'concierge',
    color: 'teal'
  },
  {
    id: 3,
    name: 'Booker (booking agent)',
    description: 'Schedules appointments, reservations, or consultations directly with customers.',
    icon: 'calendar_add_on',
    color: 'amber'
  },
  {
    id: 4,
    name: 'Order Management',
    description: 'Assists with getting order statuses, placing new orders, and processing returns.',
    icon: 'receipt_long',
    color: 'green'
  },
  {
    id: 5,
    name: 'Customer Service',
    description: 'Pre-configured for handling support queries, FAQs, and ticket creation.',
    icon: 'support_agent',
    color: 'blue'
  },
  {
    id: 6,
    name: 'Lead Caller',
    description: 'Optimized for qualifying leads, collecting contact info, and setting up follow-ups.',
    icon: 'filter_alt',
    color: 'orange'
  }
])

// Handle template selection
const handleTemplateSelect = (template) => {
  console.log('Template selected:', template)
  // Redirect be configure page ba template name
  router.push({
    path: '/agents/configure',
    query: { template: template.name }
  })
}
</script>
