<template>
  <header class="sticky top-0 z-10 w-full bg-container-light/80 dark:bg-container-dark/80 backdrop-blur-sm border-b border-border-light dark:border-border-dark">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo & Brand -->
        <div class="flex items-center gap-3">
          <router-link to="/" class="flex items-center gap-3 group">
            <img src="/logo-medium.png" alt="AIOOS" class="w-10 h-10 object-contain group-hover:scale-105 transition-transform" />
            <span class="text-xl font-bold text-slate-900 dark:text-white">AIOOS</span>
          </router-link>
        </div>

        <!-- Navigation Links -->
        <div class="flex items-center gap-6">
          <router-link
            to="/dashboard"
            class="text-sm font-medium text-secondary-gray hover:text-primary-blue dark:text-gray-300 dark:hover:text-primary"
            :class="{ 'font-bold !text-primary-blue dark:!text-primary': $route.path === '/dashboard' }"
          >
            Dashboard
          </router-link>
          <router-link
            to="/agents/create"
            class="text-sm font-medium text-secondary-gray hover:text-primary-blue dark:text-gray-300 dark:hover:text-primary"
            :class="{ 'font-bold !text-primary-blue dark:!text-primary': $route.path.includes('/agents') }"
          >
            Agents
          </router-link>
          <a
            href="#"
            class="text-sm font-medium text-secondary-gray hover:text-primary-blue dark:text-gray-300 dark:hover:text-primary"
          >
            Analytics
          </a>
          <a
            href="#"
            class="text-sm font-medium text-secondary-gray hover:text-primary-blue dark:text-gray-300 dark:hover:text-primary"
          >
            Settings
          </a>

          <!-- User Profile -->
          <div
            class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10 cursor-pointer hover:ring-2 hover:ring-primary-blue transition-all"
            style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDNfPA8tMUXDq2V1sMQDW-miZWMMjIcieHScO4qVUPpFYJLpZl-NockzICT2v61TuQnRPoez6efgKSbQaHFHR18Ip_495EsBrZ_tfjyRoKIVFpbj0C2eQI6D9pbicualFanitP3Wo3yqti8IyMs2HvA5dGd2g9Zw-5B62vAt4i8DMRTu6UZjzUcKNgXC9ylCLh_yNsZJ7dJnV2NPVcWnARn-z49wHwxg7zVIKyWcil4MYfNAzwsk8DL3NPXFFsuev4J1nBrrlXoGzTA");'
          ></div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
// No props needed - pure navigation component
</script>
