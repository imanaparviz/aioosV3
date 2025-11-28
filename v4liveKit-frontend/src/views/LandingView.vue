<template>
  <div class="min-h-screen">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-white/70 dark:bg-slate-900/70 border-b border-slate-200/50 dark:border-slate-800/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <router-link to="/" class="flex items-center gap-3 group cursor-pointer">
            <img src="/logo-medium.png" alt="AIOOS" class="w-10 h-10 object-contain group-hover:scale-105 transition-transform" />
            <span class="text-xl font-bold text-slate-900 dark:text-white">AIOOS</span>
          </router-link>

          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center gap-8">
            <router-link to="/features" class="text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary transition-colors">Features</router-link>
            <router-link to="/solutions" class="text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary transition-colors">Solutions</router-link>
            <router-link to="/pricing" class="text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary transition-colors">Pricing</router-link>
            <a href="#testimonials" class="text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary transition-colors">Testimonials</a>
          </div>

          <!-- CTA Buttons -->
          <div class="hidden md:flex items-center gap-3">
            <router-link
              to="/login"
              class="px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary transition-colors"
            >
              Login
            </router-link>
            <router-link
              to="/signup"
              class="px-6 py-2.5 bg-gradient-to-r from-primary to-indigo-600 text-white rounded-lg font-bold text-sm hover:shadow-lg hover:shadow-primary/30 transition-all duration-300 hover:-translate-y-0.5"
            >
              Get Started Free
            </router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800">
            <span class="material-symbols-outlined text-slate-700 dark:text-slate-300">menu</span>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
        <div class="px-4 py-4 space-y-3">
          <router-link to="/features" class="block px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg">Features</router-link>
          <router-link to="/solutions" class="block px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg">Solutions</router-link>
          <router-link to="/pricing" class="block px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg">Pricing</router-link>
          <a href="#testimonials" class="block px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg">Testimonials</a>
          <router-link to="/login" class="block px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg">Login</router-link>
          <router-link to="/signup" class="block px-4 py-2 bg-gradient-to-r from-primary to-indigo-600 text-white rounded-lg font-bold text-sm text-center">Get Started Free</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="text-center max-w-4xl mx-auto">
          <!-- Badge -->
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 backdrop-blur-sm border border-primary/20 mb-8 animate-pulse">
            <span class="size-2 bg-primary rounded-full"></span>
            <span class="text-sm font-semibold text-primary">AI-Powered Voice Agent Platform</span>
          </div>

          <!-- Headline -->
          <h1 class="text-5xl sm:text-6xl lg:text-7xl font-black leading-tight mb-6">
            <span class="bg-gradient-to-r from-slate-900 via-primary to-indigo-600 dark:from-white dark:via-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
              Automate Your Voice Agents
            </span>
            <br />
            <span class="text-slate-800 dark:text-white">With AI Intelligence</span>
          </h1>

          <!-- Subtitle -->
          <p class="text-xl text-slate-600 dark:text-slate-400 mb-10 max-w-2xl mx-auto">
            Transform customer interactions with AIOOS. Boost efficiency by 10x, reduce costs by 70%, and deliver exceptional experiences 24/7.
          </p>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <router-link
              to="/signup"
              class="group px-8 py-4 bg-gradient-to-r from-primary to-indigo-600 text-white rounded-xl font-bold text-lg hover:shadow-2xl hover:shadow-primary/40 transition-all duration-300 hover:-translate-y-1 flex items-center gap-2"
            >
              <span>Start Free Trial</span>
              <span class="material-symbols-outlined group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </router-link>
            <button class="px-8 py-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold text-lg border-2 border-slate-200 dark:border-slate-700 hover:border-primary dark:hover:border-primary transition-all duration-300 flex items-center gap-2">
              <span class="material-symbols-outlined">play_circle</span>
              <span>Watch Demo</span>
            </button>
          </div>

          <!-- Dashboard Preview -->
          <div class="relative group">
            <div class="absolute -inset-1 bg-gradient-to-r from-primary to-indigo-600 rounded-2xl blur-2xl opacity-30 group-hover:opacity-50 transition-opacity"></div>
            <div class="relative bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden">
              <video
                autoplay
                loop
                muted
                playsinline
                class="w-full aspect-video rounded-xl object-cover"
              >
                <source src="/demo-video.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm border-y border-slate-200/50 dark:border-slate-800/50">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-4xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent mb-2">10x</div>
            <div class="text-sm font-medium text-slate-600 dark:text-slate-400">Faster Response</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent mb-2">70%</div>
            <div class="text-sm font-medium text-slate-600 dark:text-slate-400">Cost Reduction</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent mb-2">24/7</div>
            <div class="text-sm font-medium text-slate-600 dark:text-slate-400">Availability</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent mb-2">99.9%</div>
            <div class="text-sm font-medium text-slate-600 dark:text-slate-400">Uptime SLA</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section - Will continue in next edit -->
    <section id="features" class="py-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl sm:text-5xl font-black text-slate-900 dark:text-white mb-4">
            Everything You Need to <span class="bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">Succeed</span>
          </h2>
          <p class="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Powerful features designed to transform your voice agent operations
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-primary/20 to-indigo-600/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-primary/30 dark:hover:shadow-primary/50 transition-all duration-500">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-primary to-indigo-600 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">psychology</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3">AI-Powered Intelligence</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Advanced NLP and machine learning algorithms understand context and deliver human-like conversations.
              </p>
            </div>
          </div>

          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-emerald-300/50 dark:hover:shadow-emerald-900/50 transition-all duration-500">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">insights</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3">Real-time Analytics</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Track performance metrics, call quality, and customer satisfaction with actionable insights.
              </p>
            </div>
          </div>

          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-purple-300/50 dark:hover:shadow-purple-900/50 transition-all duration-500">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">language</span>
              </div>
              <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-3">Multi-language Support</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Communicate in 40+ languages with natural voice synthesis and recognition.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-24 px-4 sm:px-6 lg:px-8 bg-slate-50 dark:bg-slate-900/50">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl sm:text-5xl font-black text-slate-900 dark:text-white mb-4">
            Simple, <span class="bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">Transparent Pricing</span>
          </h2>
          <p class="text-xl text-slate-600 dark:text-slate-400">
            Start free, scale as you grow. No hidden fees.
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <!-- Starter -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-slate-200 to-slate-300 dark:from-slate-800 dark:to-slate-700 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-slate-300/50 dark:hover:shadow-slate-900/50 transition-all duration-500">
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">Starter</h3>
              <div class="mb-6">
                <span class="text-4xl font-black text-slate-900 dark:text-white">$49</span>
                <span class="text-slate-600 dark:text-slate-400">/month</span>
              </div>
              <ul class="space-y-4 mb-8">
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Up to 1,000 calls/month</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">2 voice agents</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Basic analytics</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Email support</span>
                </li>
              </ul>
              <router-link to="/signup" class="block w-full px-6 py-3 text-center bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
                Start Free Trial
              </router-link>
            </div>
          </div>

          <!-- Professional (Featured) -->
          <div class="relative transform md:scale-105">
            <div class="absolute -inset-1 bg-gradient-to-r from-primary to-indigo-600 rounded-3xl blur-xl opacity-75"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border-2 border-primary shadow-2xl shadow-primary/50">
              <div class="absolute -top-4 left-1/2 -translate-x-1/2 px-6 py-2 bg-gradient-to-r from-primary to-indigo-600 text-white text-sm font-bold rounded-full shadow-lg">
                Most Popular
              </div>
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">Professional</h3>
              <div class="mb-6">
                <span class="text-4xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">$199</span>
                <span class="text-slate-600 dark:text-slate-400">/month</span>
              </div>
              <ul class="space-y-4 mb-8">
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Up to 10,000 calls/month</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">10 voice agents</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Advanced analytics</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Priority support</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-primary">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">API access</span>
                </li>
              </ul>
              <router-link to="/signup" class="block w-full px-6 py-3 text-center bg-gradient-to-r from-primary to-indigo-600 text-white rounded-xl font-bold hover:shadow-2xl hover:shadow-primary/50 transition-all hover:scale-105">
                Start Free Trial
              </router-link>
            </div>
          </div>

          <!-- Enterprise -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-indigo-300/50 dark:hover:shadow-indigo-900/50 transition-all duration-500">
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">Enterprise</h3>
              <div class="mb-6">
                <span class="text-4xl font-black text-slate-900 dark:text-white">Custom</span>
              </div>
              <ul class="space-y-4 mb-8">
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-indigo-600">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Unlimited calls</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-indigo-600">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Unlimited agents</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-indigo-600">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Custom integrations</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-indigo-600">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">Dedicated support</span>
                </li>
                <li class="flex items-start gap-3">
                  <span class="material-symbols-outlined text-indigo-600">check_circle</span>
                  <span class="text-slate-600 dark:text-slate-400">SLA guarantee</span>
                </li>
              </ul>
              <router-link to="/" class="block w-full px-6 py-3 text-center bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl font-bold hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
                Contact Sales
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section id="testimonials" class="py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <!-- Background Gradient -->
      <div class="absolute inset-0 bg-gradient-to-b from-transparent via-primary/5 to-transparent pointer-events-none"></div>

      <div class="max-w-7xl mx-auto relative z-10">
        <div class="text-center mb-16">
          <h2 class="text-4xl sm:text-5xl font-black text-slate-900 dark:text-white mb-4">
            Loved by <span class="bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">Industry Leaders</span>
          </h2>
          <p class="text-xl text-slate-600 dark:text-slate-400">
            See what our customers have to say
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <!-- Testimonial 1 -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-primary/20 to-indigo-600/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200/50 dark:border-slate-800/50 hover:shadow-2xl hover:shadow-primary/10 transition-all duration-500 group-hover:border-primary/50 h-full flex flex-col">
              <!-- Stars -->
              <div class="flex gap-0.5 mb-6">
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </div>

              <!-- Quote -->
              <div class="mb-8 flex-grow">
                <svg class="size-10 text-primary/20 mb-4" fill="currentColor" viewBox="0 0 32 32">
                  <path d="M10 8c-3.3 0-6 2.7-6 6v10h10V14H8c0-1.1.9-2 2-2h2V8h-2zm12 0c-3.3 0-6 2.7-6 6v10h10V14h-6c0-1.1.9-2 2-2h2V8h-2z"/>
                </svg>
                <p class="text-lg text-slate-700 dark:text-slate-300 leading-relaxed italic">
                  "AIOOS transformed our customer service. We reduced response time by 80% and our customers love the instant support."
                </p>
              </div>

              <!-- Author -->
              <div class="flex items-center gap-4 pt-6 border-t border-slate-200/50 dark:border-slate-700/50">
                <div class="relative">
                  <div class="absolute -inset-1 bg-gradient-to-br from-primary to-indigo-600 rounded-full opacity-20 blur"></div>
                  <img
                    src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop&crop=faces"
                    alt="Sarah Chen"
                    class="relative size-14 rounded-full object-cover ring-2 ring-white dark:ring-slate-900"
                  />
                </div>
                <div>
                  <div class="font-bold text-slate-900 dark:text-white text-lg">Sarah Chen</div>
                  <div class="text-sm text-slate-600 dark:text-slate-400 font-medium">CEO, TechCorp</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Testimonial 2 -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-600/20 to-purple-600/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200/50 dark:border-slate-800/50 hover:shadow-2xl hover:shadow-indigo-500/10 transition-all duration-500 group-hover:border-indigo-500/50 h-full flex flex-col">
              <!-- Stars -->
              <div class="flex gap-0.5 mb-6">
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </div>

              <!-- Quote -->
              <div class="mb-8 flex-grow">
                <svg class="size-10 text-indigo-500/20 mb-4" fill="currentColor" viewBox="0 0 32 32">
                  <path d="M10 8c-3.3 0-6 2.7-6 6v10h10V14H8c0-1.1.9-2 2-2h2V8h-2zm12 0c-3.3 0-6 2.7-6 6v10h10V14h-6c0-1.1.9-2 2-2h2V8h-2z"/>
                </svg>
                <p class="text-lg text-slate-700 dark:text-slate-300 leading-relaxed italic">
                  "The ROI was immediate. AIOOS paid for itself in the first month. Highly recommend for any scaling business."
                </p>
              </div>

              <!-- Author -->
              <div class="flex items-center gap-4 pt-6 border-t border-slate-200/50 dark:border-slate-700/50">
                <div class="relative">
                  <div class="absolute -inset-1 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full opacity-20 blur"></div>
                  <img
                    src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=faces"
                    alt="Michael Brown"
                    class="relative size-14 rounded-full object-cover ring-2 ring-white dark:ring-slate-900"
                  />
                </div>
                <div>
                  <div class="font-bold text-slate-900 dark:text-white text-lg">Michael Brown</div>
                  <div class="text-sm text-slate-600 dark:text-slate-400 font-medium">COO, FinanceHub</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Testimonial 3 -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-pink-500/20 to-rose-600/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200/50 dark:border-slate-800/50 hover:shadow-2xl hover:shadow-pink-500/10 transition-all duration-500 group-hover:border-pink-500/50 h-full flex flex-col">
              <!-- Stars -->
              <div class="flex gap-0.5 mb-6">
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="size-5 fill-yellow-400" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </div>

              <!-- Quote -->
              <div class="mb-8 flex-grow">
                <svg class="size-10 text-pink-500/20 mb-4" fill="currentColor" viewBox="0 0 32 32">
                  <path d="M10 8c-3.3 0-6 2.7-6 6v10h10V14H8c0-1.1.9-2 2-2h2V8h-2zm12 0c-3.3 0-6 2.7-6 6v10h10V14h-6c0-1.1.9-2 2-2h2V8h-2z"/>
                </svg>
                <p class="text-lg text-slate-700 dark:text-slate-300 leading-relaxed italic">
                  "Implementation was seamless. The team is incredible and the platform just works. Best investment we've made."
                </p>
              </div>

              <!-- Author -->
              <div class="flex items-center gap-4 pt-6 border-t border-slate-200/50 dark:border-slate-700/50">
                <div class="relative">
                  <div class="absolute -inset-1 bg-gradient-to-br from-pink-500 to-rose-600 rounded-full opacity-20 blur"></div>
                  <img
                    src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=faces"
                    alt="Emily Rodriguez"
                    class="relative size-14 rounded-full object-cover ring-2 ring-white dark:ring-slate-900"
                  />
                </div>
                <div>
                  <div class="font-bold text-slate-900 dark:text-white text-lg">Emily Rodriguez</div>
                  <div class="text-sm text-slate-600 dark:text-slate-400 font-medium">CTO, CloudScale</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA Section -->
    <section class="py-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="relative">
          <div class="absolute -inset-1 bg-gradient-to-r from-primary to-indigo-600 rounded-3xl blur-lg opacity-10"></div>
          <div class="relative bg-gradient-to-br from-primary to-indigo-600 rounded-3xl p-12 text-center text-white">
            <h2 class="text-4xl sm:text-5xl font-black mb-6">
              Ready to Transform Your Business?
            </h2>
            <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of companies using AIOOS to deliver exceptional customer experiences.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
              <router-link
                to="/signup"
                class="px-8 py-4 bg-white text-primary rounded-xl font-bold text-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-1"
              >
                Start Free Trial - No Credit Card Required
              </router-link>
            </div>
            <p class="text-sm text-blue-100 mt-6">14-day free trial • Cancel anytime • No hidden fees</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
          <div class="col-span-2 md:col-span-1">
            <div class="flex items-center gap-2 mb-4">
              <img src="/logo-medium.png" alt="AIOOS" class="w-8 h-8 object-contain" />
              <span class="text-xl font-black text-slate-900 dark:text-white">AIOOS</span>
            </div>
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-4">
              The future of voice agent automation.
            </p>
          </div>

          <div>
            <h3 class="font-bold text-slate-900 dark:text-white mb-4">Product</h3>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><router-link to="/features" class="hover:text-primary transition-colors">Features</router-link></li>
              <li><router-link to="/pricing" class="hover:text-primary transition-colors">Pricing</router-link></li>
              <li><router-link to="/solutions" class="hover:text-primary transition-colors">Solutions</router-link></li>
              <li><a href="#" class="hover:text-primary transition-colors">Documentation</a></li>
            </ul>
          </div>

          <div>
            <h3 class="font-bold text-slate-900 dark:text-white mb-4">Company</h3>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><a href="#" class="hover:text-primary transition-colors">About Us</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Blog</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Careers</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Contact</a></li>
            </ul>
          </div>

          <div>
            <h3 class="font-bold text-slate-900 dark:text-white mb-4">Legal</h3>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><a href="#" class="hover:text-primary transition-colors">Terms of Service</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Privacy Policy</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Cookie Policy</a></li>
            </ul>
          </div>
        </div>

        <div class="pt-8 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-4">
          <p class="text-sm text-slate-600 dark:text-slate-400">
            © 2026 AIOOS. All rights reserved.
          </p>
          <div class="flex gap-4">
            <a href="#" class="text-slate-400 hover:text-primary transition-colors">
              <span class="material-symbols-outlined">link</span>
            </a>
            <a href="#" class="text-slate-400 hover:text-primary transition-colors">
              <span class="material-symbols-outlined">link</span>
            </a>
            <a href="#" class="text-slate-400 hover:text-primary transition-colors">
              <span class="material-symbols-outlined">link</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

// Agar user logged in bashe, befreste be dashboard
onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>

<style scoped>
/* Smooth scroll behavior */
html {
  scroll-behavior: smooth;
}
</style>
