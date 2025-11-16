<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
    <!-- Fixed Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-white/70 dark:bg-slate-900/70 border-b border-slate-200/50 dark:border-slate-800/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <router-link to="/" class="flex items-center gap-3 group">
            <div class="flex items-center justify-center size-10 rounded-xl bg-gradient-to-br from-primary to-indigo-600 text-white font-black text-xl shadow-lg shadow-primary/30 group-hover:scale-105 transition-transform">
              AI
            </div>
            <span class="text-2xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">
              AIOOS
            </span>
          </router-link>

          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center gap-8">
            <router-link to="/features" class="text-sm font-medium text-primary dark:text-primary">
              Features
            </router-link>
            <router-link to="/solutions" class="text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors">
              Solutions
            </router-link>
            <router-link to="/pricing" class="text-sm font-medium text-slate-700 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors">
              Pricing
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
            Powerful Features
          </span>
        </div>

        <h1 class="text-5xl sm:text-6xl lg:text-7xl font-black leading-tight mb-6">
          <span class="bg-gradient-to-r from-slate-900 via-primary to-indigo-600 dark:from-white dark:via-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
            Seamless Control
          </span>
          <br />
          <span class="text-slate-800 dark:text-white">Limitless Possibilities</span>
        </h1>

        <p class="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
          Explore the tools that make our AI voice agents the most intelligent, adaptable, and easy-to-manage solution on the market.
        </p>
      </div>
    </section>

    <!-- Feature Cards Grid -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Omnichannel Integration -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-blue-300/50 dark:hover:shadow-blue-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">hub</span>
              </div>
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Omnichannel Integration</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Connect with customers on their preferred channels. Our agents seamlessly integrate with phone systems, web chat, SMS, and popular messaging apps.
              </p>
            </div>
          </div>

          <!-- Advanced NLP & NLU -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-purple-300/50 dark:hover:shadow-purple-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">psychology</span>
              </div>
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Advanced NLP & NLU</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Powered by state-of-the-art Natural Language Processing, our agents understand context, sentiment, and intent for truly human-like conversations.
              </p>
            </div>
          </div>

          <!-- No-Code Flow Builder -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-emerald-300/50 dark:hover:shadow-emerald-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">account_tree</span>
              </div>
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">No-Code Flow Builder</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Design, build, and deploy complex conversation flows with our intuitive drag-and-drop interface. No coding experience required.
              </p>
            </div>
          </div>

          <!-- Real-Time Analytics -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-amber-300/50 dark:hover:shadow-amber-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">bar_chart</span>
              </div>
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Real-Time Analytics</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Monitor performance with a comprehensive dashboard. Track call volume, resolution rates, customer satisfaction, and more to make data-driven decisions.
              </p>
            </div>
          </div>

          <!-- Seamless CRM Integration -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-500/20 to-violet-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-indigo-300/50 dark:hover:shadow-indigo-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">api</span>
              </div>
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Seamless CRM Integration</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Connect to your existing CRM and business tools. Personalize interactions by giving agents access to customer history and data in real-time.
              </p>
            </div>
          </div>

          <!-- Agent Customization -->
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-rose-500/20 to-red-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-rose-300/50 dark:hover:shadow-rose-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-rose-500 to-red-500 text-white shadow-lg mb-6">
                <span class="material-symbols-outlined text-3xl">tune</span>
              </div>
              <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Agent Customization</h3>
              <p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                Tailor your agent's voice, personality, and language to perfectly match your brand identity and connect with your target audience.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Live Monitoring Feature Section -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="flex flex-col gap-6">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 dark:bg-primary/20 border border-primary/20 dark:border-primary/30 w-fit">
              <span class="text-sm font-bold text-primary">Live Monitoring & Takeover</span>
            </div>

            <h2 class="text-4xl md:text-5xl font-black text-slate-900 dark:text-white leading-tight">
              <span class="bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">Never Miss</span> a Beat
            </h2>

            <p class="text-lg text-slate-600 dark:text-slate-400 leading-relaxed">
              Our live dashboard allows your human agents to monitor AI conversations in real-time. If a conversation requires a human touch, they can seamlessly take over the call or chat with a single click, ensuring a perfect customer experience every time.
            </p>

            <ul class="space-y-4">
              <li class="flex items-start gap-3">
                <span class="material-symbols-outlined text-primary text-2xl flex-shrink-0 mt-0.5">check_circle</span>
                <div>
                  <p class="font-bold text-slate-900 dark:text-white">Real-time Monitoring</p>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Watch all AI conversations as they happen</p>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <span class="material-symbols-outlined text-primary text-2xl flex-shrink-0 mt-0.5">check_circle</span>
                <div>
                  <p class="font-bold text-slate-900 dark:text-white">One-Click Takeover</p>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Seamlessly switch from AI to human agent</p>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <span class="material-symbols-outlined text-primary text-2xl flex-shrink-0 mt-0.5">check_circle</span>
                <div>
                  <p class="font-bold text-slate-900 dark:text-white">Full Conversation Context</p>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Human agents see complete chat history</p>
                </div>
              </li>
            </ul>

            <button class="flex items-center gap-2 text-primary text-lg font-bold group w-fit">
              <span>See it in action</span>
              <span class="material-symbols-outlined transition-transform group-hover:translate-x-1">arrow_forward</span>
            </button>
          </div>

          <div class="relative group/image">
            <div class="absolute -inset-2 bg-gradient-to-r from-primary to-indigo-600 rounded-3xl opacity-20 blur-2xl group-hover/image:opacity-30 transition-opacity"></div>
            <div class="relative bg-slate-100 dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800">
              <img
                src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop"
                alt="Live monitoring dashboard"
                class="w-full h-auto rounded-xl shadow-2xl object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Automated Workflows Feature Section -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="relative group/image order-2 lg:order-1">
            <div class="absolute -inset-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-3xl opacity-20 blur-2xl group-hover/image:opacity-30 transition-opacity"></div>
            <div class="relative bg-slate-100 dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800">
              <img
                src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop"
                alt="Workflow builder interface"
                class="w-full h-auto rounded-xl shadow-2xl object-cover"
              />
            </div>
          </div>

          <div class="flex flex-col gap-6 order-1 lg:order-2">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 dark:bg-emerald-500/20 border border-emerald-500/20 dark:border-emerald-500/30 w-fit">
              <span class="text-sm font-bold text-emerald-600 dark:text-emerald-400">Automated Workflows</span>
            </div>

            <h2 class="text-4xl md:text-5xl font-black text-slate-900 dark:text-white leading-tight">
              <span class="bg-gradient-to-r from-emerald-500 to-teal-500 bg-clip-text text-transparent">Automate</span> & Elevate
            </h2>

            <p class="text-lg text-slate-600 dark:text-slate-400 leading-relaxed">
              Go beyond simple Q&A. Build sophisticated workflows that can schedule appointments, process payments, update customer records, and trigger actions in other systems. Free your team to focus on high-value tasks while the voice agent handles the routine work.
            </p>

            <ul class="space-y-4">
              <li class="flex items-start gap-3">
                <span class="material-symbols-outlined text-emerald-500 text-2xl flex-shrink-0 mt-0.5">check_circle</span>
                <div>
                  <p class="font-bold text-slate-900 dark:text-white">Appointment Scheduling</p>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Automatically book and manage appointments</p>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <span class="material-symbols-outlined text-emerald-500 text-2xl flex-shrink-0 mt-0.5">check_circle</span>
                <div>
                  <p class="font-bold text-slate-900 dark:text-white">Payment Processing</p>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Securely handle transactions within calls</p>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <span class="material-symbols-outlined text-emerald-500 text-2xl flex-shrink-0 mt-0.5">check_circle</span>
                <div>
                  <p class="font-bold text-slate-900 dark:text-white">System Integrations</p>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Trigger actions across your tech stack</p>
                </div>
              </li>
            </ul>

            <button class="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 text-lg font-bold group w-fit">
              <span>Explore workflow possibilities</span>
              <span class="material-symbols-outlined transition-transform group-hover:translate-x-1">arrow_forward</span>
            </button>
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
              Ready to Build Your Perfect Voice Agent?
            </h2>
            <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Experience the power and flexibility of our platform firsthand. Start your free trial today and see how easy it is to automate your conversations.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
              <router-link to="/login" class="px-8 py-4 text-lg font-bold text-primary bg-white rounded-xl hover:shadow-2xl hover:scale-105 transition-all">
                Start Free Trial
              </router-link>
              <button class="px-8 py-4 text-lg font-bold text-white border-2 border-white rounded-xl hover:bg-white/10 transition-all">
                Talk to Sales
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
              <div class="flex items-center justify-center size-10 rounded-xl bg-gradient-to-br from-primary to-indigo-600 text-white font-black text-xl shadow-lg shadow-primary/30">
                AI
              </div>
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
// No reactive state needed for this page
</script>
