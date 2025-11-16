<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Event Details Modal -->
    <EventDetailsModal
      :show="showEventModal"
      :event="selectedEvent"
      @close="showEventModal = false"
      @edit="handleEditEvent"
      @delete="handleDeleteEvent"
    />

    <!-- Create Event Modal -->
    <CreateEventModal
      :show="showCreateModal"
      @close="showCreateModal = false"
      @created="handleCreateSubmit"
    />

    <!-- Main Content -->
    <main class="flex-1 p-6 lg:p-10 overflow-y-auto">
      <div class="flex flex-col h-full">
        <!-- Header -->
        <header class="flex flex-wrap items-center justify-between gap-4 mb-6">
          <h1 class="text-slate-900 dark:text-white text-3xl lg:text-4xl font-black leading-tight tracking-[-0.033em]">
            Agent Calendar
          </h1>
          <button
            @click="handleCreateEvent"
            class="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90"
          >
            <span class="material-symbols-outlined text-lg">add</span>
            <span class="truncate">Create Event</span>
          </button>
        </header>

        <!-- Controls -->
        <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
          <!-- Agent Selector & Month Navigation -->
          <div class="flex items-center gap-4">
            <!-- Agent Selector -->
            <div class="relative">
              <select
                v-model="selectedAgentId"
                @change="onAgentChange"
                class="appearance-none h-10 px-4 pr-10 border border-gray-300 dark:border-gray-700 rounded-lg text-sm font-medium text-gray-900 dark:text-white bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option :value="null">All Events</option>
                <option v-for="agent in availableAgents" :key="agent.id" :value="agent.id">
                  {{ agent.name }}
                </option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500 dark:text-gray-400">
                <span class="material-symbols-outlined text-lg">expand_more</span>
              </div>
            </div>
            <div class="flex items-center border border-slate-300 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800">
              <button
                @click="previousMonth"
                class="p-2 text-slate-500 dark:text-slate-400 hover:text-primary dark:hover:text-primary"
              >
                <span class="material-symbols-outlined">chevron_left</span>
              </button>
              <h2 class="px-2 text-base font-semibold text-slate-900 dark:text-white whitespace-nowrap">
                {{ currentMonthYear }}
              </h2>
              <button
                @click="nextMonth"
                class="p-2 text-slate-500 dark:text-slate-400 hover:text-primary dark:hover:text-primary"
              >
                <span class="material-symbols-outlined">chevron_right</span>
              </button>
            </div>
            <button
              @click="goToToday"
              class="h-10 px-4 border border-slate-300 dark:border-slate-700 rounded-lg text-sm font-medium text-slate-900 dark:text-white bg-white dark:bg-slate-800 hover:bg-primary/10"
            >
              Today
            </button>
          </div>

          <!-- View Switcher -->
          <div class="flex items-center gap-2 p-1 rounded-lg bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700">
            <button
              @click="currentView = 'month'"
              class="px-3 py-1 text-sm font-medium rounded-md"
              :class="currentView === 'month'
                ? 'bg-white dark:bg-slate-700 text-primary'
                : 'text-slate-500 dark:text-slate-400 hover:bg-white dark:hover:bg-slate-700'"
            >
              Month
            </button>
            <button
              @click="currentView = 'week'"
              class="px-3 py-1 text-sm font-medium rounded-md"
              :class="currentView === 'week'
                ? 'bg-white dark:bg-slate-700 text-primary'
                : 'text-slate-500 dark:text-slate-400 hover:bg-white dark:hover:bg-slate-700'"
            >
              Week
            </button>
            <button
              @click="currentView = 'day'"
              class="px-3 py-1 text-sm font-medium rounded-md"
              :class="currentView === 'day'
                ? 'bg-white dark:bg-slate-700 text-primary'
                : 'text-slate-500 dark:text-slate-400 hover:bg-white dark:hover:bg-slate-700'"
            >
              Day
            </button>
          </div>
        </div>

        <!-- Calendar Grid -->
        <div class="flex-1 grid grid-cols-7 auto-rows-fr gap-px border-l border-t border-slate-300 dark:border-slate-700 bg-slate-300 dark:bg-slate-700 rounded-xl overflow-hidden">
          <!-- Day Headers -->
          <div
            v-for="day in daysOfWeek"
            :key="day"
            class="text-center py-2 text-sm font-semibold text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-900 border-r border-b border-slate-300 dark:border-slate-700"
          >
            {{ day }}
          </div>

          <!-- Calendar Days -->
          <div
            v-for="day in calendarDays"
            :key="day.date"
            class="relative p-2 text-sm font-medium bg-white dark:bg-slate-900 border-r border-b border-slate-300 dark:border-slate-700 min-h-[100px]"
            :class="{
              'bg-slate-50 dark:bg-slate-950 text-slate-400': !day.isCurrentMonth,
              'bg-primary/10': day.isToday
            }"
          >
            <!-- Day Number -->
            <span
              v-if="day.isToday"
              class="absolute top-1.5 right-1.5 size-7 flex items-center justify-center bg-primary text-white rounded-full text-xs font-bold"
            >
              {{ day.day }}
            </span>
            <span v-else class="text-slate-900 dark:text-white">
              {{ day.day }}
            </span>

            <!-- Events -->
            <div v-if="day.events.length > 0" class="mt-1 space-y-1">
              <div
                v-for="event in day.events"
                :key="event.id"
                @click="handleEventClick(event)"
                class="px-2 py-1 rounded-md text-xs font-semibold truncate cursor-pointer"
                :class="getEventClass(event.type)"
              >
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>

        <!-- Business Hours Configuration -->
        <div class="mt-10">
          <div v-if="selectedAgentId">
            <BusinessHoursConfig :agent-id="selectedAgentId" />
          </div>
          <div v-else class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 text-center">
            <span class="material-symbols-outlined text-4xl text-gray-400 dark:text-gray-600">event_available</span>
            <h3 class="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
              Select an Agent
            </h3>
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Choose an agent from the dropdown above to configure their scheduling rules and availability.
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'
import EventDetailsModal from '@/components/EventDetailsModal.vue'
import CreateEventModal from '@/components/CreateEventModal.vue'
import BusinessHoursConfig from '@/components/BusinessHoursConfig.vue'
import { getCalendarEvents, createCalendarEvent } from '@/services/api'
import axios from 'axios'

