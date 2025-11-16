<template>
  <div
    class="group flex cursor-pointer flex-col gap-4 rounded-xl border border-border-light dark:border-border-dark bg-card-light dark:bg-card-dark p-6 transition-all duration-200 hover:-translate-y-1 hover:shadow-lg hover:border-primary"
    @click="$emit('select', template)"
  >
    <!-- Icon -->
    <div
      class="flex h-12 w-12 items-center justify-center rounded-lg"
      :class="iconBgClass"
    >
      <span
        class="material-symbols-outlined text-3xl"
        :class="iconColorClass"
      >
        {{ template.icon }}
      </span>
    </div>

    <!-- Content -->
    <div class="flex flex-col gap-2">
      <h3 class="text-text-light dark:text-text-dark text-lg font-bold leading-normal">
        {{ template.name }}
      </h3>
      <p class="text-subtext-light dark:text-subtext-dark text-sm font-normal leading-normal">
        {{ template.description }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  template: {
    type: Object,
    required: true
  }
})

defineEmits(['select'])

// Dynamic classes baraye icon background va color
const iconBgClass = computed(() => {
  const colorMap = {
    indigo: 'bg-indigo-100 dark:bg-indigo-900/50',
    teal: 'bg-teal-100 dark:bg-teal-900/50',
    amber: 'bg-amber-100 dark:bg-amber-900/50',
    green: 'bg-green-100 dark:bg-green-900/50',
    blue: 'bg-blue-100 dark:bg-blue-900/50',
    orange: 'bg-orange-100 dark:bg-orange-900/50',
    gray: 'bg-gray-200 dark:bg-gray-700'
  }
  return colorMap[props.template.color] || colorMap.gray
})

const iconColorClass = computed(() => {
  const colorMap = {
    indigo: 'text-indigo-600 dark:text-indigo-400',
    teal: 'text-teal-600 dark:text-teal-400',
    amber: 'text-amber-600 dark:text-amber-400',
    green: 'text-green-600 dark:text-green-400',
    blue: 'text-blue-600 dark:text-blue-400',
    orange: 'text-orange-600 dark:text-orange-400',
    gray: 'text-subtext-light dark:text-subtext-dark'
  }
  return colorMap[props.template.color] || colorMap.gray
})
</script>
