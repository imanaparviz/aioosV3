<template>
  <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">
        Scheduling Rules & Availability
      </h2>
      <button
        @click="handleSave"
        :disabled="saving"
        class="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 disabled:opacity-50"
      >
        <span v-if="saving" class="material-symbols-outlined text-lg animate-spin">sync</span>
        <span v-else class="material-symbols-outlined text-lg">save</span>
        <span class="truncate">{{ saving ? 'Saving...' : 'Save Changes' }}</span>
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg">
      <p class="text-sm text-red-800 dark:text-red-300">{{ errorMessage }}</p>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="mb-4 p-3 bg-green-100 dark:bg-green-900/30 border border-green-300 dark:border-green-700 rounded-lg">
      <p class="text-sm text-green-800 dark:text-green-300">{{ successMessage }}</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Working Hours -->
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Working Hours
        </h3>
        <div class="space-y-4">
          <div v-for="day in daysOfWeek" :key="day.key" class="flex items-start gap-4">
            <!-- Day Checkbox -->
            <div class="w-28 pt-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  v-model="workingDays[day.key]"
                  type="checkbox"
                  class="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary cursor-pointer"
                />
                <span
                  class="text-sm font-medium"
                  :class="workingDays[day.key] ? 'text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400'"
                >
                  {{ day.label }}
                </span>
              </label>
            </div>

            <!-- Time Inputs -->
            <div v-if="workingDays[day.key]" class="flex-1">
              <div
                v-for="(block, index) in workingHours[day.key] || []"
                :key="index"
                class="flex items-center gap-2 mb-2"
              >
                <input
                  v-model="block.start"
                  type="time"
                  class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary focus:ring-primary sm:text-sm bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
                <span class="text-gray-500 dark:text-gray-400">-</span>
                <input
                  v-model="block.end"
                  type="time"
                  class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary focus:ring-primary sm:text-sm bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
                <button
                  @click="removeWorkingBlock(day.key, index)"
                  class="p-2 text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400"
                >
                  <span class="material-symbols-outlined">delete</span>
                </button>
              </div>
              <button
                v-if="(workingHours[day.key] || []).length === 0"
                @click="addWorkingBlock(day.key)"
                class="text-sm text-primary hover:underline"
              >
                Add time block
              </button>
            </div>
            <div v-else class="flex-1">
              <p class="pt-2 text-sm text-gray-500 dark:text-gray-400">Unavailable</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Break Times & Duration -->
      <div>
        <!-- Break Times -->
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Break Times
        </h3>
        <div class="space-y-4 bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
          <div v-for="(breakTime, index) in breakTimes" :key="index" class="space-y-2">
            <div class="flex items-center justify-between">
              <input
                v-model="breakTime.name"
                type="text"
                placeholder="Break name (e.g., Lunch Break)"
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary focus:ring-primary sm:text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
            <div class="flex items-center gap-2">
              <input
                v-model="breakTime.start"
                type="time"
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary focus:ring-primary sm:text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <span class="text-gray-500 dark:text-gray-400">-</span>
              <input
                v-model="breakTime.end"
                type="time"
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary focus:ring-primary sm:text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <button
                @click="removeBreak(index)"
                class="p-2 text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400"
              >
                <span class="material-symbols-outlined">delete</span>
              </button>
            </div>
            <div class="flex flex-wrap gap-2">
              <label
                v-for="day in daysOfWeek"
                :key="day.key"
                class="flex items-center gap-1 cursor-pointer"
              >
                <input
                  v-model="breakTime.days"
                  :value="day.key"
                  type="checkbox"
                  class="h-3 w-3 rounded border-gray-300 text-primary focus:ring-primary cursor-pointer"
                />
                <span class="text-xs text-gray-600 dark:text-gray-400">{{ day.short }}</span>
              </label>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              Applied to: {{ formatBreakDays(breakTime.days) }}
            </p>
          </div>
        </div>
        <button
          @click="addBreak"
          class="mt-4 flex items-center gap-2 text-sm font-medium text-primary hover:underline"
        >
          <span class="material-symbols-outlined text-lg">add_circle</span>
          <span>Add break block</span>
        </button>

        <!-- Default Appointment Duration -->
        <div class="mt-8">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Default Appointment Duration
          </h3>
          <div class="relative w-full max-w-xs">
            <select
              v-model="defaultDuration"
              class="appearance-none block w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md py-2 pl-3 pr-10 text-sm focus:outline-none focus:ring-primary focus:border-primary text-gray-900 dark:text-white"
            >
              <option :value="30">30 minutes</option>
              <option :value="45">45 minutes</option>
              <option :value="60">1 hour</option>
              <option :value="90">1.5 hours</option>
              <option :value="120">2 hours</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500 dark:text-gray-400">
              <span class="material-symbols-outlined">expand_more</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, defineProps } from 'vue'
