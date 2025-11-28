<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex flex-col gap-6">
        <!-- Back Navigation & Progress -->
        <div class="flex flex-col gap-4">
          <router-link
            to="/agents/create"
            class="flex items-center gap-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-primary"
          >
            <span class="material-symbols-outlined text-base">arrow_back</span>
            Back to Agents
          </router-link>

          <!-- Progress Bar (inline) -->
          <div class="flex flex-col gap-3">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-gray-900 dark:text-white">Step 2 of 3</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">Configuration</p>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div class="bg-primary-blue h-2 rounded-full" style="width: 66%;"></div>
            </div>
          </div>
        </div>

        <!-- Page Heading -->
        <div class="flex flex-wrap justify-between items-start gap-3">
          <div class="flex flex-col gap-2">
            <div class="flex items-center gap-3">
              <p class="text-warning-yellow bg-yellow-400/20 text-xs font-bold py-1 px-3 rounded-md">
                {{ templateName }}
              </p>
            </div>
            <h1 class="text-3xl font-black text-gray-900 dark:text-white">
              Create a new agent
            </h1>
            <p class="text-base text-gray-600 dark:text-gray-400">
              Configure your {{ templateName }} to direct callers to the correct department.
            </p>
          </div>
        </div>

        <!-- Form Container -->
        <div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <form @submit.prevent="handleSubmit" class="flex flex-col divide-y divide-gray-200 dark:divide-gray-700">
            <!-- Section: Basic Information -->
            <div class="p-6 md:p-8">
              <h2 class="text-lg font-bold text-gray-900 dark:text-white pb-1">Basic Information</h2>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
                Give your agent a unique name and description.
              </p>
              <div class="grid grid-cols-1 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-900 dark:text-gray-300 mb-1.5" for="agent-name">
                    Agent Name
                  </label>
                  <input
                    v-model="formData.name"
                    class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-900 dark:text-white shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                    id="agent-name"
                    placeholder="e.g., Main Office Router"
                    type="text"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-900 dark:text-gray-300 mb-1.5" for="agent-description">
                    Description (Optional)
                  </label>
                  <textarea
                    v-model="formData.description"
                    class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-900 dark:text-white shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                    id="agent-description"
                    placeholder="Describe the purpose of this agent..."
                    rows="3"
                  ></textarea>
                </div>
              </div>
            </div>

            <!-- Section: Language & Region -->
            <div class="p-6 md:p-8">
              <h2 class="text-lg font-bold text-gray-900 dark:text-white pb-1">Language &amp; Region</h2>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
                Select the primary language your agent will use.
              </p>
              <div>
                <label class="block text-sm font-medium text-gray-900 dark:text-gray-300 mb-1.5" for="language-selection">
                  Language
                </label>
                <select
                  v-model="formData.language"
                  class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-900 dark:text-white shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                  id="language-selection"
                >
                  <option value="en-US">English (United States)</option>
                  <option value="es-ES">Spanish (Spain)</option>
                  <option value="fr-FR">French (France)</option>
                </select>
              </div>
            </div>

            <!-- Section: Conversation Messages -->
            <div class="p-6 md:p-8">
              <h2 class="text-lg font-bold text-gray-900 dark:text-white pb-1">Conversation Messages</h2>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
                Customize the messages callers will hear.
              </p>
              <div class="grid grid-cols-1 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-900 dark:text-gray-300 mb-1.5" for="welcome-message">
                    Welcome Message
                  </label>
                  <textarea
                    v-model="formData.welcomeMessage"
                    class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-900 dark:text-white shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                    id="welcome-message"
                    placeholder="e.g., Thank you for calling. Please tell me which department you'd like to reach."
                    rows="3"
                  ></textarea>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-900 dark:text-gray-300 mb-1.5" for="transfer-message">
                    Transfer Message
                  </label>
                  <textarea
                    v-model="formData.transferMessage"
                    class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-900 dark:text-white shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                    id="transfer-message"
                    placeholder="e.g., One moment while I connect you to..."
                    rows="3"
                  ></textarea>
                  <div class="mt-2 flex items-center gap-2">
                    <button
                      @click="insertVariable"
                      class="text-sm font-medium text-primary hover:underline"
                      type="button"
                    >
                      + Insert Variable
                    </button>
                    <span class="inline-flex items-center rounded-md bg-blue-100 dark:bg-blue-900/50 px-2 py-0.5 text-xs font-semibold text-blue-700 dark:text-blue-300">
                      &#123;&#123;department.name&#125;&#125;
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Section: Departments -->
            <div class="p-6 md:p-8">
              <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
                <div class="flex-grow">
                  <h2 class="text-lg font-bold text-gray-900 dark:text-white pb-1">Departments</h2>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    Define the departments callers can be routed to. A minimum of two is required.
                  </p>
                </div>
                <button
                  @click="addDepartment"
                  class="flex items-center justify-center gap-2 rounded-lg bg-primary/10 dark:bg-primary/20 px-4 py-2 text-sm font-bold text-primary hover:bg-primary/20 dark:hover:bg-primary/30 transition-colors"
                  type="button"
                >
                  <span class="material-symbols-outlined text-base">add</span>
                  <span>Add Department</span>
                </button>
              </div>

              <!-- Departments List -->
              <div v-if="departments.length > 0" class="flex flex-col gap-4">
                <div
                  v-for="dept in departments"
                  :key="dept.id"
                  class="flex items-center gap-4 rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900"
                >
                  <!-- Icon -->
                  <div class="flex-shrink-0 size-10 rounded-lg bg-primary/10 dark:bg-primary/20 flex items-center justify-center">
                    <span class="material-symbols-outlined text-primary">
                      {{ dept.icon }}
                    </span>
                  </div>

                  <!-- Department Info -->
                  <div class="flex-grow">
                    <p class="font-bold text-gray-900 dark:text-white">
                      {{ dept.name }}
                    </p>
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                      {{ dept.description }} {{ dept.phone ? `(${dept.phone})` : '' }}
                    </p>
                  </div>

                  <!-- Actions -->
                  <div class="flex items-center gap-2">
                    <button
                      @click="editDepartment(dept)"
                      class="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400 transition-colors"
                      type="button"
                    >
                      <span class="material-symbols-outlined text-lg">edit</span>
                    </button>
                    <button
                      @click="deleteDepartment(dept)"
                      class="p-2 rounded-md hover:bg-red-100 dark:hover:bg-red-900/50 text-red-600 transition-colors"
                      type="button"
                    >
                      <span class="material-symbols-outlined text-lg">delete</span>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else class="text-center py-12 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
                <span class="material-symbols-outlined text-5xl text-gray-400">group_off</span>
                <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-gray-300">No departments added</h3>
                <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
                  Get started by adding your first department.
                </p>
              </div>
            </div>
          </form>
        </div>
      </div>
      </div>
    </main>

    <!-- Sticky Footer for Actions -->
    <footer class="sticky bottom-0 z-10 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-t border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-end items-center gap-3">
          <button
            @click="handleCancel"
            class="rounded-lg px-4 py-2.5 text-sm font-bold text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            type="button"
          >
            Cancel
          </button>
          <button
            @click="handleSaveDraft"
            class="rounded-lg bg-gray-200 dark:bg-gray-600 px-4 py-2.5 text-sm font-bold text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors"
            type="button"
          >
            Save Draft
          </button>
          <button
            @click="handleSubmit"
            :disabled="loading"
            class="rounded-lg bg-primary px-4 py-2.5 text-sm font-bold text-white shadow-sm hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            type="submit"
          >
            <span v-if="loading" class="material-symbols-outlined animate-spin">sync</span>
            <span>{{ loading ? 'Creating Agent...' : 'Save & Deploy' }}</span>
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'
import { createAgent } from '@/services/api'

