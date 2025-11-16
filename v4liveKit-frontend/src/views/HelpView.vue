<template>
  <div class="flex min-h-screen w-full">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-6 lg:p-10">
      <div class="mx-auto max-w-5xl">
        <!-- Header with Search -->
        <div class="mb-12 text-center">
          <h1 class="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">Help & Support</h1>
          <p class="mt-2 text-lg text-gray-600 dark:text-gray-400">We're here to help. Find the answers you need.</p>

          <!-- Search Bar -->
          <div class="relative mx-auto mt-6 max-w-2xl">
            <span class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
              <span class="material-symbols-outlined">search</span>
            </span>
            <input
              v-model="searchQuery"
              @input="handleSearch"
              class="block w-full rounded-full border-gray-300 bg-white py-3 pl-12 pr-4 text-base shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-900/50 dark:text-white"
              placeholder="Search for articles, topics..."
              type="search"
            />
          </div>
        </div>

        <!-- Two Column Layout -->
        <div class="grid grid-cols-1 gap-10 lg:grid-cols-3">
          <!-- FAQ Section (2/3 width) -->
          <div class="lg:col-span-2">
            <h2 class="mb-6 text-2xl font-semibold text-gray-900 dark:text-white">Frequently Asked Questions</h2>

            <div class="space-y-6">
              <!-- Getting Started -->
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white">Getting Started</h3>
                <div class="mt-2 space-y-2 border-l-2 border-gray-200 pl-4 dark:border-gray-700">
                  <a
                    v-for="question in faqCategories.gettingStarted"
                    :key="question"
                    @click.prevent="handleQuestionClick(question)"
                    class="block text-gray-600 hover:text-primary cursor-pointer dark:text-gray-400 dark:hover:text-primary-hover"
                    href="#"
                  >
                    {{ question }}
                  </a>
                </div>
              </div>

              <!-- Account Management -->
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white">Account Management</h3>
                <div class="mt-2 space-y-2 border-l-2 border-gray-200 pl-4 dark:border-gray-700">
                  <a
                    v-for="question in faqCategories.accountManagement"
                    :key="question"
                    @click.prevent="handleQuestionClick(question)"
                    class="block text-gray-600 hover:text-primary cursor-pointer dark:text-gray-400 dark:hover:text-primary-hover"
                    href="#"
                  >
                    {{ question }}
                  </a>
                </div>
              </div>

              <!-- Troubleshooting -->
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white">Troubleshooting</h3>
                <div class="mt-2 space-y-2 border-l-2 border-gray-200 pl-4 dark:border-gray-700">
                  <a
                    v-for="question in faqCategories.troubleshooting"
                    :key="question"
                    @click.prevent="handleQuestionClick(question)"
                    class="block text-gray-600 hover:text-primary cursor-pointer dark:text-gray-400 dark:hover:text-primary-hover"
                    href="#"
                  >
                    {{ question }}
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Section (1/3 width) -->
          <div class="lg:col-span-1">
            <div class="rounded-xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900/50">
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                Can't find what you're looking for?
              </h3>
              <p class="mt-2 text-gray-600 dark:text-gray-400">
                Our support team is always ready to help. Reach out to us for any questions.
              </p>

              <!-- Contact Options -->
              <div class="mt-6 space-y-4">
                <!-- Email Support -->
                <a
                  @click.prevent="handleEmailSupport"
                  class="group flex items-center gap-4 rounded-lg border border-gray-200 p-4 transition-colors hover:bg-gray-50 cursor-pointer dark:border-gray-700 dark:hover:bg-gray-800/50"
                  href="#"
                >
                  <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary dark:bg-primary/20">
                    <span class="material-symbols-outlined">mail</span>
                  </div>
                  <div>
                    <p class="font-medium text-gray-900 dark:text-white">Email Support</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">support@agentapp.com</p>
                  </div>
                </a>

                <!-- Live Chat -->
                <a
                  @click.prevent="handleLiveChat"
                  class="group flex items-center gap-4 rounded-lg border border-gray-200 p-4 transition-colors hover:bg-gray-50 cursor-pointer dark:border-gray-700 dark:hover:bg-gray-800/50"
                  href="#"
                >
                  <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary dark:bg-primary/20">
                    <span class="material-symbols-outlined">chat_bubble</span>
                  </div>
                  <div>
                    <p class="font-medium text-gray-900 dark:text-white">Live Chat</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">Chat with us now</p>
                  </div>
                </a>

                <!-- Documentation -->
                <a
                  @click.prevent="handleDocumentation"
                  class="group flex items-center gap-4 rounded-lg border border-gray-200 p-4 transition-colors hover:bg-gray-50 cursor-pointer dark:border-gray-700 dark:hover:bg-gray-800/50"
                  href="#"
                >
                  <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary dark:bg-primary/20">
                    <span class="material-symbols-outlined">menu_book</span>
                  </div>
                  <div>
                    <p class="font-medium text-gray-900 dark:text-white">Documentation</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">View our full guides</p>
                  </div>
                </a>
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

const router = useRouter()

// Search
const searchQuery = ref('')

// FAQ Categories
const faqCategories = ref({
  gettingStarted: [
    'How do I create a new voice agent?',
    'What are the system requirements?',
    'Understanding the dashboard layout.'
  ],
  accountManagement: [
    'How can I change my password?',
    'Updating your billing information.',
    'How do I close my account?'
  ],
  troubleshooting: [
    'Voice agent is not responding.',
    'Issues with API integrations.',
    'Resolving common error codes.'
  ]
})

// Methods
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    console.log('Searching for:', searchQuery.value)
    // In real implementation, this would filter FAQ results
  }
}

const handleQuestionClick = (question) => {
  console.log('Opening article:', question)
  alert(`Article: ${question}\n\nThis would open a detailed help article with step-by-step instructions.\n\nIn the full implementation, this would navigate to a dedicated article page.`)
}

const handleEmailSupport = () => {
  window.location.href = 'mailto:support@agentapp.com'
}

const handleLiveChat = () => {
  alert('Live Chat\n\nOpening live chat...\n\nIn the full implementation, this would open a chat widget or redirect to a live chat platform.')
}

const handleDocumentation = () => {
  alert('Documentation\n\nThis would open the complete documentation portal with:\n- API Reference\n- Integration Guides\n- Best Practices\n- Video Tutorials\n\nIn the full implementation, this might open a separate docs site.')
}
</script>
