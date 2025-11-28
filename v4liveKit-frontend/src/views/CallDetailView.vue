<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-6 lg:p-10 overflow-y-auto">
      <div class="mx-auto max-w-4xl">
        <!-- Breadcrumbs -->
        <div class="flex flex-wrap gap-2 items-center">
          <router-link
            to="/call-logs"
            class="text-slate-500 dark:text-slate-400 hover:text-primary text-base font-medium leading-normal"
          >
            Call Logs
          </router-link>
          <span class="material-symbols-outlined text-slate-500 dark:text-slate-400 text-lg">chevron_right</span>
          <span class="text-slate-900 dark:text-white text-base font-medium leading-normal">
            Call ID {{ callId }}
          </span>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="flex items-center justify-center py-20">
          <div class="text-center">
            <div class="inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-primary border-r-transparent"></div>
            <p class="mt-4 text-slate-600 dark:text-slate-400">Loading call details...</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="mt-8 p-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-red-600 dark:text-red-400 text-3xl">error</span>
            <div>
              <h3 class="text-lg font-bold text-red-900 dark:text-red-100">Failed to load call</h3>
              <p class="text-sm text-red-700 dark:text-red-300 mt-1">{{ error }}</p>
            </div>
          </div>
          <router-link to="/call-logs" class="mt-4 inline-flex items-center gap-2 text-red-600 dark:text-red-400 hover:underline">
            <span class="material-symbols-outlined">arrow_back</span>
            Back to Call Logs
          </router-link>
        </div>

        <!-- Call Content (only show when loaded) -->
        <div v-else>

        <!-- Page Heading & Actions -->
        <div class="flex flex-wrap justify-between items-start gap-4 mt-4">
          <div class="flex flex-col gap-1">
            <h1 class="text-slate-900 dark:text-white text-3xl lg:text-4xl font-black leading-tight tracking-[-0.033em]">
              Call ID {{ callId }}
            </h1>
            <p class="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">
              Caller: {{ callData.caller }} | {{ callData.date }}, {{ callData.time }}
            </p>
          </div>
          <div class="flex gap-3 flex-wrap">

            <button
              @click="handleViewTranscript"
              class="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-slate-50 dark:hover:bg-slate-700"
            >
              <span class="material-symbols-outlined text-lg">description</span>
              <span class="truncate">View Transcript</span>
            </button>
            <button
              @click="handleShareCall"
              class="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-slate-50 dark:hover:bg-slate-700"
            >
              <span class="material-symbols-outlined text-lg">share</span>
              <span class="truncate">Share Call</span>
            </button>
          </div>
        </div>

        <!-- Call Summary Section -->
        <section class="mt-8">
          <h2 class="text-slate-900 dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em]">
            Call Summary
          </h2>
          <div class="mt-4 grid grid-cols-2 md:grid-cols-3 gap-6 p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
            <div class="flex flex-col gap-1">
              <p class="text-sm text-slate-500 dark:text-slate-400">Duration</p>
              <p class="text-base font-medium text-slate-900 dark:text-white">{{ callData.duration }}</p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-sm text-slate-500 dark:text-slate-400">Outcome</p>
              <p class="inline-flex items-center gap-2 text-base font-medium text-green-600 dark:text-green-400">
                <span class="material-symbols-outlined text-lg">check_circle</span>
                {{ callData.outcome }}
              </p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-sm text-slate-500 dark:text-slate-400">Department</p>
              <p class="text-base font-medium text-slate-900 dark:text-white">{{ callData.department }}</p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-sm text-slate-500 dark:text-slate-400">Assigned Agent</p>
              <p class="text-base font-medium text-slate-900 dark:text-white">{{ callData.assignedAgent }}</p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-sm text-slate-500 dark:text-slate-400">Date & Time</p>
              <p class="text-base font-medium text-slate-900 dark:text-white">
                {{ callData.date }}, {{ callData.time }}
              </p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-sm text-slate-500 dark:text-slate-400">Transferred To</p>
              <p class="text-base font-medium text-slate-900 dark:text-white">{{ callData.transferredTo }}</p>
            </div>
          </div>
        </section>

        <!-- AI Analysis Section -->
        <section v-if="callData.summary_json" class="mt-8">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-slate-900 dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em]">
              AI Analysis
            </h2>
            <button
              v-if="!isGeneratingSummary"
              @click="handleRegenerateSummary"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary border border-primary rounded-lg hover:bg-primary/5"
            >
              <span class="material-symbols-outlined text-lg">refresh</span>
              <span>Regenerate</span>
            </button>
            <div v-else class="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
              <span class="material-symbols-outlined animate-spin">refresh</span>
              Generating...
            </div>
          </div>

          <div class="p-6 bg-gradient-to-br from-primary/5 to-primary/10 dark:from-primary/10 dark:to-primary/20 border border-primary/20 rounded-xl">
            <!-- Main Summary -->
            <div class="mb-6">
              <div class="flex items-center gap-2 mb-2">
                <span class="material-symbols-outlined text-primary">auto_awesome</span>
                <h3 class="text-base font-bold text-slate-900 dark:text-white">Summary</h3>
              </div>
              <p class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                {{ callData.summary_json.summary }}
              </p>
            </div>

            <!-- Sentiment Badge -->
            <div v-if="callData.summary_json.sentiment" class="mb-6">
              <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full"
                :class="getSentimentClass(callData.summary_json.sentiment)"
              >
                <span class="material-symbols-outlined text-base">
                  {{ getSentimentIcon(callData.summary_json.sentiment) }}
                </span>
                <span class="text-sm font-medium capitalize">
                  {{ callData.summary_json.sentiment }} Sentiment
                </span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Key Points -->
              <div v-if="callData.summary_json.key_points && callData.summary_json.key_points.length > 0">
                <div class="flex items-center gap-2 mb-3">
                  <span class="material-symbols-outlined text-primary text-lg">checklist</span>
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white">Key Points</h3>
                </div>
                <ul class="space-y-2">
                  <li
                    v-for="(point, index) in callData.summary_json.key_points"
                    :key="index"
                    class="flex items-start gap-2 text-sm text-slate-700 dark:text-slate-300"
                  >
                    <span class="material-symbols-outlined text-primary text-base mt-0.5">check_circle</span>
                    <span>{{ point }}</span>
                  </li>
                </ul>
              </div>

              <!-- Topics -->
              <div v-if="callData.summary_json.topics && callData.summary_json.topics.length > 0">
                <div class="flex items-center gap-2 mb-3">
                  <span class="material-symbols-outlined text-primary text-lg">label</span>
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white">Topics</h3>
                </div>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="(topic, index) in callData.summary_json.topics"
                    :key="index"
                    class="inline-flex items-center px-3 py-1 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-full text-xs font-medium text-slate-700 dark:text-slate-300"
                  >
                    {{ topic }}
                  </span>
                </div>
              </div>

              <!-- Action Items -->
              <div v-if="callData.summary_json.action_items && callData.summary_json.action_items.length > 0">
                <div class="flex items-center gap-2 mb-3">
                  <span class="material-symbols-outlined text-primary text-lg">task_alt</span>
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white">Action Items</h3>
                </div>
                <ul class="space-y-2">
                  <li
                    v-for="(item, index) in callData.summary_json.action_items"
                    :key="index"
                    class="flex items-start gap-2 text-sm text-slate-700 dark:text-slate-300"
                  >
                    <span class="material-symbols-outlined text-amber-600 dark:text-amber-400 text-base mt-0.5">arrow_right</span>
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </div>

              <!-- Duration Analysis -->
              <div v-if="callData.summary_json.duration_analysis">
                <div class="flex items-center gap-2 mb-3">
                  <span class="material-symbols-outlined text-primary text-lg">timer</span>
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white">Duration Analysis</h3>
                </div>
                <p class="text-sm text-slate-700 dark:text-slate-300">
                  {{ callData.summary_json.duration_analysis }}
                </p>
              </div>
            </div>
          </div>
        </section>

        <!-- No Summary Available -->
        <section v-else-if="callData.transcript_json && callData.transcript_json.length >= 2" class="mt-8">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-slate-900 dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em]">
              AI Analysis
            </h2>
          </div>

          <div class="p-8 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-xl text-center">
            <div class="flex items-center justify-center size-14 bg-primary/10 rounded-full text-primary mx-auto mb-4">
              <span class="material-symbols-outlined text-3xl">auto_awesome</span>
            </div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-2">No AI Summary Available</h3>
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-4">
              Generate an AI-powered summary to get insights, key points, and action items.
            </p>
            <button
              @click="handleRegenerateSummary"
              :disabled="isGeneratingSummary"
              class="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span class="material-symbols-outlined" :class="isGeneratingSummary ? 'animate-spin' : ''">
                {{ isGeneratingSummary ? 'refresh' : 'auto_awesome' }}
              </span>
              <span>{{ isGeneratingSummary ? 'Generating...' : 'Generate AI Summary' }}</span>
            </button>
          </div>
        </section>

        <!-- Tab Navigation & Content -->
        <div class="mt-8">
          <div class="border-b border-slate-200 dark:border-slate-800">
            <nav aria-label="Tabs" class="-mb-px flex space-x-6">
              <button
                @click="activeTab = 'transcript'"
                class="whitespace-nowrap py-3 px-1 border-b-2 font-semibold text-sm"
                :class="activeTab === 'transcript'
                  ? 'text-primary border-primary'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white border-transparent'"
              >
                Transcript
              </button>

              <button
                @click="activeTab = 'timeline'"
                class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm"
                :class="activeTab === 'timeline'
                  ? 'text-primary border-primary'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white border-transparent'"
              >
                Timeline
              </button>
            </nav>
          </div>

          <!-- Transcript Content -->
          <div v-if="activeTab === 'transcript'" class="mt-6">
            <!-- Empty state when no transcript -->
            <div v-if="transcript.length === 0" class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-10 flex flex-col items-center justify-center text-center">
              <div class="flex items-center justify-center size-14 bg-slate-100 dark:bg-slate-800 rounded-full text-slate-400">
                <span class="material-symbols-outlined text-3xl">chat_bubble_outline</span>
              </div>
              <h3 class="mt-4 text-lg font-bold text-slate-900 dark:text-white">No Transcript Available</h3>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
                The conversation transcript will appear here after the call ends.
              </p>
            </div>

            <!-- Transcript messages -->
            <div v-else class="space-y-6">
            <div v-for="message in transcript" :key="message.id" class="flex gap-4" :class="message.speaker === 'agent' ? 'flex-row-reverse' : ''">
              <!-- Avatar -->
              <div
                class="flex-shrink-0 size-8 rounded-full flex items-center justify-center"
                :class="message.speaker === 'agent'
                  ? 'bg-primary text-white'
                  : 'bg-primary/10 text-primary'"
              >
                <span class="material-symbols-outlined text-lg">
                  {{ message.speaker === 'agent' ? 'headset_mic' : 'person' }}
                </span>
              </div>

              <!-- Message Bubble -->
              <div :class="message.speaker === 'agent' ? 'flex-1 text-right' : 'flex-1'">
                <div
                  class="rounded-lg p-4"
                  :class="message.speaker === 'agent'
                    ? 'inline-block text-left bg-primary/10'
                    : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800'"
                >
                  <div class="flex justify-between items-center mb-1">
                    <p
                      class="font-bold text-sm"
                      :class="message.speaker === 'agent' ? 'text-primary' : 'text-slate-900 dark:text-white'"
                    >
                      {{ message.speaker === 'agent' ? 'Agent' : 'Customer' }}
                    </p>
                    <p class="text-xs text-slate-500 dark:text-slate-400">{{ message.timestamp }}</p>
                  </div>
                  <p class="text-sm text-slate-900 dark:text-white">
                    {{ message.text }}
                    <span
                      v-if="message.sentiment"
                      class="material-symbols-outlined text-base align-text-bottom"
                      :class="message.sentiment === 'positive' ? 'text-green-600' : 'text-red-600'"
                      :title="message.sentiment === 'positive' ? 'Positive Sentiment' : 'Negative Sentiment'"
                    >
                      {{ message.sentiment === 'positive' ? 'sentiment_satisfied' : 'sentiment_dissatisfied' }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
            </div><!-- End v-else for transcript messages -->
          </div>



          <!-- Timeline Content -->
          <div v-if="activeTab === 'timeline'" class="mt-6">
            <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-10 flex flex-col items-center justify-center text-center">
              <div class="flex items-center justify-center size-14 bg-primary/10 rounded-full text-primary">
                <span class="material-symbols-outlined text-3xl">timeline</span>
              </div>
              <h3 class="mt-4 text-lg font-bold text-slate-900 dark:text-white">Call Timeline</h3>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
                Visual timeline of call events will be displayed here.
              </p>
            </div>
          </div>
        </div>
        </div><!-- End v-else -->
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'
import { getCallById } from '@/services/api'
import apiClient from '@/services/api'

const route = useRoute()
const callId = ref(route.params.id)
const activeTab = ref('transcript')
const isLoading = ref(true)
const error = ref(null)
const isGeneratingSummary = ref(false)

// Call data from API
const callData = ref({
  caller: 'N/A',
  date: 'N/A',
  time: 'N/A',
  duration: '0s',
  outcome: 'Unknown',
  department: 'N/A',
  assignedAgent: 'N/A',
  transferredTo: 'N/A',
  status: 'unknown',
  agent_name: 'N/A',
  start_time: null,
  end_time: null,
  duration_seconds: 0,
  transcript: '',
  transcript_json: null,
  summary: null,
  summary_json: null
})

// Transcript messages parsed from API
const transcript = ref([])

// Format duration in seconds to readable format
const formatDuration = (seconds) => {
  if (!seconds) return '0s'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  if (mins > 0) {
    return `${mins}m ${secs}s`
  }
  return `${secs}s`
}

// Format date/time
const formatDateTime = (isoString) => {
  if (!isoString) return { date: 'N/A', time: 'N/A' }
  const date = new Date(isoString)
  return {
    date: date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }),
    time: date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  }
}

