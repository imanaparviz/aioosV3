<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark">
      <div class="flex h-full grow flex-col items-center justify-center py-10 px-4 sm:px-6 lg:px-8">
        <div class="w-full max-w-4xl">
        <!-- Header & Navigation -->
        <div class="mb-8 space-y-4">
          <router-link
            to="/agents/configure"
            class="inline-flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-primary dark:text-gray-400 dark:hover:text-primary"
          >
            <span class="material-symbols-outlined">arrow_back</span>
            Back to Configuration
          </router-link>

          <!-- Breadcrumb -->
          <div class="flex flex-wrap items-center gap-2 font-medium text-gray-500 dark:text-gray-400">
            <router-link to="/agents/create" class="hover:text-primary">Setup</router-link>
            <span class="material-symbols-outlined text-lg">chevron_right</span>
            <router-link to="/agents/configure" class="hover:text-primary">Configure</router-link>
            <span class="material-symbols-outlined text-lg">chevron_right</span>
            <span class="font-bold text-gray-900 dark:text-white">Number</span>
          </div>

          <!-- Title -->
          <div class="flex flex-col gap-2">
            <h1 class="text-4xl font-black tracking-tighter text-gray-900 dark:text-white">
              Assign a phone number
            </h1>
            <p class="text-base text-gray-600 dark:text-gray-300">
              Provide a dedicated number for your new agent or skip for now.
            </p>
          </div>
        </div>

        <!-- Main Content Area -->
        <div v-if="!isSuccess" class="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800">
          <div class="p-6 sm:p-8">
            <fieldset class="flex flex-col gap-4">
              <legend class="sr-only">Phone Number Assignment Options</legend>

              <!-- Option 1: Assign a phone number -->
              <label
                class="flex cursor-pointer items-start gap-4 rounded-lg border border-gray-200 p-4 transition-all dark:border-gray-700"
                :class="{
                  'border-primary ring-2 ring-primary/20 dark:border-primary': selectedOption === 'assign'
                }"
              >
                <input
                  v-model="selectedOption"
                  class="mt-1 h-5 w-5 shrink-0 border-2 border-gray-300 bg-transparent text-transparent checked:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 focus:ring-offset-white dark:border-gray-600 dark:checked:border-primary dark:focus:ring-offset-gray-800"
                  name="phone-option"
                  type="radio"
                  value="assign"
                />
                <div class="flex w-full flex-col gap-4">
                  <div class="flex grow flex-col">
                    <p class="text-base font-medium text-gray-900 dark:text-white">
                      Assign a phone number
                    </p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">
                      Select an available number from your organization's pool.
                    </p>
                  </div>

                  <!-- Conditional Dropdown Section -->
                  <div v-if="selectedOption === 'assign'" class="w-full max-w-md">
                    <label class="flex flex-col">
                      <p class="pb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                        Phone Number
                      </p>
                      <select
                        v-model="selectedPhoneNumber"
                        class="form-select w-full rounded-lg border-gray-300 bg-gray-50 text-gray-900 shadow-sm focus:border-primary focus:ring-primary/50 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                      >
                        <option disabled value="">Select a number...</option>
                        <option value="1">+1 (555) 123-4567 - San Francisco, CA</option>
                        <option value="2">+44 20 7946 0958 - London, UK</option>
                        <option value="3">+1 (800) 555-0199 - Toll-Free</option>
                      </select>
                    </label>
                  </div>
                </div>
              </label>

              <!-- Option 2: Skip for now -->
              <label
                class="flex cursor-pointer items-start gap-4 rounded-lg border border-gray-200 p-4 transition-all dark:border-gray-700"
                :class="{
                  'border-primary ring-2 ring-primary/20 dark:border-primary': selectedOption === 'skip'
                }"
              >
                <input
                  v-model="selectedOption"
                  class="mt-1 h-5 w-5 shrink-0 border-2 border-gray-300 bg-transparent text-transparent checked:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 focus:ring-offset-white dark:border-gray-600 dark:checked:border-primary dark:focus:ring-offset-gray-800"
                  name="phone-option"
                  type="radio"
                  value="skip"
                />
                <div class="flex w-full flex-col gap-4">
                  <div class="flex grow flex-col">
                    <p class="text-base font-medium text-gray-900 dark:text-white">
                      Skip for now
                    </p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">
                      You can assign a number later from the agent's settings page.
                    </p>
                  </div>

                  <!-- Conditional Info Box -->
                  <div
                    v-if="selectedOption === 'skip'"
                    class="flex items-center gap-3 rounded-lg bg-yellow-100 p-4 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300"
                  >
                    <span class="material-symbols-outlined text-yellow-600 dark:text-yellow-400">info</span>
                    <p class="text-sm">
                      The agent will be created without a number. You can assign one at any time from the agent's configuration.
                    </p>
                  </div>
                </div>
              </label>
            </fieldset>
          </div>

          <!-- Action Bar -->
          <div class="flex items-center justify-end gap-4 rounded-b-xl border-t border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-800/50">
            <button
              @click="handleCancel"
              class="rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:ring-gray-600 dark:hover:bg-gray-600"
              type="button"
            >
              Cancel
            </button>
            <button
              @click="handleComplete"
              :disabled="isLoading || (selectedOption === 'assign' && !selectedPhoneNumber)"
              class="rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:cursor-not-allowed disabled:bg-gray-300 dark:disabled:bg-gray-600"
              type="submit"
            >
              {{ isLoading ? 'Creating...' : 'Complete Setup' }}
            </button>
          </div>
        </div>

        <!-- Error State -->
        <div
          v-if="errorMessage"
          class="mt-4 flex items-center gap-3 rounded-lg bg-error/10 p-4 text-error dark:bg-error/20 dark:text-red-400"
        >
          <span class="material-symbols-outlined">error</span>
          <p class="text-sm font-medium">{{ errorMessage }}</p>
        </div>

        <!-- Success State -->
        <div
          v-if="isSuccess"
          class="flex flex-col items-center justify-center rounded-xl border border-gray-200 bg-white p-12 text-center shadow-sm dark:border-gray-700 dark:bg-gray-800"
        >
          <div class="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-success/10">
            <span class="material-symbols-outlined text-4xl text-success">check_circle</span>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
            Agent Created Successfully!
          </h2>
          <p class="mt-2 max-w-md text-gray-600 dark:text-gray-300">
            Your new agent is now configured and ready to be used. You can view the agent's details or create another one.
          </p>
          <div class="mt-8 flex flex-wrap justify-center gap-4">
            <button
              @click="handleCreateAnother"
              class="rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:ring-gray-600 dark:hover:bg-gray-600"
              type="button"
            >
              Create Another Agent
            </button>
            <button
              @click="handleViewDetails"
              class="rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary/90"
              type="button"
            >
              View Agent Details
            </button>
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

