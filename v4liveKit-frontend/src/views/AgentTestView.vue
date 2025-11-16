<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark">
      <div class="w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Header -->
        <div class="flex flex-col gap-4 mb-8">
          <router-link
            to="/dashboard"
            class="flex items-center gap-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-primary"
          >
            <span class="material-symbols-outlined text-base">arrow_back</span>
            Back to Dashboard
          </router-link>

          <h1 class="text-3xl font-black text-gray-900 dark:text-white">
            Test Agent with Voice Widget
          </h1>
          <p class="text-base text-gray-600 dark:text-gray-400">
            Test your voice agent directly in the browser before connecting it to a phone number.
          </p>
        </div>

        <!-- Test Interface -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <!-- Agent Selection -->
          <div v-if="!selectedAgent" class="flex flex-col gap-4">
            <h2 class="text-lg font-bold text-gray-900 dark:text-white">Select an Agent to Test</h2>

            <div v-if="loading" class="text-center py-8">
              <span class="material-symbols-outlined animate-spin text-4xl text-primary">sync</span>
              <p class="mt-2 text-gray-600 dark:text-gray-400">Loading agents...</p>
            </div>

            <div v-else-if="agents.length === 0" class="text-center py-8">
              <span class="material-symbols-outlined text-5xl text-gray-400">inbox</span>
              <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-gray-300">No agents found</h3>
              <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
                Create an agent first to test it here.
              </p>
              <router-link
                to="/agents/create"
                class="mt-4 inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-bold text-white hover:bg-primary/90"
              >
                <span class="material-symbols-outlined text-base">add</span>
                Create Agent
              </router-link>
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button
                v-for="agent in agents"
                :key="agent.id"
                @click="selectAgent(agent)"
                class="flex items-center gap-4 p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary hover:bg-primary/5 transition-colors text-left"
              >
                <div class="flex-shrink-0 size-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <span class="material-symbols-outlined text-primary">smart_toy</span>
                </div>
                <div class="flex-grow">
                  <p class="font-bold text-gray-900 dark:text-white">{{ agent.name }}</p>
                  <p class="text-sm text-gray-600 dark:text-gray-400">{{ agent.description || 'No description' }}</p>
                  <span
                    :class="{
                      'inline-flex items-center mt-1 rounded-full px-2 py-0.5 text-xs font-semibold': true,
                      'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300': agent.status === 'active',
                      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300': agent.status === 'inactive',
                    }"
                  >
                    {{ agent.status }}
                  </span>
                </div>
              </button>
            </div>
          </div>

          <!-- Voice Widget -->
          <div v-else class="flex flex-col gap-6">
            <!-- Agent Info -->
            <div class="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center gap-3">
                <div class="flex-shrink-0 size-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <span class="material-symbols-outlined text-primary">smart_toy</span>
                </div>
                <div>
                  <p class="font-bold text-gray-900 dark:text-white">{{ selectedAgent.name }}</p>
                  <p class="text-sm text-gray-600 dark:text-gray-400">Testing Mode</p>
                </div>
              </div>
              <button
                @click="resetTest"
                class="flex items-center gap-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-primary"
              >
                <span class="material-symbols-outlined text-base">close</span>
                Change Agent
              </button>
            </div>

            <!-- Voice Chat Interface -->
            <div class="flex flex-col items-center gap-6 py-8">
              <!-- Status Indicator -->
              <div class="text-center">
                <div
                  :class="{
                    'size-32 rounded-full flex items-center justify-center mb-4 mx-auto': true,
                    'bg-gray-200 dark:bg-gray-700': !isConnected && !isConnecting,
                    'bg-yellow-200 dark:bg-yellow-900/50 animate-pulse': isConnecting,
                    'bg-green-200 dark:bg-green-900/50': isConnected,
                  }"
                >
                  <span
                    :class="{
                      'material-symbols-outlined text-6xl': true,
                      'text-gray-500': !isConnected && !isConnecting,
                      'text-yellow-600': isConnecting,
                      'text-green-600 animate-pulse': isConnected,
                    }"
                  >
                    {{ isConnected ? 'mic' : (isConnecting ? 'sync' : 'mic_off') }}
                  </span>
                </div>

                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
                  {{ connectionStatusText }}
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  {{ connectionHintText }}
                </p>
              </div>

              <!-- Control Buttons -->
              <div class="flex gap-4">
                <button
                  v-if="!isConnected && !isConnecting"
                  @click="startTest"
                  :disabled="loading"
                  class="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-base font-bold text-white shadow-sm hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span class="material-symbols-outlined">call</span>
                  Start Voice Test
                </button>

                <button
                  v-if="isConnected"
                  @click="endTest"
                  class="flex items-center gap-2 rounded-lg bg-red-600 px-6 py-3 text-base font-bold text-white shadow-sm hover:bg-red-700 transition-colors"
                >
                  <span class="material-symbols-outlined">call_end</span>
                  End Test
                </button>
              </div>

              <!-- Audio Elements (hidden) -->
              <audio ref="remoteAudio" autoplay></audio>

              <!-- Error Display -->
              <div v-if="error" class="w-full p-4 bg-red-100 dark:bg-red-900/50 border border-red-300 dark:border-red-700 rounded-lg">
                <p class="text-sm text-red-800 dark:text-red-300">
                  <span class="font-bold">Error:</span> {{ error }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Instructions -->
        <div class="mt-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <h3 class="text-sm font-bold text-blue-900 dark:text-blue-300 mb-2">ℹ️ How to Use</h3>
          <ul class="text-sm text-blue-800 dark:text-blue-400 space-y-1 list-disc list-inside">
            <li>Select an agent from the list above</li>
            <li>Click "Start Voice Test" to begin</li>
            <li>Allow microphone access when prompted</li>
            <li>Speak naturally with the agent</li>
            <li>Click "End Test" when done</li>
          </ul>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'
import { getAgents } from '@/services/api'
import { Room, RoomEvent } from 'livekit-client'

const router = useRouter()

// State
const agents = ref([])
const selectedAgent = ref(null)
const loading = ref(false)
const error = ref(null)

// LiveKit
const room = ref(null)
const isConnecting = ref(false)
const isConnected = ref(false)
const remoteAudio = ref(null)

// Computed
const connectionStatusText = computed(() => {
  if (isConnecting.value) return 'Connecting...'
  if (isConnected.value) return 'Connected'
  return 'Ready to Test'
})

const connectionHintText = computed(() => {
  if (isConnecting.value) return 'Setting up voice connection...'
  if (isConnected.value) return 'Speak naturally with the agent'
  return 'Click the button below to start testing'
})

// Load agents
const loadAgents = async () => {
  loading.value = true
  error.value = null

  try {
    const data = await getAgents()
    agents.value = data
  } catch (err) {
    console.error('Failed to load agents:', err)
    error.value = 'Failed to load agents'
  } finally {
    loading.value = false
  }
}

// Select agent
const selectAgent = (agent) => {
  selectedAgent.value = agent
  error.value = null
}

// Reset test
const resetTest = () => {
  if (room.value) {
    room.value.disconnect()
    room.value = null
  }
  selectedAgent.value = null
  isConnected.value = false
  isConnecting.value = false
  error.value = null
}

// Start test
const startTest = async () => {
  if (!selectedAgent.value) return

  isConnecting.value = true
  error.value = null

  try {
    // Call backend to create test session
    const response = await fetch(`http://localhost:8000/api/agents/${selectedAgent.value.id}/test`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_identity: 'test-user'
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to create test session')
    }

    const sessionData = await response.json()
    console.log('Test session created:', sessionData)

    // Connect to LiveKit room
    room.value = new Room()

    // Set up event listeners
    room.value.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
      console.log('🔊 Track subscribed:', track.kind, 'from', participant.identity)

      if (track.kind === 'audio') {
        console.log('🔊 Attaching audio track to element...')
        // Attach remote audio track to audio element
        const element = track.attach(remoteAudio.value)
        console.log('✅ Audio element:', element)
        console.log('✅ Audio element volume:', element.volume)
        console.log('✅ Audio element muted:', element.muted)

        // Make sure it's not muted and volume is up
        element.volume = 1.0
        element.muted = false
        element.play().catch(e => console.error('Failed to play audio:', e))

        console.log('✅ Agent audio attached and should be playing NOW!')
      }
    })

    room.value.on(RoomEvent.ParticipantConnected, (participant) => {
      console.log('👤 Participant connected:', participant.identity)
    })

    room.value.on(RoomEvent.TrackPublished, (publication, participant) => {
      console.log('📢 Track published:', publication.kind, 'by', participant.identity)
    })

    room.value.on(RoomEvent.LocalTrackPublished, (publication) => {
      console.log('✅ Local track published:', publication.kind)
    })

    room.value.on(RoomEvent.Connected, async () => {
      console.log('✅ Connected to room')
      isConnected.value = true
      isConnecting.value = false

      // IMPORTANT: Enable local microphone after connecting
      try {
        console.log('🎤 Requesting microphone access...')

        // Get microphone track manually (workaround for structuredClone bug)
        const audioDevices = await navigator.mediaDevices.enumerateDevices()
        const microphones = audioDevices.filter(d => d.kind === 'audioinput')

        console.log(`Found ${microphones.length} microphones`)

        // Request simple microphone access
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
          },
          video: false
        })

        console.log('✅ Got microphone stream')

        // Publish the audio track to room
        const audioTrack = stream.getAudioTracks()[0]
        await room.value.localParticipant.publishTrack(audioTrack, {
          name: 'microphone',
          source: 'microphone'
        })

        console.log('✅ Microphone track published!')
      } catch (micError) {
        console.error('❌ Failed to enable microphone:', micError)
        error.value = `Microphone error: ${micError.message}. Please grant microphone permission in your browser.`

        // Disconnect if mic fails
        room.value.disconnect()
      }
    })

    room.value.on(RoomEvent.Disconnected, (reason) => {
      console.log('Disconnected from room. Reason:', reason)
      isConnected.value = false
      isConnecting.value = false
    })

    room.value.on(RoomEvent.MediaDevicesError, (error) => {
      console.error('❌ Media device error:', error)
      error.value = `Media device error: ${error.message}`
    })

    // Connect to room WITHOUT auto-publishing (we'll do it manually)
    console.log('🔌 Connecting to LiveKit room...')
    await room.value.connect(sessionData.livekit_url, sessionData.token, {
      audio: false,  // Don't auto-publish audio - we'll do it manually
      video: false,
    })

    console.log('✅ Room connected successfully!')

    // Small delay to ensure connection is stable
    await new Promise(resolve => setTimeout(resolve, 500))

  } catch (err) {
    console.error('Failed to start test:', err)
    error.value = err.message || 'Failed to start test'
    isConnecting.value = false
    isConnected.value = false
  }
}

// End test
const endTest = () => {
  if (room.value) {
    room.value.disconnect()
    room.value = null
  }
  isConnected.value = false
  isConnecting.value = false
}

// Load agents on mount
loadAgents()

// Cleanup on unmount
onUnmounted(() => {
  if (room.value) {
    room.value.disconnect()
  }
})
</script>
