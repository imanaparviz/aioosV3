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
              Event Details
            </h2>
            <button
              @click="handleClose"
              class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <span class="material-symbols-outlined text-xl">close</span>
            </button>
          </div>

          <!-- Content -->
          <div class="p-6 space-y-4">
            <!-- Title -->
            <div>
              <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Title
              </label>
              <p class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ event.title }}
              </p>
            </div>

            <!-- Date & Time -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  <span class="material-symbols-outlined text-base align-middle mr-1">calendar_today</span>
                  Date
                </label>
                <p class="text-base font-medium text-gray-900 dark:text-white">
                  {{ formatDate(event.event_date) }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  <span class="material-symbols-outlined text-base align-middle mr-1">schedule</span>
                  Time
                </label>
                <p class="text-base font-medium text-gray-900 dark:text-white">
                  {{ event.event_time || 'Not specified' }}
                </p>
              </div>
            </div>

            <!-- Duration -->
            <div v-if="event.duration_minutes">
              <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                <span class="material-symbols-outlined text-base align-middle mr-1">timelapse</span>
                Duration
              </label>
              <p class="text-base font-medium text-gray-900 dark:text-white">
                {{ event.duration_minutes }} minutes
              </p>
            </div>

            <!-- Status -->
            <div>
              <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Status
              </label>
              <span
                class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-semibold"
                :class="getStatusClass(event.status)"
              >
                <span class="material-symbols-outlined text-base">{{ getStatusIcon(event.status) }}</span>
                {{ event.status.charAt(0).toUpperCase() + event.status.slice(1) }}
              </span>
            </div>

            <!-- Description -->
            <div v-if="event.description">
              <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Description
              </label>
              <p class="text-base text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
                {{ event.description }}
              </p>
            </div>

            <!-- Created by Agent Badge -->
            <div v-if="event.created_by_agent" class="flex items-center gap-2 text-sm text-primary">
              <span class="material-symbols-outlined text-base">smart_toy</span>
              <span class="font-medium">Created by AI Agent</span>
            </div>
          </div>

          <!-- Footer -->
          <div class="flex items-center justify-end gap-3 p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
            <button
              @click="handleClose"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              Close
            </button>
            <button
              v-if="event.status !== 'cancelled'"
              @click="handleEdit"
              class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-primary/90 transition-colors"
            >
              Edit Event
            </button>
            <button
              @click="handleDelete"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  event: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'edit', 'delete'])

const handleClose = () => {
  emit('close')
}

const handleEdit = () => {
  emit('edit', props.event)
}

const handleDelete = () => {
  if (confirm('Are you sure you want to delete this event?')) {
    emit('delete', props.event)
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00')
  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getStatusClass = (status) => {
  const classes = {
    confirmed: 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400',
    pending: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400',
    cancelled: 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400',
    completed: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
  }
  return classes[status] || 'bg-gray-100 dark:bg-gray-900/30 text-gray-600 dark:text-gray-400'
}

const getStatusIcon = (status) => {
  const icons = {
    confirmed: 'check_circle',
    pending: 'schedule',
    cancelled: 'cancel',
    completed: 'task_alt'
  }
  return icons[status] || 'info'
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
