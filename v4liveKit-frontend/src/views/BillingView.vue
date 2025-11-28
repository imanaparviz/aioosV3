<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="mx-auto max-w-7xl p-6 lg:p-8">
        <!-- Page Header -->
        <header class="sticky top-0 backdrop-blur-sm z-10 py-4 mb-8">
          <h1 class="text-4xl font-black leading-tight tracking-[-0.033em] text-slate-900 dark:text-white">
            Billing & Subscriptions
          </h1>
          <p class="mt-2 text-slate-600 dark:text-slate-400">
            Manage your plan, payment methods, and view your billing history.
          </p>
        </header>

        <!-- Two Column Layout -->
        <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
          <!-- Left Column (2/3 width) -->
          <div class="flex flex-col gap-8 lg:col-span-2">
            <!-- Current Plan Card -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 backdrop-blur-md dark:bg-slate-900/80">
              <div class="border-b border-slate-200 dark:border-slate-800 p-6">
                <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Current Plan</h2>
                <p class="text-sm text-slate-500 dark:text-slate-400">You are currently on the Pro Plan.</p>
              </div>
              <div class="p-6">
                <div class="flex flex-col gap-6 md:flex-row md:items-start md:justify-between">
                  <div>
                    <p class="text-4xl font-bold text-slate-900 dark:text-white">
                      ${{ currentPlan.price }}<span class="text-base font-medium text-slate-500 dark:text-slate-400">/month</span>
                    </p>
                    <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
                      Your next bill is on {{ currentPlan.nextBill }}.
                    </p>
                  </div>
                  <div class="flex flex-wrap gap-2">
                    <button
                      @click="handleChangePlan"
                      class="flex h-10 items-center justify-center gap-2 rounded-full border border-slate-300 dark:border-slate-700 bg-transparent px-4 text-sm font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
                    >
                      Change Plan
                    </button>
                    <button
                      @click="handleUpgrade"
                      class="flex h-10 items-center justify-center rounded-full bg-primary px-4 text-sm font-bold text-white hover:bg-primary/90"
                    >
                      Upgrade
                    </button>
                  </div>
                </div>

                <!-- Plan Features -->
                <div class="mt-6 border-t border-slate-200 dark:border-slate-800 pt-6">
                  <h3 class="font-semibold text-slate-800 dark:text-white">Plan features include:</h3>
                  <ul class="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <li v-for="feature in currentPlan.features" :key="feature" class="flex items-center gap-3">
                      <span class="material-symbols-outlined text-green-500" style="font-variation-settings: 'FILL' 1;">
                        check_circle
                      </span>
                      <span class="text-sm text-slate-600 dark:text-slate-300">{{ feature }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 p-4 text-center">
                <a
                  @click.prevent="handleCancelSubscription"
                  class="text-sm font-medium text-red-600 dark:text-red-500 hover:underline cursor-pointer"
                  href="#"
                >
                  Cancel Subscription
                </a>
              </div>
            </div>

            <!-- Billing History Card -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 backdrop-blur-md dark:bg-slate-900/80">
              <div class="border-b border-slate-200 dark:border-slate-800 p-6">
                <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Billing History</h2>
                <p class="text-sm text-slate-500 dark:text-slate-400">Download your past invoices.</p>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                  <thead>
                    <tr class="bg-slate-50/80 backdrop-blur-md dark:bg-slate-800/50 text-slate-600 dark:text-slate-300">
                      <th class="p-4 font-medium">Date</th>
                      <th class="p-4 font-medium">Description</th>
                      <th class="p-4 font-medium">Amount</th>
                      <th class="p-4 font-medium"></th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
                    <tr v-for="invoice in billingHistory" :key="invoice.id">
                      <td class="p-4 text-slate-600 dark:text-slate-300">{{ invoice.date }}</td>
                      <td class="p-4 font-medium text-slate-800 dark:text-white">{{ invoice.description }}</td>
                      <td class="p-4 text-slate-600 dark:text-slate-300">${{ invoice.amount }}</td>
                      <td class="p-4 text-right">
                        <button
                          @click="handleDownloadInvoice(invoice)"
                          class="flex items-center gap-2 text-sm font-medium text-primary hover:underline"
                        >
                          <span class="material-symbols-outlined text-base">download</span>
                          <span>Invoice</span>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Right Column (1/3 width) -->
          <div class="flex flex-col gap-8">
            <!-- Payment Method Card -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 backdrop-blur-md dark:bg-slate-900/80">
              <div class="border-b border-slate-200 dark:border-slate-800 p-6">
                <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Payment Method</h2>
              </div>
              <div class="p-6">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <!-- Card Icon -->
                    <div class="flex h-10 w-16 items-center justify-center rounded bg-slate-100 dark:bg-slate-800">
                      <span class="text-xs font-bold text-slate-600 dark:text-slate-300">VISA</span>
                    </div>
                    <div>
                      <p class="font-medium text-slate-800 dark:text-white">
                        {{ paymentMethod.type }} ending in {{ paymentMethod.last4 }}
                      </p>
                      <p class="text-sm text-slate-500 dark:text-slate-400">
                        Expires {{ paymentMethod.expiry }}
                      </p>
                    </div>
                  </div>
                  <button
                    @click="handleEditPayment"
                    class="text-sm font-medium text-primary hover:underline"
                  >
                    Edit
                  </button>
                </div>
                <button
                  @click="handleAddPayment"
                  class="mt-4 flex w-full h-10 items-center justify-center gap-2 rounded-full border border-slate-300 dark:border-slate-700 bg-transparent text-sm font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
                >
                  <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">add</span>
                  <span>Add New Method</span>
                </button>
              </div>
            </div>

            <!-- Usage This Month Card -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 backdrop-blur-md dark:bg-slate-900/80">
              <div class="border-b border-slate-200 dark:border-slate-800 p-6">
                <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Usage This Month</h2>
              </div>
              <div class="flex flex-col gap-6 p-6">
                <div v-for="usage in usageData" :key="usage.label">
                  <div class="flex justify-between text-sm">
                    <span class="font-medium text-slate-700 dark:text-slate-200">{{ usage.label }}</span>
                    <span class="text-slate-500 dark:text-slate-400">{{ usage.used }} / {{ usage.total }} Used</span>
                  </div>
                  <div class="mt-2 h-2 w-full rounded-full bg-slate-200 dark:bg-slate-700">
                    <div
                      class="h-2 rounded-full bg-primary"
                      :style="{ width: usage.percentage + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Need Help Card -->
            <div class="rounded-xl bg-slate-100/80 backdrop-blur-md dark:bg-slate-800/50 p-6">
              <div class="flex items-center gap-4">
                <div class="flex size-12 items-center justify-center rounded-full bg-white dark:bg-slate-700 text-primary">
                  <span class="material-symbols-outlined">quiz</span>
                </div>
                <div>
                  <h3 class="font-semibold text-slate-900 dark:text-white">Need Help?</h3>
                  <a
                    @click.prevent="handleBillingFAQ"
                    class="text-sm font-medium text-primary hover:underline cursor-pointer"
                    href="#"
                  >
                    Check our billing FAQs
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'

const router = useRouter()

// Current Plan Data
const currentPlan = ref({
  name: 'Pro Plan',
  price: 49,
  nextBill: 'June 23, 2024',
  features: [
    '10 Voice Agents',
    '50,000 API calls/month',
    'Advanced Analytics',
    'Email & Chat Support'
  ]
})

// Billing History
const billingHistory = ref([
  { id: 1, date: 'May 23, 2024', description: 'Pro Plan - Monthly', amount: '49.00' },
  { id: 2, date: 'April 23, 2024', description: 'Pro Plan - Monthly', amount: '49.00' },
  { id: 3, date: 'March 23, 2024', description: 'Pro Plan - Monthly', amount: '49.00' }
])

// Payment Method
const paymentMethod = ref({
  type: 'Visa',
  last4: '1234',
  expiry: '06/2026'
})

// Usage Data
const usageData = ref([
  { label: 'Voice Agents', used: 7, total: 10, percentage: 70 },
  { label: 'API Calls', used: '34,120', total: '50,000', percentage: 68 }
])

// Methods
const handleChangePlan = () => {
  alert('Change Plan\n\nAvailable plans:\n- Basic: $19/month\n- Pro: $49/month (Current)\n- Enterprise: $99/month\n\nThis would show a plan selection modal.')
}

const handleUpgrade = () => {
  alert('Upgrade to Enterprise\n\nEnterprise Plan includes:\n- Unlimited Voice Agents\n- 500,000 API calls/month\n- Priority Support\n- Custom Integrations\n\nPrice: $99/month\n\nThis would show upgrade confirmation.')
}

const handleCancelSubscription = () => {
  if (confirm('Are you sure you want to cancel your subscription?\n\nYou will lose access to Pro features at the end of your billing cycle.')) {
    alert('Subscription Cancelled\n\nYour subscription has been cancelled. You will continue to have access until June 23, 2024.')
  }
}

const handleDownloadInvoice = (invoice) => {
  console.log('Downloading invoice:', invoice)
  alert(`Download Invoice\n\nDate: ${invoice.date}\nAmount: $${invoice.amount}\n\nThis would download a PDF invoice.`)
}

const handleEditPayment = () => {
  alert('Edit Payment Method\n\nThis would open a secure form to update your payment information.')
}

const handleAddPayment = () => {
  alert('Add Payment Method\n\nThis would open a secure form to add a new credit card or payment method.')
}

const handleBillingFAQ = () => {
  router.push('/help')
}
</script>
