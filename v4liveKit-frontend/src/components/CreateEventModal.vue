<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="show"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
        @click.self="handleClose"
      >
        <div
          class="relative w-full max-w-lg bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden"
          @click.stop
        >
          <!-- Header -->
          <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">
              Create New Event
            </h2>
            <button
              @click="handleClose"
              class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <span class="material-symbols-outlined text-xl">close</span>
            </button>
          </div>

          <!-- Form -->
          <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
            <!-- Title -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Event Title *
              </label>
              <input
                v-model="form.title"
                type="text"
                required
                placeholder="Team Meeting, Client Call, etc."
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>

            <!-- Date & Time -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Date *
                </label>
                <input
                  v-model="form.event_date"
                  type="date"
                  required
                  class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Time *
                </label>
                <input
                  v-model="form.event_time"
                  type="time"
                  required
                  class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
            </div>

            <!-- Duration -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Duration (minutes)
              </label>
              <select
                v-model="form.duration_minutes"
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option :value="15">15 minutes</option>
                <option :value="30">30 minutes</option>
                <option :value="60" selected>1 hour</option>
                <option :value="90">1.5 hours</option>
                <option :value="120">2 hours</option>
              </select>
            </div>

            <!-- Status -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Status
              </label>
              <select
                v-model="form.status"
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="confirmed">Confirmed</option>
                <option value="pending">Pending</option>
              </select>
            </div>

            <!-- Description -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Description (Optional)
              </label>
              <textarea
                v-model="form.description"
                rows="3"
                placeholder="Add event details, notes, or agenda..."
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
              ></textarea>
            </div>

            <!-- Error Message -->
            <div v-if="errorMessage" class="p-3 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg">
              <p class="text-sm text-red-800 dark:text-red-300">
                {{ errorMessage }}
              </p>
            </div>
          </form>

          <!-- Footer -->
          <div class="flex items-center justify-end gap-3 p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
            <button
              @click="handleClose"
              type="button"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              @click="handleSubmit"
              :disabled="loading"
              type="submit"
              class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading" class="material-symbols-outlined text-base animate-spin">sync</span>
              <span v-else>Create Event</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue'
import { createCalendarEvent } from '@/services/api'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'created'])

// Form state
const form = ref({
  title: '',
  event_date: new Date().toISOString().split('T')[0],
  event_time: '09:00',
  duration_minutes: 60,
  status: 'confirmed',
  description: '',
  user_id: 'dev-user-123', // TODO: Get from auth
  agent_id: null
})

const loading = ref(false)
const errorMessage = ref('')

// Reset form when modal opens
watch(() => props.show, (newVal) => {
  if (newVal) {
    form.value = {
      title: '',
      event_date: new Date().toISOString().split('T')[0],
      event_time: '09:00',
      duration_minutes: 60,
      status: 'confirmed',
      description: '',
      user_id: 'dev-user-123',
      agent_id: null
    }
    errorMessage.value = ''
  }
})

const handleClose = () => {
  emit('close')
}

const handleSubmit = async () => {
  if (!form.value.title || !form.value.event_date || !form.value.event_time) {
    errorMessage.value = 'Please fill in all required fields'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    // Call API to create event
    await createCalendarEvent(form.value)

    // Emit success to parent
    emit('created', form.value)
  } catch (err) {
    console.error('Failed to create event:', err)
    errorMessage.value = err.response?.data?.detail || 'Failed to create event. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.2s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
}
</style>
