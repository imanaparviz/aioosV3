<template>
  <div class="min-h-screen flex font-display text-white selection:bg-banana-500/30">
    <!-- Left Side - Brand Experience (Desktop Only) -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-black/20 backdrop-blur-3xl">
      <!-- Animated Background Particles -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute top-[-10%] left-[-10%] w-[600px] h-[600px] bg-banana-500/5 rounded-full blur-[120px] animate-pulse-slow"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-purple-500/5 rounded-full blur-[100px] animate-pulse-slow delay-1000"></div>
        <div class="absolute top-[40%] left-[40%] w-[300px] h-[300px] bg-blue-500/5 rounded-full blur-[80px] animate-float"></div>
      </div>

      <!-- Grid Pattern -->
      <div class="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-[0.03]"></div>

      <div class="relative z-10 w-full flex flex-col justify-between p-12 xl:p-16">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <img src="/logo-medium.png" alt="AIOOS" class="w-10 h-10 object-contain" />
          <span class="text-xl font-bold text-white">AIOOS</span>
        </div>

        <!-- Hero Content -->
        <div class="space-y-12">
          <div class="space-y-6">
            <h1 class="text-5xl font-bold leading-tight tracking-tight">
              The Future of <br />
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-banana-400 to-banana-600">Voice Intelligence</span>
            </h1>
            <p class="text-slate-400 text-lg max-w-md leading-relaxed">
              Orchestrate millions of autonomous voice agents with nano-second latency and human-like empathy.
            </p>
          </div>

          <!-- Floating Stats Cards -->
          <div class="grid grid-cols-2 gap-4 max-w-md">
            <div class="bg-white/5 backdrop-blur-xl border border-white/10 p-5 rounded-2xl hover:bg-white/10 transition-colors duration-300 group">
              <div class="flex items-center gap-3 mb-2">
                <div class="p-2 rounded-lg bg-banana-500/10 text-banana-500 group-hover:scale-110 transition-transform">
                  <span class="material-symbols-outlined text-xl">speed</span>
                </div>
                <span class="text-sm text-slate-400 font-medium">Latency</span>
              </div>
              <div class="text-2xl font-bold text-white">~50ms</div>
              <div class="text-xs text-slate-500 mt-1">Global Edge Network</div>
            </div>
            
            <div class="bg-white/5 backdrop-blur-xl border border-white/10 p-5 rounded-2xl hover:bg-white/10 transition-colors duration-300 group">
              <div class="flex items-center gap-3 mb-2">
                <div class="p-2 rounded-lg bg-green-500/10 text-green-500 group-hover:scale-110 transition-transform">
                  <span class="material-symbols-outlined text-xl">verified_user</span>
                </div>
                <span class="text-sm text-slate-400 font-medium">Uptime</span>
              </div>
              <div class="text-2xl font-bold text-white">99.99%</div>
              <div class="text-xs text-slate-500 mt-1">Enterprise SLA</div>
            </div>
          </div>
        </div>

        <!-- Trust Indicator -->
        <div class="flex items-center gap-4 text-sm text-slate-500">
          <div class="flex -space-x-2">
            <div v-for="i in 4" :key="i" class="w-8 h-8 rounded-full border-2 border-[#0A0A0A] bg-slate-800 flex items-center justify-center text-xs text-white overflow-hidden">
               <img :src="`https://i.pravatar.cc/100?img=${i + 10}`" alt="User" class="w-full h-full object-cover opacity-80" />
            </div>
          </div>
          <p>Trusted by 10,000+ developers</p>
        </div>
      </div>
    </div>

    <!-- Right Side - Auth Form -->
    <div class="w-full lg:w-1/2 flex flex-col justify-center items-center p-6 sm:p-12 relative">
      <!-- Mobile Background -->
      <div class="absolute inset-0 lg:bg-transparent -z-10">
         <div class="absolute top-[-20%] right-[-20%] w-[300px] h-[300px] bg-banana-500/10 rounded-full blur-[100px]"></div>
      </div>

      <!-- Mobile Brand Header -->
      <div class="lg:hidden absolute top-0 left-0 w-full p-6 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <img src="/logo-medium.png" alt="AIOOS" class="w-8 h-8 object-contain" />
          <span class="text-xl font-bold text-white">AIOOS</span>
        </div>
      </div>

      <div class="w-full max-w-[420px] space-y-8 mt-16 lg:mt-0">
        <!-- Header -->
        <div class="text-center space-y-2">
          <h2 class="text-3xl font-bold text-white tracking-tight">
            {{ isLogin ? 'Welcome back' : 'Create account' }}
          </h2>
          <p class="text-slate-400">
            {{ isLogin ? 'Enter your credentials to access the dashboard' : 'Start building your voice agents today' }}
          </p>
        </div>

        <!-- Social Auth -->
        <div class="grid grid-cols-2 gap-4">
          <button class="flex items-center justify-center gap-3 py-3 px-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all duration-200 group">
            <img src="https://www.svgrepo.com/show/475656/google-color.svg" class="w-5 h-5 opacity-80 group-hover:opacity-100 transition-opacity" alt="Google" />
            <span class="text-sm font-medium text-slate-300 group-hover:text-white">Google</span>
          </button>
          <button class="flex items-center justify-center gap-3 py-3 px-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all duration-200 group">
            <img src="https://www.svgrepo.com/show/512317/github-142.svg" class="w-5 h-5 invert opacity-80 group-hover:opacity-100 transition-opacity" alt="GitHub" />
            <span class="text-sm font-medium text-slate-300 group-hover:text-white">GitHub</span>
          </button>
        </div>

        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-white/10"></div>
          </div>
          <div class="relative flex justify-center text-xs uppercase tracking-wider">
            <span class="px-4 text-slate-500">Or continue with email</span>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- Name Field (Signup Only) -->
          <div v-if="!isLogin" class="group">
            <label class="block text-xs font-medium text-slate-400 mb-1.5 ml-1 uppercase tracking-wider group-focus-within:text-banana-400 transition-colors">Full Name</label>
            <div class="relative">
              <input
                v-model="name"
                type="text"
                required
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 focus:outline-none focus:border-banana-500/50 focus:bg-white/10 focus:ring-1 focus:ring-banana-500/50 transition-all duration-300"
                placeholder="John Doe"
              />
              <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-600 group-focus-within:text-banana-500 transition-colors">person</span>
            </div>
          </div>

          <!-- Email Field -->
          <div class="group">
            <label class="block text-xs font-medium text-slate-400 mb-1.5 ml-1 uppercase tracking-wider group-focus-within:text-banana-400 transition-colors">Email Address</label>
            <div class="relative">
              <input
                v-model="email"
                type="email"
                required
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 focus:outline-none focus:border-banana-500/50 focus:bg-white/10 focus:ring-1 focus:ring-banana-500/50 transition-all duration-300"
                placeholder="name@company.com"
              />
              <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-600 group-focus-within:text-banana-500 transition-colors">mail</span>
            </div>
          </div>

          <!-- Password Field -->
          <div class="group">
            <label class="block text-xs font-medium text-slate-400 mb-1.5 ml-1 uppercase tracking-wider group-focus-within:text-banana-400 transition-colors">Password</label>
            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 focus:outline-none focus:border-banana-500/50 focus:bg-white/10 focus:ring-1 focus:ring-banana-500/50 transition-all duration-300"
                placeholder="••••••••"
              />
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-600 hover:text-white transition-colors"
              >
                <span class="material-symbols-outlined">{{ showPassword ? 'visibility_off' : 'visibility' }}</span>
              </button>
            </div>
          </div>

          <!-- Options -->
          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2 cursor-pointer group">
              <input type="checkbox" class="w-4 h-4 rounded border-white/20 bg-white/5 text-banana-500 focus:ring-banana-500/50 transition-colors" />
              <span class="text-slate-400 group-hover:text-slate-300 transition-colors">
                {{ isLogin ? 'Remember me' : 'I agree to Terms' }}
              </span>
            </label>
            <a v-if="isLogin" href="#" class="text-banana-500 hover:text-banana-400 font-medium transition-colors">Forgot password?</a>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="p-3 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center gap-3 text-red-400 text-sm animate-shake">
            <span class="material-symbols-outlined text-lg">error</span>
            {{ error }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gradient-to-r from-banana-500 to-banana-600 hover:from-banana-400 hover:to-banana-500 text-black font-bold py-3.5 rounded-xl shadow-lg shadow-banana-500/20 hover:shadow-banana-500/40 transform hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="w-5 h-5 border-2 border-black/20 border-t-black rounded-full animate-spin"></span>
            <span v-else>{{ isLogin ? 'Sign In' : 'Create Account' }}</span>
            <span v-if="!loading" class="material-symbols-outlined text-lg">arrow_forward</span>
          </button>
        </form>

        <!-- Footer -->
        <div class="text-center">
          <p class="text-slate-500 text-sm">
            {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
            <button @click="isLogin = !isLogin" class="text-white hover:text-banana-400 font-medium transition-colors ml-1">
              {{ isLogin ? 'Create account' : 'Sign in' }}
            </button>
          </p>
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

const isLogin = ref(true)
const name = ref('')
const email = ref('imanaparviz@gmail.com')
const password = ref('Iman051051021')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const handleSubmit = async () => {
  error.value = ''
  loading.value = true

  try {
    if (isLogin.value) {
      await authStore.login(email.value, password.value)
    } else {
      // Simulate signup
      await new Promise(resolve => setTimeout(resolve, 1000))
      await authStore.login(email.value, password.value)
    }
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Authentication failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.animate-pulse-slow {
  animation: pulse 8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.animate-float {
  animation: float 6s ease-in-out infinite;
}
.delay-1000 {
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
</style>
