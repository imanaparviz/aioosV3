<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="mx-auto bg-center bg-no-repeat aspect-square bg-cover rounded-full size-20"
             style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBCmFpXNP5jugI3VGmxYF2ywZ3_vLcsFaQX6bibr_RdhAaHXYDgGvujOtj9NToW3kkzjhulBMn1boCbloFfxfluC8i-oMreTrxAbPN8AaOe4Aj4Skh1mow02iWt7InT-CPzOUdt2nLDl21gkA1l00xvtKTSo2YKq5_b9AbTguI_e3lZRtIiLZb4KiHjZr3Eyeh6upH-eF_AlxsmdzKZLedcWVHjaqVq_7FsbefBUq8-9NtbpW58qkhmKN05JfkROr89C1SwutHIXvCD");'>
        </div>
        <h2 class="mt-6 text-3xl font-black text-slate-900 dark:text-white">
          Welcome back
        </h2>
        <p class="mt-2 text-sm text-slate-600 dark:text-slate-400">
          Sign in to your Voice AI account
        </p>
      </div>

      <!-- Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Email address
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Enter your email"
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Enter your password"
            />
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="text-red-600 dark:text-red-400 text-sm text-center">
          {{ error }}
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full flex justify-center items-center gap-2 py-3 px-4 rounded-lg bg-primary text-white font-bold hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="loading">Loading...</span>
          <span v-else>Sign in</span>
        </button>

        <!-- Signup Link -->
        <p class="text-center text-sm text-slate-600 dark:text-slate-400">
          Don't have an account?
          <router-link to="/signup" class="font-medium text-primary hover:text-primary/90">
            Sign up
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Failed to login. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