const router = useRouter()

// State
const selectedOption = ref('skip')  // Default to skip for easier flow
const selectedPhoneNumber = ref('')
const isLoading = ref(false)
const isSuccess = ref(false)
const errorMessage = ref('')

// Actions
const handleCancel = () => {
  if (confirm('Are you sure you want to cancel? All progress will be lost.')) {
    router.push('/dashboard')
  }
}

const handleComplete = async () => {
  // Validation
  if (selectedOption.value === 'assign' && !selectedPhoneNumber.value) {
    errorMessage.value = 'Please select a phone number.'
    return
  }

  errorMessage.value = ''
  isLoading.value = true

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Success!
    isSuccess.value = true
    console.log('Agent created successfully!', {
      option: selectedOption.value,
      phoneNumber: selectedPhoneNumber.value
    })
  } catch (error) {
    errorMessage.value = 'Unable to create agent. An unexpected error occurred. Please try again.'
    console.error('Error creating agent:', error)
  } finally {
    isLoading.value = false
  }
}

const handleCreateAnother = () => {
  router.push('/agents/create')
}

const handleViewDetails = () => {
  // In real implementation, this would use the actual agent ID returned from API
  const mockAgentId = 'new-agent-' + Date.now()
  router.push(`/agents/${mockAgentId}?name=${encodeURIComponent('New Agent')}`)
}
</script>
