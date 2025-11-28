<template>
  <AnimatedBackground />
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AnimatedBackground from '@/components/AnimatedBackground.vue'

const authStore = useAuthStore()

// Check mikonim user logged in hast ya na
onMounted(() => {
  authStore.initAuth()
})
</script>
