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
              @click="handleListenRecording"
              class="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90"
            >
              <span class="material-symbols-outlined text-lg">play_arrow</span>
              <span class="truncate">Listen to Recording</span>
            </button>
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
                @click="activeTab = 'recording'"
                class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm"
                :class="activeTab === 'recording'
                  ? 'text-primary border-primary'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white border-transparent'"
              >
                Recording
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
          <div v-if="activeTab === 'transcript'" class="mt-6 space-y-6">
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
          </div>

          <!-- Recording Content -->
          <div v-if="activeTab === 'recording'" class="mt-6">
            <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-10 flex flex-col items-center justify-center text-center">
              <div class="flex items-center justify-center size-14 bg-primary/10 rounded-full text-primary">
                <span class="material-symbols-outlined text-3xl">play_circle</span>
              </div>
              <h3 class="mt-4 text-lg font-bold text-slate-900 dark:text-white">Audio Player</h3>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
                Click "Listen to Recording" button to play the audio.
              </p>
            </div>
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
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'

const route = useRoute()
const callId = ref(route.params.id || '78B4C-091A')
const activeTab = ref('transcript')

// Call data
const callData = ref({
  caller: '+1-555-123-4567',
  date: 'Oct 27, 2023',
  time: '10:15 AM',
  duration: '5m 32s',
  outcome: 'Resolved',
  department: 'Technical Support',
  assignedAgent: 'Jane Doe',
  transferredTo: 'N/A'
})

// Transcript messages
const transcript = ref([
  {
    id: 1,
    speaker: 'customer',
    timestamp: '00:12',
    text: "Hello, I'm having an issue with my recent order. It hasn't arrived yet.",
    sentiment: null
  },
  {
    id: 2,
    speaker: 'agent',
    timestamp: '00:18',
    text: "I'm sorry to hear that. Can you please provide me with your order number?",
    sentiment: null
  },
  {
    id: 3,
    speaker: 'customer',
    timestamp: '00:25',
    text: "Sure, it's 123-ABC-456. But I'm getting really frustrated, this is the third time I've called!",
    sentiment: 'negative'
  },
  {
    id: 4,
    speaker: 'agent',
    timestamp: '00:35',
    text: "I understand your frustration. Let me check the status right away... It looks like it was delivered yesterday. I've processed a full refund for you.",
    sentiment: 'positive'
  }
])

// Methods
const handleListenRecording = () => {
  alert('Listen to Recording\n\nThis would open an audio player with the call recording.')
  activeTab.value = 'recording'
}

const handleViewTranscript = () => {
  alert('View Transcript\n\nThis would download the full transcript as a text or PDF file.')
}

const handleShareCall = () => {
  alert('Share Call\n\nThis would open a modal to share the call details via email or generate a shareable link.')
}

onMounted(() => {
  // In real implementation, fetch call data from API based on route.params.id
  console.log('Call ID:', callId.value)
})
</script>
