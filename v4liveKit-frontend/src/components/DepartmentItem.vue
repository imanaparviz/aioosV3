<template>
  <div class="flex items-center gap-4 rounded-lg border border-border-light dark:border-border-dark p-4 bg-background-light dark:bg-background-dark">
    <!-- Icon -->
    <div class="flex-shrink-0 size-10 rounded-lg bg-primary/10 dark:bg-primary/20 flex items-center justify-center">
      <span class="material-symbols-outlined text-primary-blue">
        {{ department.icon }}
      </span>
    </div>

    <!-- Department Info -->
    <div class="flex-grow">
      <p class="font-bold text-text-dark dark:text-white">
        {{ department.name }}
      </p>
      <p class="text-sm text-secondary-gray dark:text-gray-400">
        {{ department.description }} {{ department.phone ? `(${department.phone})` : '' }}
      </p>
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-2">
      <button
        @click="$emit('edit', department)"
        class="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 text-secondary-gray dark:text-gray-400 transition-colors"
        type="button"
      >
        <span class="material-symbols-outlined text-lg">edit</span>
      </button>
      <button
        @click="$emit('delete', department)"
        class="p-2 rounded-md hover:bg-red-100 dark:hover:bg-red-900/50 text-error-red transition-colors"
        type="button"
      >
        <span class="material-symbols-outlined text-lg">delete</span>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  department: {
    type: Object,
    required: true
  }
})

defineEmits(['edit', 'delete'])
</script>
