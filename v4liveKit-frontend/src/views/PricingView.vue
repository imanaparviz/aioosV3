<template>
  <div class="min-h-screen">
    <!-- Fixed Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-white/70 dark:bg-slate-900/70 border-b border-slate-200/50 dark:border-slate-800/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <router-link to="/" class="flex items-center gap-3 group">
            <img src="/logo-medium.png" alt="AIOOS" class="w-10 h-10 object-contain group-hover:scale-105 transition-transform" />
            <span class="text-xl font-bold text-slate-900 dark:text-white">AIOOS</span>
          </router-link>

          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center gap-8">
            <router-link to="/#features" class="text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors">
              Features
            </router-link>
            <router-link to="/pricing" class="text-sm font-medium text-primary dark:text-primary">
              Pricing
            </router-link>
            <router-link to="/#testimonials" class="text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors">
              Testimonials
            </router-link>
          </div>

          <!-- Auth Buttons -->
          <div class="flex items-center gap-3">
            <router-link to="/login" class="px-4 py-2 text-sm font-semibold text-slate-700 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors">
              Log In
            </router-link>
            <router-link to="/login" class="px-6 py-2.5 text-sm font-bold text-white bg-gradient-to-r from-primary to-indigo-600 rounded-lg hover:shadow-lg hover:shadow-primary/50 transition-all hover:scale-105">
              Start Free
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-32 pb-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto text-center">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 dark:bg-primary/20 border border-primary/20 dark:border-primary/30 mb-6">
          <span class="size-2 rounded-full bg-primary animate-pulse"></span>
          <span class="text-sm font-semibold bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">
            Transparent Pricing
          </span>
        </div>

        <h1 class="text-5xl sm:text-6xl lg:text-7xl font-black leading-tight mb-6">
          <span class="bg-gradient-to-r from-slate-900 via-primary to-indigo-600 dark:from-white dark:via-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
            Powerful Voice AI
          </span>
          <br />
          <span class="text-slate-800 dark:text-white">For Every Scale</span>
        </h1>

        <p class="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto mb-8">
          Start free and scale up as you grow. No credit card required.
        </p>

        <!-- Billing Toggle -->
        <div class="flex items-center justify-center gap-4 mb-4">
          <span class="text-sm font-medium text-slate-600 dark:text-slate-400" :class="{ 'text-slate-900 dark:text-white font-bold': billingCycle === 'monthly' }">
            Monthly
          </span>
          <button
            @click="toggleBilling"
            class="relative w-16 h-8 rounded-full transition-colors duration-300"
            :class="billingCycle === 'yearly' ? 'bg-gradient-to-r from-primary to-indigo-600' : 'bg-slate-300 dark:bg-slate-700'"
          >
            <span
              class="absolute top-1 left-1 size-6 rounded-full bg-white shadow-lg transition-transform duration-300"
              :class="{ 'translate-x-8': billingCycle === 'yearly' }"
            ></span>
          </button>
          <span class="text-sm font-medium text-slate-600 dark:text-slate-400 flex items-center gap-2" :class="{ 'text-slate-900 dark:text-white font-bold': billingCycle === 'yearly' }">
            Yearly
            <span class="px-2 py-0.5 text-xs font-bold text-white bg-gradient-to-r from-green-500 to-emerald-600 rounded-full">
              Save 20%
            </span>
          </span>
        </div>
      </div>
    </section>

    <!-- Pricing Cards -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Basic Plan -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-slate-200 to-slate-300 dark:from-slate-800 dark:to-slate-700 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white dark:bg-slate-900 rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-slate-300/50 dark:hover:shadow-slate-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex-1">
                <h3 class="text-xl font-bold text-primary mb-2">Starter</h3>
                <div class="flex items-baseline gap-2 mb-4">
                  <span class="text-5xl font-black text-slate-900 dark:text-white">
                    ${{ billingCycle === 'monthly' ? '29' : '23' }}
                  </span>
                  <span class="text-slate-600 dark:text-slate-400 font-medium">/ month</span>
                </div>
                <p class="text-slate-600 dark:text-slate-400 mb-6">
                  For individuals & small teams getting started.
                </p>

                <button class="w-full py-3 px-6 rounded-xl font-bold text-primary bg-primary/10 hover:bg-primary/20 border-2 border-primary/20 hover:border-primary/40 transition-all mb-8">
                  Start Free Trial
                </button>

                <div class="space-y-4 pt-6 border-t border-slate-200 dark:border-slate-800">
                  <p class="text-sm font-bold text-slate-900 dark:text-white mb-4">Includes:</p>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">5 Voice Agents</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Basic Analytics Dashboard</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">API Access</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Email Support</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">14-Day Free Trial</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pro Plan (Featured) -->
          <div class="relative transform md:scale-105 md:-my-4">
            <div class="absolute -inset-1 bg-gradient-to-r from-primary to-indigo-600 rounded-3xl blur"></div>
            <div class="relative bg-white dark:bg-slate-900 rounded-3xl p-8 border-2 border-primary h-full flex flex-col">
              <!-- Most Popular Badge -->
              <div class="absolute -top-4 left-1/2 -translate-x-1/2 px-6 py-2 bg-gradient-to-r from-primary to-indigo-600 text-white text-sm font-bold rounded-full shadow-lg">
                Most Popular
              </div>

              <div class="flex-1">
                <h3 class="text-xl font-bold text-primary mb-2 mt-2">Professional</h3>
                <div class="flex items-baseline gap-2 mb-4">
                  <span class="text-5xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">
                    ${{ billingCycle === 'monthly' ? '99' : '79' }}
                  </span>
                  <span class="text-slate-600 dark:text-slate-400 font-medium">/ month</span>
                </div>
                <p class="text-slate-600 dark:text-slate-400 mb-6">
                  For growing businesses that need more power.
                </p>

                <button class="w-full py-3 px-6 rounded-xl font-bold text-white bg-gradient-to-r from-primary to-indigo-600 hover:shadow-lg hover:shadow-primary/50 transition-all hover:scale-105 mb-8">
                  Choose Plan
                </button>

                <div class="space-y-4 pt-6 border-t border-slate-200 dark:border-slate-800">
                  <p class="text-sm font-bold text-slate-900 dark:text-white mb-4">Everything in Starter, plus:</p>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">50 Voice Agents</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Advanced Analytics & Reports</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Custom Integrations</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Priority Support (24/7)</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-primary text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Team Collaboration Tools</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Enterprise Plan -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white dark:bg-slate-900 rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-indigo-300/50 dark:hover:shadow-indigo-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex-1">
                <h3 class="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">Enterprise</h3>
                <div class="flex items-baseline gap-2 mb-4">
                  <span class="text-5xl font-black text-slate-900 dark:text-white">Custom</span>
                </div>
                <p class="text-slate-600 dark:text-slate-400 mb-6">
                  For large organizations with specific needs.
                </p>

                <button class="w-full py-3 px-6 rounded-xl font-bold text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:shadow-lg hover:shadow-indigo-500/50 transition-all hover:scale-105 mb-8">
                  Contact Sales
                </button>

                <div class="space-y-4 pt-6 border-t border-slate-200 dark:border-slate-800">
                  <p class="text-sm font-bold text-slate-900 dark:text-white mb-4">Everything in Professional, plus:</p>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-indigo-600 text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Unlimited Voice Agents</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-indigo-600 text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">White-label Solutions</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-indigo-600 text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Dedicated Account Manager</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-indigo-600 text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">Custom SLAs & Security</span>
                  </div>
                  <div class="flex items-start gap-3">
                    <span class="material-symbols-outlined text-indigo-600 text-xl flex-shrink-0">check_circle</span>
                    <span class="text-sm text-slate-700 dark:text-slate-300">On-premise Deployment</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Feature Comparison Table -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-4xl md:text-5xl font-black text-center mb-12">
          <span class="bg-gradient-to-r from-slate-900 via-primary to-indigo-600 dark:from-white dark:via-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
            Compare All Features
          </span>
        </h2>

        <div class="relative">
          <div class="absolute -inset-4 bg-gradient-to-r from-primary/10 via-indigo-500/10 to-purple-500/10 rounded-3xl blur-2xl"></div>
          <div class="relative overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead class="bg-gradient-to-r from-slate-100 to-slate-50 dark:from-slate-800/50 dark:to-slate-900/50">
                  <tr>
                    <th class="px-6 py-4 text-left text-sm font-bold text-slate-900 dark:text-white">Feature</th>
                    <th class="px-6 py-4 text-center text-sm font-bold text-slate-900 dark:text-white">Starter</th>
                    <th class="px-6 py-4 text-center text-sm font-bold text-primary">Professional</th>
                    <th class="px-6 py-4 text-center text-sm font-bold text-indigo-600">Enterprise</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="border-t border-slate-200 dark:border-slate-800">
                    <td class="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-300">Number of Voice Agents</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">5</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">50</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">Unlimited</td>
                  </tr>
                  <tr class="border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30">
                    <td class="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-300">API Access</td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-primary">check_circle</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-primary">check_circle</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-indigo-600">check_circle</span></td>
                  </tr>
                  <tr class="border-t border-slate-200 dark:border-slate-800">
                    <td class="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-300">Analytics Dashboard</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">Basic</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">Advanced</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">Advanced + Custom</td>
                  </tr>
                  <tr class="border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30">
                    <td class="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-300">Custom Integrations</td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-slate-400">cancel</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-primary">check_circle</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-indigo-600">check_circle</span></td>
                  </tr>
                  <tr class="border-t border-slate-200 dark:border-slate-800">
                    <td class="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-300">Team Collaboration</td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-slate-400">cancel</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-primary">check_circle</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-indigo-600">check_circle</span></td>
                  </tr>
                  <tr class="border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30">
                    <td class="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-300">Support Level</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">Email</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">Priority 24/7</td>
                    <td class="px-6 py-4 text-center text-sm text-slate-600 dark:text-slate-400">Dedicated</td>
                  </tr>
                  <tr class="border-t border-slate-200 dark:border-slate-800">
                    <td class="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-300">White-label</td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-slate-400">cancel</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-slate-400">cancel</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-indigo-600">check_circle</span></td>
                  </tr>
                  <tr class="border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30">
                    <td class="px-6 py-4 text-sm font-medium text-slate-700 dark:text-slate-300">Security SLAs</td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-slate-400">cancel</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-slate-400">cancel</span></td>
                    <td class="px-6 py-4 text-center"><span class="material-symbols-outlined text-indigo-600">check_circle</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl md:text-5xl font-black text-center mb-12">
          <span class="bg-gradient-to-r from-slate-900 via-primary to-indigo-600 dark:from-white dark:via-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
            Frequently Asked Questions
          </span>
        </h2>

        <div class="space-y-4">
          <div v-for="(faq, index) in faqs" :key="index" class="group">
            <div class="relative">
              <div class="absolute -inset-0.5 bg-gradient-to-r from-primary/20 to-indigo-600/20 rounded-2xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-300"></div>
              <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden">
                <button
                  @click="toggleFAQ(index)"
                  class="w-full px-6 py-5 flex items-center justify-between text-left hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
                >
                  <h3 class="text-base font-bold text-slate-900 dark:text-white pr-4">{{ faq.question }}</h3>
                  <span class="material-symbols-outlined text-primary flex-shrink-0 transition-transform duration-300" :class="{ 'rotate-180': faq.open }">
                    expand_more
                  </span>
                </button>
                <transition
                  enter-active-class="transition-all duration-300 ease-out"
                  leave-active-class="transition-all duration-200 ease-in"
                  enter-from-class="max-h-0 opacity-0"
                  enter-to-class="max-h-96 opacity-100"
                  leave-from-class="max-h-96 opacity-100"
                  leave-to-class="max-h-0 opacity-0"
                >
                  <div v-if="faq.open" class="px-6 pb-5 border-t border-slate-200 dark:border-slate-800">
                    <p class="pt-4 text-slate-600 dark:text-slate-400 leading-relaxed">{{ faq.answer }}</p>
                  </div>
                </transition>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-5xl mx-auto">
        <div class="relative">
          <div class="absolute -inset-1 bg-gradient-to-r from-primary via-indigo-600 to-purple-600 rounded-3xl blur-lg opacity-10"></div>
          <div class="relative bg-gradient-to-br from-primary to-indigo-600 rounded-3xl p-12 text-center">
            <h2 class="text-4xl md:text-5xl font-black text-white mb-4">
              Ready to Get Started?
            </h2>
            <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of businesses automating their voice agents with AIOOS
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
              <router-link to="/login" class="px-8 py-4 text-lg font-bold text-primary bg-white rounded-xl hover:shadow-2xl hover:scale-105 transition-all">
                Start Free Trial
              </router-link>
              <button class="px-8 py-4 text-lg font-bold text-white border-2 border-white rounded-xl hover:bg-white/10 transition-all">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <!-- Brand -->
          <div class="flex flex-col gap-4">
            <div class="flex items-center gap-3">
              <img src="/logo-medium.png" alt="AIOOS" class="w-10 h-10 object-contain" />
              <span class="text-2xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">
                AIOOS
              </span>
            </div>
            <p class="text-sm text-slate-600 dark:text-slate-400">
              The leading platform for AI voice agent management.
            </p>
          </div>

          <!-- Product -->
          <div>
            <h3 class="text-sm font-bold text-slate-900 dark:text-white mb-4">Product</h3>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><router-link to="/features" class="hover:text-primary transition-colors">Features</router-link></li>
              <li><router-link to="/pricing" class="hover:text-primary transition-colors">Pricing</router-link></li>
              <li><router-link to="/solutions" class="hover:text-primary transition-colors">Solutions</router-link></li>
              <li><a href="#" class="hover:text-primary transition-colors">Documentation</a></li>
            </ul>
          </div>

          <!-- Company -->
          <div>
            <h3 class="text-sm font-bold text-slate-900 dark:text-white mb-4">Company</h3>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><router-link to="/" class="hover:text-primary transition-colors">About Us</router-link></li>
              <li><router-link to="/" class="hover:text-primary transition-colors">Careers</router-link></li>
              <li><router-link to="/" class="hover:text-primary transition-colors">Contact</router-link></li>
              <li><router-link to="/" class="hover:text-primary transition-colors">Blog</router-link></li>
            </ul>
          </div>

          <!-- Legal -->
          <div>
            <h3 class="text-sm font-bold text-slate-900 dark:text-white mb-4">Legal</h3>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li><router-link to="/" class="hover:text-primary transition-colors">Terms of Service</router-link></li>
              <li><router-link to="/" class="hover:text-primary transition-colors">Privacy Policy</router-link></li>
              <li><router-link to="/" class="hover:text-primary transition-colors">Cookie Policy</router-link></li>
            </ul>
          </div>
        </div>

        <div class="pt-8 border-t border-slate-200 dark:border-slate-800 text-center text-sm text-slate-600 dark:text-slate-400">
          <p>&copy; 2026 AIOOS. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const billingCycle = ref('monthly')

