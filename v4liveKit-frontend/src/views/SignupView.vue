<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="mx-auto bg-center bg-no-repeat aspect-square bg-cover rounded-full size-20"
             style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBCmFpXNP5jugI3VGmxYF2ywZ3_vLcsFaQX6bibr_RdhAaHXYDgGvujOtj9NToW3kkzjhulBMn1boCbloFfxfluC8i-oMreTrxAbPN8AaOe4Aj4Skh1mow02iWt7InT-CPzOUdt2nLDl21gkA1l00xvtKTSo2YKq5_b9AbTguI_e3lZRtIiLZb4KiHjZr3Eyeh6upH-eF_AlxsmdzKZLedcWVHjaqVq_7FsbefBUq8-9NtbpW58qkhmKN05JfkROr89C1SwutHIXvCD");'>
        </div>
        <h2 class="mt-6 text-3xl font-black text-slate-900 dark:text-white">
          Create your account
        </h2>
        <p class="mt-2 text-sm text-slate-600 dark:text-slate-400">
          Get started with Voice AI Agents
        </p>
      </div>

      <!-- Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleSignup">
        <div class="space-y-4">
          <!-- Name -->
          <div>
            <label for="name" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Full name
            </label>
            <input
              id="name"
              v-model="name"
              type="text"
              required
              class="w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Enter your full name"
            />
          </div>

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
              minlength="6"
              class="w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Create a password (min. 6 characters)"
            />
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Confirm password
            </label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              required
              class="w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Confirm your password"
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
          <span v-if="loading">Creating account...</span>
          <span v-else>Sign up</span>
        </button>

        <!-- Login Link -->
        <p class="text-center text-sm text-slate-600 dark:text-slate-400">
          Already have an account?
          <router-link to="/login" class="font-medium text-primary hover:text-primary/90">
            Sign in
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

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

const handleSignup = async () => {
  error.value = ''

  // Validation
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }

  loading.value = true

  try {
    await authStore.signup(name.value, email.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Failed to create account. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