const router = useRouter()
const route = useRoute()

// Template name az route param
const templateName = ref(route.query.template || 'Call Router')

// Form data
const formData = ref({
  name: '',
  description: '',
  language: 'en-US',
  welcomeMessage: '',
  transferMessage: ''
})

// Loading & error states
const loading = ref(false)
const error = ref(null)
const success = ref(false)

// Departments (mock data)
const departments = ref([
  {
    id: 1,
    name: 'Sales',
    description: 'For new inquiries and purchases.',
    phone: '+1-202-555-0182',
    icon: 'support_agent'
  },
  {
    id: 2,
    name: 'Support',
    description: 'For technical assistance.',
    phone: '+1-202-555-0145',
    icon: 'help'
  }
])

// Actions
const addDepartment = () => {
  const newDept = {
    id: Date.now(),
    name: 'New Department',
    description: 'Description here',
    phone: '+1-202-555-0000',
    icon: 'business'
  }
  departments.value.push(newDept)
}

const editDepartment = (dept) => {
  console.log('Edit department:', dept)
  alert(`Edit department: ${dept.name}\n\nThis will open a modal in the full implementation!`)
}

const deleteDepartment = (dept) => {
  if (confirm(`Are you sure you want to delete ${dept.name}?`)) {
    departments.value = departments.value.filter(d => d.id !== dept.id)
  }
}

const insertVariable = () => {
  alert('Insert variable feature!\n\nThis will open a dropdown to select variables.')
}

const handleCancel = () => {
  if (confirm('Are you sure you want to cancel? Any unsaved changes will be lost.')) {
    router.push('/agents/create')
  }
}

const handleSaveDraft = () => {
  console.log('Saving draft...', formData.value, departments.value)
  alert('Draft saved successfully! ✅')
}

const handleSubmit = async () => {
  if (!formData.value.name.trim()) {
    alert('Please enter an agent name')
    return
  }

  loading.value = true
  error.value = null
  success.value = false

  try {
    // Build system instructions from welcome/transfer messages
    let systemInstructions = `You are a ${templateName.value} voice agent.\n\n`

    if (formData.value.welcomeMessage) {
      systemInstructions += `Welcome Message: ${formData.value.welcomeMessage}\n\n`
    }

    if (formData.value.transferMessage) {
      systemInstructions += `Transfer Message: ${formData.value.transferMessage}\n\n`
    }

    // Add departments info
    if (departments.value.length > 0) {
      systemInstructions += `Available Departments:\n`
      departments.value.forEach(dept => {
        systemInstructions += `- ${dept.name}: ${dept.description} (${dept.phone})\n`
      })
    }

    // Create agent data
    const agentData = {
      name: formData.value.name,
      description: formData.value.description || `${templateName.value} agent`,
      language: formData.value.language.split('-')[0], // en-US → en
      llm_model: 'gpt-4o-mini',
      temperature: 0.7,
      system_instructions: systemInstructions.trim()
    }

    console.log('Creating agent...', agentData)

    // Call API
    const createdAgent = await createAgent(agentData)

    console.log('✅ Agent created successfully:', createdAgent)
    success.value = true

    // Show success message
    alert(`🎉 Agent "${createdAgent.name}" created successfully!\n\nID: ${createdAgent.id}\nStatus: ${createdAgent.status}`)

    // Redirect to dashboard to see the new agent
    router.push('/dashboard')

  } catch (err) {
    console.error('❌ Failed to create agent:', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to create agent'
    alert(`Error creating agent: ${error.value}`)
  } finally {
    loading.value = false
  }
}
</script>