const toggleBilling = () => {
  billingCycle.value = billingCycle.value === 'monthly' ? 'yearly' : 'monthly'
}

const faqs = ref([
  {
    question: 'Can I change my plan later?',
    answer: 'Yes, you can upgrade or downgrade your plan at any time from your account settings. Prorated charges or credits will be applied automatically.',
    open: false
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards, including Visa, Mastercard, and American Express. For Enterprise plans, we also support invoicing and bank transfers.',
    open: false
  },
  {
    question: 'Is there a free trial?',
    answer: 'Yes, we offer a 14-day free trial on our Starter plan. No credit card is required to get started.',
    open: false
  },
  {
    question: 'What happens if I exceed my usage limits?',
    answer: 'If you exceed the limits of your current plan, we will notify you. You will have the option to upgrade your plan to accommodate your growing needs. We do not charge overage fees automatically.',
    open: false
  },
  {
    question: 'Do you offer refunds?',
    answer: 'Yes, we offer a 30-day money-back guarantee for all paid plans. If you\'re not satisfied with AIOOS, contact our support team for a full refund.',
    open: false
  },
  {
    question: 'Can I cancel my subscription anytime?',
    answer: 'Absolutely! You can cancel your subscription at any time from your account settings. Your access will continue until the end of your current billing period.',
    open: false
  }
])

const toggleFAQ = (index) => {
  faqs.value[index].open = !faqs.value[index].open
}
</script>
