<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <div class="mx-auto flex max-w-7xl flex-col gap-6">
        <!-- Header -->
        <header class="sticky top-0 backdrop-blur-sm z-10 py-4 -mx-8 px-8 mb-6 flex flex-wrap justify-between gap-3">
          <div class="flex min-w-72 flex-col gap-3">
            <h1 class="text-slate-900 dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">
              API & Webhooks
            </h1>
            <p class="text-slate-600 dark:text-slate-400 text-base font-normal leading-normal">
              Manage API keys and configure webhooks for your application.
            </p>
          </div>
        </header>

        <!-- Tabs -->
        <div class="pb-3">
          <div class="flex border-b border-slate-200 dark:border-slate-800 gap-8">
            <button
              @click="activeTab = 'api-keys'"
              class="flex flex-col items-center justify-center border-b-[3px] pb-[13px] pt-4"
              :class="activeTab === 'api-keys'
                ? 'border-b-primary text-primary'
                : 'border-b-transparent text-slate-400 hover:text-slate-600'"
            >
              <p class="text-sm font-bold leading-normal tracking-[0.015em]">API Keys</p>
            </button>
            <button
              @click="activeTab = 'webhooks'"
              class="flex flex-col items-center justify-center border-b-[3px] pb-[13px] pt-4"
              :class="activeTab === 'webhooks'
                ? 'border-b-primary text-primary'
                : 'border-b-transparent text-slate-400 hover:text-slate-600'"
            >
              <p class="text-sm font-bold leading-normal tracking-[0.015em]">Webhooks</p>
            </button>
            <button
              @click="activeTab = 'documentation'"
              class="flex flex-col items-center justify-center border-b-[3px] pb-[13px] pt-4"
              :class="activeTab === 'documentation'
                ? 'border-b-primary text-primary'
                : 'border-b-transparent text-slate-400 hover:text-slate-600'"
            >
              <p class="text-sm font-bold leading-normal tracking-[0.015em]">API Documentation</p>
            </button>
          </div>
        </div>

        <!-- API Keys Tab Content -->
        <div v-if="activeTab === 'api-keys'" class="flex flex-col gap-6">
          <!-- Header with Create Button -->
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-2xl font-bold text-slate-900 dark:text-white">API Keys</h2>
              <p class="text-slate-600 dark:text-slate-400 mt-1">
                Manage your API keys to authenticate requests to the Voice Agent API.
              </p>
            </div>
            <button
              @click="handleCreateKey"
              class="inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-bold text-white hover:bg-primary/90"
            >
              <span class="material-symbols-outlined !text-[18px]">add</span>
              <span>Create New Key</span>
            </button>
          </div>

          <!-- API Keys List -->
          <div class="rounded-lg border border-slate-200 dark:border-slate-800 bg-white/80 backdrop-blur-md dark:bg-slate-900/50 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
                <thead class="bg-slate-50/80 dark:bg-slate-800/50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Name</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Key</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Type</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Created</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Last Used</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white/80 dark:bg-slate-900/50 divide-y divide-slate-200 dark:divide-slate-800">
                  <tr v-for="key in apiKeys" :key="key.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/30">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-slate-900 dark:text-white">{{ key.name }}</div>
                      <div class="text-xs text-slate-500 dark:text-slate-400">{{ key.permissions }}</div>
                    </td>
                    <td class="px-6 py-4">
                      <div class="flex items-center gap-2">
                        <code class="text-xs bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded font-mono text-slate-700 dark:text-slate-300">
                          {{ key.key.substring(0, 20) }}...
                        </code>
                        <button
                          @click="handleCopyKey(key.key)"
                          class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                          title="Copy to clipboard"
                        >
                          <span class="material-symbols-outlined !text-[18px]">content_copy</span>
                        </button>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                        :class="key.type === 'Live'
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                          : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'"
                      >
                        {{ key.type }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 dark:text-slate-400">
                      {{ key.created }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 dark:text-slate-400">
                      {{ key.lastUsed }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                      <button
                        @click="handleRevokeKey(key.id)"
                        class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-medium"
                      >
                        Revoke
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Create Key Modal -->
          <div v-if="showCreateKeyModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showCreateKeyModal = false">
            <div class="bg-white dark:bg-slate-900 rounded-lg p-6 max-w-md w-full mx-4">
              <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-4">Create New API Key</h3>

              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Key Name</label>
                  <input
                    v-model="newKeyName"
                    type="text"
                    placeholder="e.g., Production API Key"
                    class="w-full px-3 py-2 border border-slate-300 dark:border-slate-700 rounded-lg bg-white/80 backdrop-blur-md dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Permissions</label>
                  <select
                    v-model="newKeyPermissions"
                    class="w-full px-3 py-2 border border-slate-300 dark:border-slate-700 rounded-lg bg-white/80 backdrop-blur-md dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                  >
                    <option>Full Access</option>
                    <option>Read Only</option>
                    <option>Write Only</option>
                  </select>
                </div>
              </div>

              <div class="flex gap-3 mt-6">
                <button
                  @click="showCreateKeyModal = false"
                  class="flex-1 px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  @click="handleSaveNewKey"
                  class="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90"
                >
                  Create Key
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Webhooks Tab Content -->
        <div v-if="activeTab === 'webhooks'" class="flex flex-col gap-6">
          <!-- Header with Add Button -->
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Webhooks</h2>
              <p class="text-slate-600 dark:text-slate-400 mt-1">
                Configure webhook endpoints to receive real-time notifications about events.
              </p>
            </div>
            <button
              @click="handleAddWebhook"
              class="inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-bold text-white hover:bg-primary/90"
            >
              <span class="material-symbols-outlined !text-[18px]">add</span>
              <span>Add Webhook</span>
            </button>
          </div>

          <!-- Webhooks List -->
          <div class="space-y-4">
            <div
              v-for="webhook in webhooks"
              :key="webhook.id"
              class="rounded-lg border border-slate-200 dark:border-slate-800 bg-white/80 backdrop-blur-md dark:bg-slate-900/50 p-6"
            >
              <div class="flex items-start justify-between mb-4">
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-2">
                    <code class="text-sm bg-slate-100 dark:bg-slate-800 px-3 py-1 rounded font-mono text-slate-700 dark:text-slate-300">
                      {{ webhook.url }}
                    </code>
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
                    >
                      {{ webhook.status }}
                    </span>
                  </div>

                  <div class="flex flex-wrap gap-2 mb-3">
                    <span
                      v-for="event in webhook.events"
                      :key="event"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-primary/10 text-primary"
                    >
                      {{ event }}
                    </span>
                  </div>

                  <div class="flex gap-4 text-sm text-slate-600 dark:text-slate-400">
                    <span>Last delivery: {{ webhook.lastDelivery }}</span>
                    <span>•</span>
                    <span>Success rate: {{ webhook.deliveryRate }}</span>
                  </div>
                </div>

                <div class="flex gap-2">
                  <button
                    @click="handleTestWebhook(webhook)"
                    class="px-3 py-1.5 text-sm border border-slate-300 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
                  >
                    Test
                  </button>
                  <button
                    @click="handleDeleteWebhook(webhook.id)"
                    class="px-3 py-1.5 text-sm text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 font-medium"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Add Webhook Modal -->
          <div v-if="showAddWebhookModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showAddWebhookModal = false">
            <div class="bg-white dark:bg-slate-900 rounded-lg p-6 max-w-md w-full mx-4">
              <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-4">Add Webhook</h3>

              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Webhook URL</label>
                  <input
                    v-model="newWebhookUrl"
                    type="url"
                    placeholder="https://your-domain.com/webhook"
                    class="w-full px-3 py-2 border border-slate-300 dark:border-slate-700 rounded-lg bg-white/80 backdrop-blur-md dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Events</label>
                  <div class="space-y-2 max-h-48 overflow-y-auto">
                    <label
                      v-for="event in availableEvents"
                      :key="event"
                      class="flex items-center gap-2 p-2 rounded hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        :value="event"
                        @change="toggleEvent(event)"
                        :checked="selectedEvents.includes(event)"
                        class="rounded border-slate-300 dark:border-slate-700 text-primary focus:ring-primary"
                      />
                      <span class="text-sm text-slate-700 dark:text-slate-300">{{ event }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <div class="flex gap-3 mt-6">
                <button
                  @click="showAddWebhookModal = false"
                  class="flex-1 px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  @click="handleSaveWebhook"
                  class="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90"
                >
                  Add Webhook
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Documentation Tab Content -->
        <div v-if="activeTab === 'documentation'" class="flex flex-col gap-6">
          <!-- Getting Started -->
          <div class="flex flex-col gap-4">
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Getting Started</h2>
            <p class="text-slate-600 dark:text-slate-400">
              Our API provides programmatic access to your voice agents. To get started, you'll need to authenticate your requests using an API key.
            </p>
          </div>

          <!-- Authentication -->
          <div class="flex flex-col gap-4">
            <h3 class="text-xl font-semibold text-slate-900 dark:text-white">Authentication</h3>
            <p class="text-slate-600 dark:text-slate-400">
              Authenticate your API requests by including your secret key in the request headers. All API requests must be made over HTTPS.
            </p>
            <div class="rounded-lg border border-slate-300 dark:border-slate-800 bg-slate-900 dark:bg-surface-dark p-4 font-mono text-sm overflow-x-auto">
              <p class="text-slate-400"># All API requests should be authenticated with a Bearer token</p>
              <p class="text-slate-200">
                <span class="text-sky-400">Authorization</span>:
                <span class="text-green-400">Bearer</span>
                <span class="text-amber-300">&lt;YOUR_API_KEY&gt;</span>
              </p>
            </div>
          </div>

          <!-- Example Request -->
          <div class="flex flex-col gap-4">
            <h3 class="text-xl font-semibold text-slate-900 dark:text-white">Example Request</h3>
            <p class="text-slate-600 dark:text-slate-400">
              Here's an example of how to create a new voice agent using our API.
            </p>
            <div class="rounded-lg border border-slate-300 dark:border-slate-800 bg-slate-900 dark:bg-surface-dark p-4 font-mono text-sm overflow-x-auto">
              <pre class="text-slate-300"><code><span class="text-violet-400">curl</span> <span class="text-green-400">-X</span> POST \
  <span class="text-amber-300">https://api.voiceagent.inc/v1/agents</span> \
  <span class="text-green-400">-H</span> <span class="text-amber-300">'Authorization: Bearer sk_test_...'</span> \
  <span class="text-green-400">-H</span> <span class="text-amber-300">'Content-Type: application/json'</span> \
  <span class="text-green-400">-d</span> <span class="text-amber-300">'{
    "name": "My First Agent",
    "voice_id": "voice_abc123",
    "initial_prompt": "Hello, how can I help you today?"
  }'</span></code></pre>
            </div>
          </div>

          <!-- Example Response -->
          <div class="flex flex-col gap-4">
            <h3 class="text-xl font-semibold text-slate-900 dark:text-white">Example Response</h3>
            <div class="rounded-lg border border-slate-300 dark:border-slate-800 bg-slate-900 dark:bg-surface-dark p-4 font-mono text-sm overflow-x-auto">
              <pre class="text-slate-300"><code>{
  <span class="text-sky-400">"id"</span>: <span class="text-amber-300">"agent_xyz789"</span>,
  <span class="text-sky-400">"object"</span>: <span class="text-amber-300">"agent"</span>,
  <span class="text-sky-400">"created"</span>: <span class="text-red-400">1678886400</span>,
  <span class="text-sky-400">"name"</span>: <span class="text-amber-300">"My First Agent"</span>,
  <span class="text-sky-400">"voice_id"</span>: <span class="text-amber-300">"voice_abc123"</span>,
  <span class="text-sky-400">"initial_prompt"</span>: <span class="text-amber-300">"Hello, how can I help you today?"</span>
}</code></pre>
            </div>
          </div>

          <!-- CTA Button -->
          <div class="mt-4">
            <button
              @click="handleViewDocs"
              class="inline-flex cursor-pointer items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-bold text-white hover:bg-primary/90"
            >
              <span>View Full API Reference</span>
              <span class="material-symbols-outlined !text-[18px]">arrow_forward</span>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SidebarNav from '@/components/SidebarNav.vue'

const activeTab = ref('api-keys')

// API Keys data
const apiKeys = ref([
  {
    id: 1,
    name: 'Production Key',
    key: 'sk_live_4f8a9b2c1d3e5f6a7b8c9d0e1f2a3b4c',
    type: 'Live',
    created: '2024-01-15',
    lastUsed: '2 hours ago',
    permissions: 'Full Access'
  },
  {
    id: 2,
    name: 'Development Key',
    key: 'sk_test_1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d',
    type: 'Test',
    created: '2024-01-10',
    lastUsed: '5 minutes ago',
    permissions: 'Read Only'
  }
])

const showCreateKeyModal = ref(false)
const newKeyName = ref('')
const newKeyPermissions = ref('Full Access')

// Webhooks data
const webhooks = ref([
  {
    id: 1,
    url: 'https://api.myapp.com/webhooks/calls',
    events: ['call.started', 'call.ended', 'call.failed'],
    status: 'Active',
    lastDelivery: '2 minutes ago',
    deliveryRate: '99.8%'
  },
  {
    id: 2,
    url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX',
    events: ['transcription.ready'],
    status: 'Active',
    lastDelivery: '1 hour ago',
    deliveryRate: '100%'
  }
])

const showAddWebhookModal = ref(false)
const newWebhookUrl = ref('')
const selectedEvents = ref([])

const availableEvents = [
  'call.started',
  'call.ended',
  'call.failed',
  'call.completed',
  'transcription.ready',
  'transcription.failed',
  'agent.updated'
]

// Methods
const handleCreateKey = () => {
  showCreateKeyModal.value = true
}

const handleCopyKey = (key) => {
  navigator.clipboard.writeText(key)
  alert('API Key copied to clipboard!')
}

const handleRevokeKey = (id) => {
  if (confirm('Are you sure you want to revoke this API key? This action cannot be undone.')) {
    apiKeys.value = apiKeys.value.filter(k => k.id !== id)
    alert('API key revoked successfully!')
  }
}

const handleSaveNewKey = () => {
  if (!newKeyName.value) {
    alert('Please enter a key name')
    return
  }

  const newKey = {
    id: apiKeys.value.length + 1,
    name: newKeyName.value,
    key: 'sk_live_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15),
    type: 'Live',
    created: new Date().toISOString().split('T')[0],
    lastUsed: 'Never',
    permissions: newKeyPermissions.value
  }

  apiKeys.value.push(newKey)
  showCreateKeyModal.value = false
  newKeyName.value = ''
  newKeyPermissions.value = 'Full Access'

  alert('New API key created!\n\nMake sure to copy it now. You won\'t be able to see it again!')
}

const handleAddWebhook = () => {
  showAddWebhookModal.value = true
}

const handleSaveWebhook = () => {
  if (!newWebhookUrl.value) {
    alert('Please enter a webhook URL')
    return
  }
  if (selectedEvents.value.length === 0) {
    alert('Please select at least one event')
    return
  }

  const newWebhook = {
    id: webhooks.value.length + 1,
    url: newWebhookUrl.value,
    events: [...selectedEvents.value],
    status: 'Active',
    lastDelivery: 'Never',
    deliveryRate: 'N/A'
  }

  webhooks.value.push(newWebhook)
  showAddWebhookModal.value = false
  newWebhookUrl.value = ''
  selectedEvents.value = []

  alert('Webhook created successfully!')
}

const handleTestWebhook = (webhook) => {
  alert(`Testing webhook: ${webhook.url}\n\nSending test payload...`)
}

const handleDeleteWebhook = (id) => {
  if (confirm('Are you sure you want to delete this webhook?')) {
    webhooks.value = webhooks.value.filter(w => w.id !== id)
    alert('Webhook deleted successfully!')
  }
}

const handleViewDocs = () => {
  alert('View Full API Reference\n\nThis would open the complete API documentation in a new tab.')
}

const toggleEvent = (event) => {
  const index = selectedEvents.value.indexOf(event)
  if (index > -1) {
    selectedEvents.value.splice(index, 1)
  } else {
    selectedEvents.value.push(event)
  }
}
</script>

<style scoped>
/* Ensure code blocks don't break layout */
pre {
  white-space: pre;
  word-wrap: normal;
  overflow-x: auto;
}

code {
  display: block;
}
</style>
