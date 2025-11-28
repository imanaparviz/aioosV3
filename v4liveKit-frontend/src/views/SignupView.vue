<template>
  <div class="min-h-screen flex bg-white dark:bg-slate-900">
    <!-- Left Side - Form -->
    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24 w-full lg:w-1/2 bg-white dark:bg-slate-900">
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <div class="flex items-center gap-3">
            <div class="bg-primary/10 p-2 rounded-xl">
               <div class="bg-center bg-no-repeat aspect-square bg-cover rounded-lg size-10"
                 style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBCmFpXNP5jugI3VGmxYF2ywZ3_vLcsFaQX6bibr_RdhAaHXYDgGvujOtj9NToW3kkzjhulBMn1boCbloFfxfluC8i-oMreTrxAbPN8AaOe4Aj4Skh1mow02iWt7InT-CPzOUdt2nLDl21gkA1l00xvtKTSo2YKq5_b9AbTguI_e3lZRtIiLZb4KiHjZr3Eyeh6upH-eF_AlxsmdzKZLedcWVHjaqVq_7FsbefBUq8-9NtbpW58qkhmKN05JfkROr89C1SwutHIXvCD");'>
               </div>
            </div>
            <span class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">Voice AI</span>
          </div>
          <h2 class="mt-8 text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Create your account
          </h2>
          <p class="mt-2 text-sm text-slate-600 dark:text-slate-400">
            Get started with your 14-day free trial.
          </p>
        </div>

        <div class="mt-10">
          <form @submit.prevent="handleSignup" class="space-y-6">
            <div>
              <label for="name" class="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Full name
              </label>
              <div class="mt-1 relative">
                <input
                  id="name"
                  v-model="name"
                  type="text"
                  autocomplete="name"
                  required
                  class="appearance-none block w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200 sm:text-sm"
                  placeholder="Enter your full name"
                />
              </div>
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Email address
              </label>
              <div class="mt-1 relative">
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  autocomplete="email"
                  required
                  class="appearance-none block w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200 sm:text-sm"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div class="space-y-1">
              <label for="password" class="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Password
              </label>
              <div class="mt-1 relative">
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  autocomplete="new-password"
                  required
                  minlength="6"
                  class="appearance-none block w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200 sm:text-sm"
                  placeholder="Create a password (min. 6 characters)"
                />
              </div>
            </div>

            <div class="space-y-1">
              <label for="confirmPassword" class="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Confirm password
              </label>
              <div class="mt-1 relative">
                <input
                  id="confirmPassword"
                  v-model="confirmPassword"
                  type="password"
                  autocomplete="new-password"
                  required
                  class="appearance-none block w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200 sm:text-sm"
                  placeholder="Confirm your password"
                />
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="rounded-lg bg-red-50 dark:bg-red-900/20 p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
                    {{ error }}
                  </h3>
                </div>
              </div>
            </div>

            <div>
              <button
                type="submit"
                :disabled="loading"
                class="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:-translate-y-0.5"
              >
                <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span v-else>Create account</span>
              </button>
            </div>
          </form>

          <div class="mt-8">
            <div class="relative">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-slate-200 dark:border-slate-700"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-white dark:bg-slate-900 text-slate-500">
                  Already have an account?
                </span>
              </div>
            </div>

            <div class="mt-6 grid grid-cols-1 gap-3">
              <router-link
                to="/login"
                class="w-full inline-flex justify-center py-3 px-4 border border-slate-300 dark:border-slate-700 rounded-xl shadow-sm bg-white dark:bg-slate-800 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
              >
                Sign in
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side - Image/Decorative -->
    <div class="hidden lg:block relative w-0 flex-1 overflow-hidden">
      <div class="absolute inset-0 h-full w-full bg-slate-900">
        <div class="absolute inset-0 bg-gradient-to-bl from-primary/20 to-slate-900 mix-blend-multiply"></div>
        <!-- Abstract Shapes -->
        <div class="absolute -top-24 -right-24 w-96 h-96 rounded-full bg-primary/20 blur-3xl"></div>
        <div class="absolute top-1/2 right-1/2 w-[30rem] h-[30rem] rounded-full bg-purple-500/20 blur-3xl"></div>
        <div class="absolute bottom-0 left-0 w-96 h-96 rounded-full bg-blue-500/20 blur-3xl"></div>
        
        <div class="relative h-full flex flex-col items-center justify-center p-12 text-center">
          <h2 class="text-4xl font-bold text-white mb-6">Join the Revolution</h2>
          <p class="text-lg text-slate-300 max-w-lg">
            Create intelligent voice agents in minutes. No coding required.
          </p>
          
          <!-- Decorative UI Element Mockup -->
          <div class="mt-12 w-full max-w-lg bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-2xl transform -rotate-2 hover:rotate-0 transition-transform duration-500">
             <div class="flex items-center justify-between mb-4">
               <div class="h-8 w-24 bg-white/10 rounded"></div>
               <div class="h-8 w-8 rounded-full bg-white/10"></div>
             </div>
             <div class="grid grid-cols-3 gap-4">
               <div class="h-24 bg-white/5 rounded-xl border border-white/5"></div>
               <div class="h-24 bg-white/5 rounded-xl border border-white/5"></div>
               <div class="h-24 bg-white/5 rounded-xl border border-white/5"></div>
             </div>
          </div>
        </div>
      </div>
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
