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
            <router-link to="/solutions" class="text-sm font-medium text-primary dark:text-primary">
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
            Industry Solutions
          </span>
        </div>

        <h1 class="text-5xl sm:text-6xl lg:text-7xl font-black leading-tight mb-6">
          <span class="bg-gradient-to-r from-slate-900 via-primary to-indigo-600 dark:from-white dark:via-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
            Tailored Solutions
          </span>
          <br />
          <span class="text-slate-800 dark:text-white">For Your Industry</span>
        </h1>

        <p class="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
          Discover how our AI voice agents can transform your business operations, no matter the sector.
        </p>
      </div>
    </section>

    <!-- Search & Filter Section -->
    <section class="pb-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="relative">
          <div class="absolute -inset-2 bg-gradient-to-r from-primary/20 via-indigo-500/20 to-purple-500/20 rounded-2xl blur-xl"></div>
          <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-200 dark:border-slate-800">
            <div class="flex items-center gap-3 mb-6">
              <img src="/logo-medium.png" alt="AIOOS" class="w-10 h-10 object-contain" />
              <span class="text-2xl font-black bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">
                AIOOS
              </span>
            </div>
            <div class="flex flex-col md:flex-row gap-4">
              <!-- Search Input -->
              <div class="relative flex-1">
                <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                  search
                </span>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search solutions (e.g., 'healthcare', 'e-commerce')"
                  class="w-full h-12 pl-12 pr-4 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 focus:ring-2 focus:ring-primary focus:border-primary transition-all text-slate-900 dark:text-white placeholder:text-slate-400"
                />
              </div>

              <!-- Industry Filter -->
              <div class="relative w-full md:w-64">
                <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                  category
                </span>
                <select
                  v-model="selectedIndustry"
                  class="w-full h-12 pl-12 pr-10 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 focus:ring-2 focus:ring-primary focus:border-primary transition-all text-slate-900 dark:text-white appearance-none cursor-pointer"
                >
                  <option value="all">All Industries</option>
                  <option value="ecommerce">E-commerce</option>
                  <option value="healthcare">Healthcare</option>
                  <option value="finance">Finance</option>
                  <option value="realestate">Real Estate</option>
                  <option value="travel">Travel</option>
                  <option value="general">General</option>
                </select>
                <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                  expand_more
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Solutions Grid -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- E-commerce -->
          <div v-if="filteredSolutions.includes('ecommerce')" class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-blue-300/50 dark:hover:shadow-blue-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center gap-4 mb-6">
                <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 text-white shadow-lg">
                  <span class="material-symbols-outlined text-3xl">shopping_cart</span>
                </div>
                <h3 class="text-2xl font-bold text-slate-900 dark:text-white">E-commerce</h3>
              </div>

              <p class="text-slate-600 dark:text-slate-400 mb-6 flex-grow">
                Automate order tracking, process returns, and provide 24/7 customer support to boost sales and customer loyalty.
              </p>

              <ul class="space-y-3 mb-6">
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-blue-500 text-lg">check_circle</span>
                  Order tracking automation
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-blue-500 text-lg">check_circle</span>
                  Return & refund processing
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-blue-500 text-lg">check_circle</span>
                  24/7 customer support
                </li>
              </ul>

              <button class="flex items-center justify-center gap-2 w-full py-3 px-6 rounded-xl font-bold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950 hover:bg-blue-100 dark:hover:bg-blue-900 transition-all group/btn">
                <span>Learn More</span>
                <span class="material-symbols-outlined transition-transform group-hover/btn:translate-x-1">arrow_forward</span>
              </button>
            </div>
          </div>

          <!-- Healthcare -->
          <div v-if="filteredSolutions.includes('healthcare')" class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-emerald-300/50 dark:hover:shadow-emerald-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center gap-4 mb-6">
                <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 text-white shadow-lg">
                  <span class="material-symbols-outlined text-3xl">medical_services</span>
                </div>
                <h3 class="text-2xl font-bold text-slate-900 dark:text-white">Healthcare</h3>
              </div>

              <p class="text-slate-600 dark:text-slate-400 mb-6 flex-grow">
                Streamline appointment booking, send reminders, and answer patient FAQs, freeing up staff for critical tasks.
              </p>

              <ul class="space-y-3 mb-6">
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-emerald-500 text-lg">check_circle</span>
                  Appointment scheduling
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-emerald-500 text-lg">check_circle</span>
                  Automated reminders
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-emerald-500 text-lg">check_circle</span>
                  Patient FAQ support
                </li>
              </ul>

              <button class="flex items-center justify-center gap-2 w-full py-3 px-6 rounded-xl font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950 hover:bg-emerald-100 dark:hover:bg-emerald-900 transition-all group/btn">
                <span>Learn More</span>
                <span class="material-symbols-outlined transition-transform group-hover/btn:translate-x-1">arrow_forward</span>
              </button>
            </div>
          </div>

          <!-- Finance & Banking -->
          <div v-if="filteredSolutions.includes('finance')" class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-amber-300/50 dark:hover:shadow-amber-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center gap-4 mb-6">
                <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 text-white shadow-lg">
                  <span class="material-symbols-outlined text-3xl">account_balance</span>
                </div>
                <h3 class="text-2xl font-bold text-slate-900 dark:text-white">Finance & Banking</h3>
              </div>

              <p class="text-slate-600 dark:text-slate-400 mb-6 flex-grow">
                Provide instant support for balance inquiries, fraud alerts, and loan applications with secure, compliant voice agents.
              </p>

              <ul class="space-y-3 mb-6">
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-amber-500 text-lg">check_circle</span>
                  Balance inquiries
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-amber-500 text-lg">check_circle</span>
                  Fraud alerts & security
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-amber-500 text-lg">check_circle</span>
                  Loan applications
                </li>
              </ul>

              <button class="flex items-center justify-center gap-2 w-full py-3 px-6 rounded-xl font-bold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950 hover:bg-amber-100 dark:hover:bg-amber-900 transition-all group/btn">
                <span>Learn More</span>
                <span class="material-symbols-outlined transition-transform group-hover/btn:translate-x-1">arrow_forward</span>
              </button>
            </div>
          </div>

          <!-- Real Estate -->
          <div v-if="filteredSolutions.includes('realestate')" class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-purple-300/50 dark:hover:shadow-purple-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center gap-4 mb-6">
                <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 text-white shadow-lg">
                  <span class="material-symbols-outlined text-3xl">real_estate_agent</span>
                </div>
                <h3 class="text-2xl font-bold text-slate-900 dark:text-white">Real Estate</h3>
              </div>

              <p class="text-slate-600 dark:text-slate-400 mb-6 flex-grow">
                Qualify leads, schedule property viewings, and answer client questions around the clock, ensuring you never miss an opportunity.
              </p>

              <ul class="space-y-3 mb-6">
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-purple-500 text-lg">check_circle</span>
                  Lead qualification
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-purple-500 text-lg">check_circle</span>
                  Property viewing scheduling
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-purple-500 text-lg">check_circle</span>
                  24/7 client support
                </li>
              </ul>

              <button class="flex items-center justify-center gap-2 w-full py-3 px-6 rounded-xl font-bold text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-950 hover:bg-purple-100 dark:hover:bg-purple-900 transition-all group/btn">
                <span>Learn More</span>
                <span class="material-symbols-outlined transition-transform group-hover/btn:translate-x-1">arrow_forward</span>
              </button>
            </div>
          </div>

          <!-- Travel & Hospitality -->
          <div v-if="filteredSolutions.includes('travel')" class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-rose-500/20 to-red-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-rose-300/50 dark:hover:shadow-rose-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center gap-4 mb-6">
                <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-rose-500 to-red-500 text-white shadow-lg">
                  <span class="material-symbols-outlined text-3xl">flight</span>
                </div>
                <h3 class="text-2xl font-bold text-slate-900 dark:text-white">Travel & Hospitality</h3>
              </div>

              <p class="text-slate-600 dark:text-slate-400 mb-6 flex-grow">
                Handle bookings, check-ins, and travel inquiries effortlessly, providing a seamless experience for your guests.
              </p>

              <ul class="space-y-3 mb-6">
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-rose-500 text-lg">check_circle</span>
                  Booking automation
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-rose-500 text-lg">check_circle</span>
                  Check-in assistance
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-rose-500 text-lg">check_circle</span>
                  Travel inquiry support
                </li>
              </ul>

              <button class="flex items-center justify-center gap-2 w-full py-3 px-6 rounded-xl font-bold text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950 hover:bg-rose-100 dark:hover:bg-rose-900 transition-all group/btn">
                <span>Learn More</span>
                <span class="material-symbols-outlined transition-transform group-hover/btn:translate-x-1">arrow_forward</span>
              </button>
            </div>
          </div>

          <!-- General Customer Service -->
          <div v-if="filteredSolutions.includes('general')" class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-500/20 to-violet-500/20 rounded-3xl opacity-0 group-hover:opacity-100 blur transition-opacity duration-500"></div>
            <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 border border-slate-200 dark:border-slate-800 hover:shadow-2xl hover:shadow-indigo-300/50 dark:hover:shadow-indigo-900/50 transition-all duration-500 h-full flex flex-col">
              <div class="flex items-center gap-4 mb-6">
                <div class="flex items-center justify-center size-14 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 text-white shadow-lg">
                  <span class="material-symbols-outlined text-3xl">support_agent</span>
                </div>
                <h3 class="text-2xl font-bold text-slate-900 dark:text-white">General Customer Service</h3>
              </div>

              <p class="text-slate-600 dark:text-slate-400 mb-6 flex-grow">
                Deploy versatile agents for any industry to handle FAQs, route calls, and collect feedback, improving overall service efficiency.
              </p>

              <ul class="space-y-3 mb-6">
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-indigo-500 text-lg">check_circle</span>
                  FAQ handling
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-indigo-500 text-lg">check_circle</span>
                  Intelligent call routing
                </li>
                <li class="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                  <span class="material-symbols-outlined text-indigo-500 text-lg">check_circle</span>
                  Feedback collection
                </li>
              </ul>

              <button class="flex items-center justify-center gap-2 w-full py-3 px-6 rounded-xl font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950 hover:bg-indigo-100 dark:hover:bg-indigo-900 transition-all group/btn">
                <span>Learn More</span>
                <span class="material-symbols-outlined transition-transform group-hover/btn:translate-x-1">arrow_forward</span>
              </button>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div v-if="filteredSolutions.length === 0" class="text-center py-16">
          <span class="material-symbols-outlined text-6xl text-slate-300 dark:text-slate-700 mb-4">search_off</span>
          <p class="text-xl font-semibold text-slate-600 dark:text-slate-400">No solutions found</p>
          <p class="text-slate-500 dark:text-slate-500 mt-2">Try adjusting your search or filter criteria</p>
        </div>
      </div>
    </section>

    <!-- Testimonial Section -->
    <section class="pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-5xl mx-auto">
        <div class="relative">
          <div class="absolute -inset-1 bg-gradient-to-r from-primary to-indigo-600 rounded-3xl blur-xl opacity-20"></div>
          <div class="relative bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl p-8 md:p-12 border border-slate-200 dark:border-slate-800">
            <div class="flex flex-col lg:flex-row items-center gap-8 lg:gap-12">
              <div class="flex-shrink-0">
                <div class="relative">
                  <div class="absolute -inset-2 bg-gradient-to-br from-primary to-indigo-600 rounded-full opacity-20 blur"></div>
                  <img
                    src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=faces"
                    alt="John Doe"
                    class="relative w-32 h-32 rounded-full object-cover shadow-xl ring-4 ring-white dark:ring-slate-900"
                  />
                </div>
              </div>
              <div class="text-center lg:text-left flex-1">
                <!-- Quote Icon -->
                <svg class="size-10 text-primary/20 mb-4 mx-auto lg:mx-0" fill="currentColor" viewBox="0 0 32 32">
                  <path d="M10 8c-3.3 0-6 2.7-6 6v10h10V14H8c0-1.1.9-2 2-2h2V8h-2zm12 0c-3.3 0-6 2.7-6 6v10h10V14h-6c0-1.1.9-2 2-2h2V8h-2z"/>
                </svg>

                <p class="text-slate-900 dark:text-slate-50 text-2xl font-bold leading-snug mb-6">
                  "Implementing AIOOS revolutionized our customer support. We've cut response times by 80% and our customers have never been happier."
                </p>

                <div class="flex flex-col gap-2">
                  <p class="text-lg font-bold text-slate-900 dark:text-white">John Doe</p>
                  <p class="text-slate-600 dark:text-slate-400 font-medium">CEO, E-commerce Giant</p>
                  <p class="text-sm text-primary font-bold mt-2">
                    Case Study: How E-commerce Giant Boosted CSAT by 40%
                  </p>
                </div>
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
              Ready to Transform Your Business?
            </h2>
            <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Explore our solutions and see how easy it is to get started with AI voice automation.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
              <router-link to="/login" class="px-8 py-4 text-lg font-bold text-primary bg-white rounded-xl hover:shadow-2xl hover:scale-105 transition-all">
                Request a Demo
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
import { ref, computed } from 'vue'

const searchQuery = ref('')
const selectedIndustry = ref('all')

const allSolutions = ['ecommerce', 'healthcare', 'finance', 'realestate', 'travel', 'general']

const filteredSolutions = computed(() => {
  let solutions = allSolutions

  // Filter by industry
  if (selectedIndustry.value !== 'all') {
    solutions = solutions.filter(s => s === selectedIndustry.value)
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    solutions = solutions.filter(solution => {
      const keywords = {
        ecommerce: ['ecommerce', 'e-commerce', 'shop', 'retail', 'order', 'cart'],
        healthcare: ['healthcare', 'health', 'medical', 'hospital', 'patient', 'doctor'],
        finance: ['finance', 'bank', 'banking', 'loan', 'money', 'payment'],
        realestate: ['real estate', 'realestate', 'property', 'house', 'apartment'],
        travel: ['travel', 'hotel', 'hospitality', 'booking', 'flight'],
        general: ['general', 'customer service', 'support', 'help']
      }
      return keywords[solution].some(keyword => keyword.includes(query))
    })
  }

  return solutions
})
</script>
