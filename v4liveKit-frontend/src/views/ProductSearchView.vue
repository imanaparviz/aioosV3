<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">
            Product Search
          </h1>
          <p class="text-slate-600 dark:text-slate-400">
            Test the backend product search engine (1429 Swedish products)
          </p>
        </div>

        <!-- Search Box -->
        <div class="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6 mb-8">
          <form @submit.prevent="handleSearch" class="flex gap-4">
            <div class="flex-1">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search for products (e.g., bacon, kyckling, mozzarella)..."
                class="w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary"
                :disabled="searching"
              />
            </div>
            <button
              type="submit"
              :disabled="!searchQuery.trim() || searching"
              class="flex items-center gap-2 px-6 py-3 bg-primary hover:bg-primary/90 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span class="material-symbols-outlined">search</span>
              <span>{{ searching ? 'Searching...' : 'Search' }}</span>
            </button>
          </form>

          <!-- Max Results Slider -->
          <div class="mt-4">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">
              Max Results: {{ maxResults }}
            </label>
            <input
              v-model.number="maxResults"
              type="range"
              min="1"
              max="20"
              class="w-full mt-2"
            />
          </div>
        </div>

        <!-- Search Results -->
        <div v-if="searchResults" class="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
          <!-- Results Header -->
          <div class="flex items-center justify-between mb-6 pb-4 border-b border-slate-200 dark:border-slate-700">
            <div>
              <h2 class="text-xl font-bold text-slate-900 dark:text-white">
                Search Results
              </h2>
              <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">
                Found {{ searchResults.total_count }} products in {{ searchResults.search_time_ms.toFixed(2) }}ms
              </p>
            </div>
            <div class="px-3 py-1 bg-primary/10 text-primary text-sm font-medium rounded-full">
              Strategy: {{ searchResults.strategy_used }}
            </div>
          </div>

          <!-- Results Grid -->
          <div v-if="searchResults.results.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="product in searchResults.results"
              :key="product.id"
              class="border border-slate-200 dark:border-slate-700 rounded-lg p-4 hover:shadow-lg transition-shadow"
            >
              <!-- Product Header -->
              <div class="flex items-start justify-between mb-3">
                <h3 class="font-semibold text-slate-900 dark:text-white text-sm flex-1">
                  {{ product.name }}
                </h3>
                <span
                  v-if="product.in_stock"
                  class="ml-2 px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-xs font-medium rounded"
                >
                  In Stock
                </span>
                <span
                  v-else
                  class="ml-2 px-2 py-0.5 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-xs font-medium rounded"
                >
                  Out of Stock
                </span>
              </div>

              <!-- Product Details -->
              <div class="space-y-2 text-sm">
                <div class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <span class="material-symbols-outlined text-lg">business</span>
                  <span>{{ product.company }}</span>
                </div>

                <div v-if="product.category" class="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                  <span class="material-symbols-outlined text-lg">category</span>
                  <span>{{ product.category }}</span>
                </div>

                <div v-if="product.price" class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-lg text-primary">attach_money</span>
                  <span class="font-bold text-lg text-primary">{{ product.price }} SEK</span>
                </div>
              </div>
            </div>
          </div>

          <!-- No Results -->
          <div v-else class="text-center py-12">
            <span class="material-symbols-outlined text-6xl text-slate-400 dark:text-slate-600 mb-4">search_off</span>
            <p class="text-slate-600 dark:text-slate-400">
              No products found for "{{ searchResults.query }}"
            </p>
          </div>
        </div>

        <!-- Error State -->
        <div v-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-red-600 dark:text-red-400">error</span>
            <div>
              <h3 class="font-semibold text-red-900 dark:text-red-100">Search Error</h3>
              <p class="text-sm text-red-700 dark:text-red-300 mt-1">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!searchResults && !error" class="text-center py-20">
          <div class="inline-flex items-center justify-center bg-primary/10 text-primary w-20 h-20 rounded-full mb-6">
            <span class="material-symbols-outlined" style="font-size: 48px;">search</span>
          </div>
          <h2 class="text-2xl font-bold text-slate-800 dark:text-white">Ready to search</h2>
          <p class="text-slate-600 dark:text-slate-400 mt-2">
            Enter a search query above to find products from the Swedish database.
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SidebarNav from '@/components/SidebarNav.vue'
import { searchProducts } from '@/services/api'

// State
const searchQuery = ref('')
const maxResults = ref(10)
const searching = ref(false)
const searchResults = ref(null)
const error = ref(null)

// Handle search
const handleSearch = async () => {
  if (!searchQuery.value.trim()) return

  searching.value = true
  error.value = null
  searchResults.value = null

  try {
    console.log('🔍 Searching for:', searchQuery.value)
    const results = await searchProducts(searchQuery.value, maxResults.value)
    console.log('✅ Search results:', results)
    searchResults.value = results
  } catch (err) {
    console.error('❌ Search failed:', err)
    error.value = 'Failed to search products. Please check if backend is running on http://localhost:8000'
  } finally {
    searching.value = false
  }
}
</script>