// Load call data from API
const loadCallData = async () => {
  if (!callId.value) {
    error.value = 'No call ID provided'
    isLoading.value = false
    return
  }

  try {
    isLoading.value = true
    error.value = null

    const data = await getCallById(callId.value)
    console.log('✅ Call data loaded:', data)

    // Parse date/time
    const { date, time } = formatDateTime(data.start_time)

    // Update call data
    callData.value = {
      caller: data.room_name || 'N/A',
      date,
      time,
      duration: formatDuration(data.duration_seconds),
      outcome: data.status === 'completed' ? 'Completed' : 'Ongoing',
      department: data.department || 'Support',
      assignedAgent: data.agent_name || 'N/A',
      transferredTo: 'N/A',
      status: data.status,
      agent_name: data.agent_name,
      start_time: data.start_time,
      end_time: data.end_time,
      duration_seconds: data.duration_seconds,
      transcript: data.transcript,
      transcript_json: data.transcript_json,
      summary: data.summary,
      summary_json: data.summary_json
    }

    // Parse transcript if available
    if (data.transcript_json && Array.isArray(data.transcript_json)) {
      transcript.value = data.transcript_json.map((msg, index) => ({
        id: index + 1,
        speaker: msg.role === 'user' ? 'customer' : 'agent',
        timestamp: msg.timestamp || '00:00',
        text: msg.text || msg.content || '',
        sentiment: msg.sentiment || null
      }))
    } else if (data.transcript) {
      // Fallback: parse plain text transcript
      const lines = data.transcript.split('\n').filter(l => l.trim())
      transcript.value = lines.map((line, index) => {
        const match = line.match(/^(USER|AGENT|ASSISTANT):\s*(.+)$/i)
        if (match) {
          return {
            id: index + 1,
            speaker: match[1].toLowerCase() === 'user' ? 'customer' : 'agent',
            timestamp: '00:00',
            text: match[2],
            sentiment: null
          }
        }
        return {
          id: index + 1,
          speaker: 'unknown',
          timestamp: '00:00',
          text: line,
          sentiment: null
        }
      })
    }

  } catch (err) {
    console.error('❌ Failed to load call data:', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to load call data'
  } finally {
    isLoading.value = false
  }
}

// Methods


const handleViewTranscript = () => {
  activeTab.value = 'transcript'
  // Scroll to transcript section if needed
  const transcriptSection = document.querySelector('.mt-8')
  if (transcriptSection) {
    transcriptSection.scrollIntoView({ behavior: 'smooth' })
  }
}

const handleShareCall = () => {
  // Copy call URL to clipboard
  const url = `${window.location.origin}/call-logs/${callId.value}`
  navigator.clipboard.writeText(url).then(() => {
    alert('Call link copied to clipboard!\n\n' + url)
  }).catch(() => {
    alert('Share Call\n\nURL: ' + url)
  })
}

// AI Summary Functions
const getSentimentIcon = (sentiment) => {
  const icons = {
    positive: 'sentiment_satisfied',
    negative: 'sentiment_dissatisfied',
    neutral: 'sentiment_neutral'
  }
  return icons[sentiment] || 'sentiment_neutral'
}

const getSentimentClass = (sentiment) => {
  const classes = {
    positive: 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300',
    negative: 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300',
    neutral: 'bg-slate-100 text-slate-800 dark:bg-slate-900/50 dark:text-slate-300'
  }
  return classes[sentiment] || classes.neutral
}

const handleRegenerateSummary = async () => {
  if (!callId.value) {
    alert('No call ID available')
    return
  }

  if (!callData.value.transcript_json || callData.value.transcript_json.length < 2) {
    alert('Cannot generate summary: Transcript must have at least 2 messages')
    return
  }

  try {
    isGeneratingSummary.value = true

    const response = await apiClient.post(`/api/calls/${callId.value}/generate-summary`)

    if (response.data.success) {
      // Update call data with new summary
      callData.value.summary = response.data.summary.summary
      callData.value.summary_json = response.data.summary

      console.log('✅ AI Summary generated successfully')
    } else {
      throw new Error('Summary generation failed')
    }

  } catch (err) {
    console.error('❌ Failed to generate summary:', err)
    alert(`Failed to generate AI summary\n\n${err.response?.data?.detail || err.message}`)
  } finally {
    isGeneratingSummary.value = false
  }
}

onMounted(() => {
  loadCallData()
})
</script>
