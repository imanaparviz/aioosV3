<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Check mikonim user logged in hast ya na
onMounted(() => {
  authStore.initAuth()
})
</script>
