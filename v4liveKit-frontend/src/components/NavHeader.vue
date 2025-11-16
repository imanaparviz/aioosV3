<template>
  <header class="sticky top-0 z-10 w-full bg-container-light/80 dark:bg-container-dark/80 backdrop-blur-sm border-b border-border-light dark:border-border-dark">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo & Brand -->
        <div class="flex items-center gap-4">
          <div class="size-6 text-primary-blue">
            <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M24 45.8096C19.6865 45.8096 15.4698 44.5305 11.8832 42.134C8.29667 39.7376 5.50128 36.3314 3.85056 32.3462C2.19985 28.361 1.76794 23.9758 2.60947 19.7452C3.451 15.5145 5.52816 11.6284 8.57829 8.5783C11.6284 5.52817 15.5145 3.45101 19.7452 2.60948C23.9758 1.76795 28.361 2.19986 32.3462 3.85057C36.3314 5.50129 39.7376 8.29668 42.134 11.8833C44.5305 15.4698 45.8096 19.6865 45.8096 24L24 24L24 45.8096Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <h2 class="text-xl font-bold leading-tight tracking-tight text-text-dark dark:text-white">
            Voice Agents
          </h2>
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