import axios from 'axios'

const props = defineProps({
  agentId: {
    type: String,
    required: true
  }
})

// Days of week
const daysOfWeek = [
  { key: 'monday', label: 'Monday', short: 'Mon' },
  { key: 'tuesday', label: 'Tuesday', short: 'Tue' },
  { key: 'wednesday', label: 'Wednesday', short: 'Wed' },
  { key: 'thursday', label: 'Thursday', short: 'Thu' },
  { key: 'friday', label: 'Friday', short: 'Fri' },
  { key: 'saturday', label: 'Saturday', short: 'Sat' },
  { key: 'sunday', label: 'Sunday', short: 'Sun' }
]

// State
const workingDays = reactive({
  monday: true,
  tuesday: true,
  wednesday: true,
  thursday: true,
  friday: true,
  saturday: false,
  sunday: false
})

const workingHours = reactive({
  monday: [{ start: '09:00', end: '17:00' }],
  tuesday: [{ start: '09:00', end: '17:00' }],
  wednesday: [{ start: '09:00', end: '17:00' }],
  thursday: [{ start: '09:00', end: '17:00' }],
  friday: [{ start: '09:00', end: '17:00' }],
  saturday: [],
  sunday: []
})

const breakTimes = ref([
  {
    name: 'Lunch Break',
    start: '12:30',
    end: '13:30',
    days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
  }
])

const defaultDuration = ref(45)
const saving = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Methods
const addWorkingBlock = (day) => {
  if (!workingHours[day]) {
    workingHours[day] = []
  }
  workingHours[day].push({ start: '09:00', end: '17:00' })
}

const removeWorkingBlock = (day, index) => {
  workingHours[day].splice(index, 1)
}

const addBreak = () => {
  breakTimes.value.push({
    name: '',
    start: '12:00',
    end: '13:00',
    days: []
  })
}

const removeBreak = (index) => {
  breakTimes.value.splice(index, 1)
}

const formatBreakDays = (days) => {
  if (!days || days.length === 0) return 'No days selected'
  return days.map(d => {
    const day = daysOfWeek.find(dw => dw.key === d)
    return day ? day.label : d
  }).join(', ')
}

const loadBusinessHours = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/business-hours/${props.agentId}`)
    const config = response.data

    // Update working hours
    if (config.working_hours) {
      Object.keys(config.working_hours).forEach(day => {
        workingDays[day] = true
        workingHours[day] = config.working_hours[day]
      })

      // Mark days without hours as not working
      daysOfWeek.forEach(day => {
        if (!config.working_hours[day.key] || config.working_hours[day.key].length === 0) {
          workingDays[day.key] = false
        }
      })
    }

    // Update break times
    if (config.break_times && config.break_times.length > 0) {
      breakTimes.value = config.break_times
    }

    // Update default duration
    if (config.default_appointment_duration) {
      defaultDuration.value = config.default_appointment_duration
    }

    console.log('✅ Business hours loaded')
  } catch (error) {
    console.error('Failed to load business hours:', error)
    // Use default values on error
  }
}

const handleSave = async () => {
  saving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // Build working hours object (only include enabled days)
    const hours = {}
    Object.keys(workingDays).forEach(day => {
      if (workingDays[day] && workingHours[day] && workingHours[day].length > 0) {
        hours[day] = workingHours[day]
      }
    })

    const payload = {
      working_hours: hours,
      break_times: breakTimes.value.filter(b => b.name && b.start && b.end),
      default_appointment_duration: defaultDuration.value
    }

    await axios.post(`http://localhost:8000/api/business-hours/${props.agentId}`, payload)

    successMessage.value = '✅ Business hours saved successfully!'
    console.log('✅ Business hours saved')

    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error) {
    console.error('Failed to save business hours:', error)
    errorMessage.value = error.response?.data?.detail || 'Failed to save business hours. Please try again.'
  } finally {
    saving.value = false
  }
}

// Load on mount
onMounted(() => {
  loadBusinessHours()
})
</script>

<style scoped>
/* Custom styles if needed */
</style>