// Route
const route = useRoute()

// State
const currentDate = ref(new Date())
const currentView = ref('month')
const events = ref([])
const loading = ref(false)
const error = ref(null)
const showEventModal = ref(false)
const showCreateModal = ref(false)
const availableAgents = ref([])
const selectedAgentId = ref(route.query.agent_id || null)
const selectedEvent = ref({
  title: '',
  event_date: '',
  event_time: '',
  duration_minutes: 0,
  status: '',
  description: ''
})

// Days of week
const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

// Computed
const currentMonthYear = computed(() => {
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  return `${months[currentDate.value.getMonth()]} ${currentDate.value.getFullYear()}`
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const today = new Date()

  // First day of month
  const firstDay = new Date(year, month, 1)
  const firstDayOfWeek = firstDay.getDay()

  // Last day of month
  const lastDay = new Date(year, month + 1, 0)
  const daysInMonth = lastDay.getDate()

  // Previous month days to fill
  const prevMonth = new Date(year, month, 0)
  const daysInPrevMonth = prevMonth.getDate()

  const days = []

  // Previous month days
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const day = daysInPrevMonth - i
    const date = new Date(year, month - 1, day)
    days.push({
      day,
      date: formatDate(date),
      isCurrentMonth: false,
      isToday: false,
      events: getEventsForDate(formatDate(date))
    })
  }

  // Current month days
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month, day)
    const isToday = date.toDateString() === today.toDateString()
    days.push({
      day,
      date: formatDate(date),
      isCurrentMonth: true,
      isToday,
      events: getEventsForDate(formatDate(date))
    })
  }

  // Next month days to fill (up to 35 or 42 total days)
  const remainingDays = 35 - days.length
  for (let day = 1; day <= remainingDays; day++) {
    const date = new Date(year, month + 1, day)
    days.push({
      day,
      date: formatDate(date),
      isCurrentMonth: false,
      isToday: false,
      events: getEventsForDate(formatDate(date))
    })
  }

  return days
})

// Methods
const formatDate = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getEventsForDate = (date) => {
  return events.value.filter(event => event.event_date === date)
}

// Load events from Supabase
const loadEvents = async () => {
  loading.value = true
  error.value = null

  try {
    // Get first and last day of current month for filtering
    const year = currentDate.value.getFullYear()
    const month = currentDate.value.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)

    const startDate = formatDate(firstDay)
    const endDate = formatDate(lastDay)

    const data = await getCalendarEvents(startDate, endDate)

    // Transform events to include type based on status
    events.value = data.map(event => ({
      ...event,
      type: event.status === 'confirmed' ? 'primary' :
            event.status === 'pending' ? 'warning' :
            event.status === 'cancelled' ? 'danger' : 'success'
    }))

    console.log(`✅ Loaded ${events.value.length} calendar events`)
  } catch (err) {
    console.error('Failed to load calendar events:', err)
    error.value = 'Failed to load calendar events'
  } finally {
    loading.value = false
  }
}

const getEventClass = (type) => {
  const classes = {
    success: 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400',
    primary: 'bg-primary/10 text-primary',
    danger: 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400',
    warning: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400'
  }
  return classes[type] || 'bg-gray-100 dark:bg-gray-900/30 text-gray-600 dark:text-gray-400'
}

const previousMonth = async () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
  await loadEvents()
}

const nextMonth = async () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
  await loadEvents()
}

const goToToday = async () => {
  currentDate.value = new Date()
  await loadEvents()
}

const handleCreateEvent = () => {
  showCreateModal.value = true
}

const handleCreateSubmit = async () => {
  // Event was already created by modal, just reload and close
  console.log('✅ Event created successfully')

  // Reload events to show the new one
  await loadEvents()

  // Close modal
  showCreateModal.value = false
}

const handleEventClick = (event) => {
  selectedEvent.value = event
  showEventModal.value = true
}

const handleEditEvent = (event) => {
  // TODO: Open edit modal
  console.log('Edit event:', event)
  alert('Edit event functionality coming soon!')
}

const handleDeleteEvent = async (event) => {
  try {
    await axios.delete(`http://localhost:8000/api/calendar/events/${event.id}`)
    console.log('✅ Event deleted:', event.id)

    // Reload events
    await loadEvents()

    // Close modal
    showEventModal.value = false
  } catch (err) {
    console.error('Failed to delete event:', err)
    alert('Failed to delete event. Please try again.')
  }
}

// Load available agents
const loadAgents = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/agents')
    availableAgents.value = response.data
    console.log(`✅ Loaded ${availableAgents.value.length} agents`)

    // If no agent selected and we have agents, select the first one
    if (!selectedAgentId.value && availableAgents.value.length > 0) {
      selectedAgentId.value = availableAgents.value[0].id
    }
  } catch (err) {
    console.error('Failed to load agents:', err)
  }
}

// Handle agent change
const onAgentChange = () => {
  console.log('Agent changed to:', selectedAgentId.value)
  // Reload events when agent changes
  loadEvents()
}

// Load events when component mounts
onMounted(() => {
  loadAgents()
  loadEvents()
})
</script>
