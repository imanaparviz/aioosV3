<template>
  <div class="flex flex-col gap-3">
    <!-- Step Info -->
    <div class="flex items-center justify-between">
      <p class="text-text-dark dark:text-white text-sm font-medium">
        Step {{ currentStep }} of {{ totalSteps }}
      </p>
      <p class="text-secondary-gray dark:text-gray-400 text-sm font-normal">
        {{ stepLabel }}
      </p>
    </div>

    <!-- Progress Bar -->
    <div class="w-full bg-border-light dark:bg-border-dark rounded-full h-2">
      <div
        class="bg-primary-blue h-2 rounded-full transition-all duration-300"
        :style="{ width: progressPercentage + '%' }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentStep: {
    type: Number,
    required: true,
    default: 1
  },
  totalSteps: {
    type: Number,
    required: true,
    default: 3
  },
  stepLabel: {
    type: String,
    default: 'Configuration'
  }
})

const progressPercentage = computed(() => {
  return Math.round((props.currentStep / props.totalSteps) * 100)
})
</script>
