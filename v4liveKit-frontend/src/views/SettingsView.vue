<template>
  <div class="flex min-h-screen w-full">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-6 lg:p-10">
      <div class="mx-auto max-w-4xl">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white">Settings</h1>
          <p class="mt-1 text-gray-600 dark:text-gray-400">Manage your account and application preferences.</p>
        </div>

        <div class="flex flex-col gap-12">
          <!-- Profile Section -->
          <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div class="md:col-span-1">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Profile</h2>
              <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Update your personal information.</p>
            </div>
            <div class="md:col-span-2">
              <div class="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900/50">
                <div class="space-y-6">
                  <!-- Avatar -->
                  <div class="flex items-center gap-4">
                    <img
                      :src="profileData.avatar"
                      alt="User avatar"
                      class="h-16 w-16 rounded-full object-cover"
                    />
                    <div>
                      <button
                        @click="handleChangeAvatar"
                        class="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                      >
                        Change
                      </button>
                      <button
                        @click="handleRemoveAvatar"
                        class="ml-2 text-sm font-medium text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                      >
                        Remove
                      </button>
                    </div>
                  </div>

                  <!-- Name Fields -->
                  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300" for="first-name">
                        First Name
                      </label>
                      <input
                        v-model="profileData.firstName"
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white sm:text-sm"
                        id="first-name"
                        type="text"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300" for="last-name">
                        Last Name
                      </label>
                      <input
                        v-model="profileData.lastName"
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white sm:text-sm"
                        id="last-name"
                        type="text"
                      />
                    </div>
                  </div>

                  <!-- Email -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300" for="email">
                      Email Address
                    </label>
                    <input
                      v-model="profileData.email"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white sm:text-sm"
                      id="email"
                      type="email"
                    />
                  </div>

                  <!-- Save Button -->
                  <div class="flex justify-end">
                    <button
                      @click="handleSaveProfile"
                      class="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 dark:ring-offset-background-dark"
                    >
                      Save Changes
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Divider -->
          <div class="border-t border-gray-200 dark:border-gray-800"></div>

          <!-- Password Section -->
          <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div class="md:col-span-1">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Password</h2>
              <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Change your password here.</p>
            </div>
            <div class="md:col-span-2">
              <div class="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900/50">
                <div class="space-y-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300" for="current-password">
                      Current Password
                    </label>
                    <input
                      v-model="passwordData.current"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white sm:text-sm"
                      id="current-password"
                      type="password"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300" for="new-password">
                      New Password
                    </label>
                    <input
                      v-model="passwordData.new"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white sm:text-sm"
                      id="new-password"
                      type="password"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300" for="confirm-password">
                      Confirm New Password
                    </label>
                    <input
                      v-model="passwordData.confirm"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:border-gray-700 dark:bg-gray-800 dark:text-white sm:text-sm"
                      id="confirm-password"
                      type="password"
                    />
                  </div>
                  <div class="flex justify-end">
                    <button
                      @click="handleUpdatePassword"
                      class="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 dark:ring-offset-background-dark"
                    >
                      Update Password
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Divider -->
          <div class="border-t border-gray-200 dark:border-gray-800"></div>

          <!-- Billing Section -->
          <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div class="md:col-span-1">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Billing</h2>
              <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Manage your subscription and payment details.</p>
            </div>
            <div class="md:col-span-2">
              <div class="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900/50">
                <div class="space-y-6">
                  <!-- Current Plan -->
                  <div>
                    <h3 class="font-medium text-gray-900 dark:text-white">Current Plan</h3>
                    <div class="mt-2 flex items-center justify-between rounded-md border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-800/50">
                      <div>
                        <p class="font-semibold text-primary">{{ billingData.plan }}</p>
                        <p class="text-sm text-gray-600 dark:text-gray-400">
                          ${{ billingData.price }}/month. Renews on {{ billingData.renewalDate }}.
                        </p>
                      </div>
                      <button
                        @click="handleChangePlan"
                        class="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                      >
                        Change Plan
                      </button>
                    </div>
                  </div>

                  <!-- Payment Method -->
                  <div>
                    <h3 class="font-medium text-gray-900 dark:text-white">Payment Method</h3>
                    <div class="mt-2 flex items-center justify-between rounded-md border border-gray-200 p-4 dark:border-gray-700">
                      <div class="flex items-center gap-3">
                        <!-- Card Icon -->
                        <svg class="h-8 w-8" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                          <rect fill="#E0E0E0" height="46" rx="4" width="46" x="1" y="1"></rect>
                          <path d="M12 18H16V30H12V18Z" fill="#212121"></path>
                          <path d="M20 18H24V30H20V18Z" fill="#212121"></path>
                          <path d="M28 18H32V30H28V18Z" fill="#212121"></path>
                          <path d="M36 18H40V30H36V18Z" fill="#212121"></path>
                        </svg>
                        <div>
                          <p class="font-medium text-gray-900 dark:text-white">{{ billingData.cardType }} ending in {{ billingData.cardLast4 }}</p>
                          <p class="text-sm text-gray-600 dark:text-gray-400">Expires {{ billingData.cardExpiry }}</p>
                        </div>
                      </div>
                      <button
                        @click="handleUpdatePayment"
                        class="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                      >
                        Update
                      </button>
                    </div>
                  </div>

                  <!-- Billing History Link -->
                  <div>
                    <a
                      @click.prevent="handleViewBillingHistory"
                      class="text-sm font-medium text-primary hover:text-primary-hover cursor-pointer"
                      href="#"
                    >
                      View billing history
                    </a>
                  </div>
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
import { useAuthStore } from '@/stores/auth'
import SidebarNav from '@/components/SidebarNav.vue'

const authStore = useAuthStore()

// Profile Data
const profileData = ref({
  avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuB5iBmk619yvbBy4U_T6g2JvsWACMJZhYXFMCTKgvVfmbngm0ewNfaiNwVyAvfCRjwGwHuKxDIgkDbK0LHTsIPofiMezA-Cmo_E3ztiE7-GWPgBmxse7E39igGAjbWnZy6BMTLd7RE6Avb6ALxlaGdvkf_7miy7wus53pCcDwNO562-lErPUSOVeePIyVNGuQF8iMmd7tUMA2DW0EPvnSfHSwaxILXnRuSVogG0KRB2tZ8CTt0A450JTWCNjR4wPh0v2Xyehdipmz7k',
  firstName: 'Olivia',
  lastName: 'Martin',
  email: 'olivia.martin@example.com'
})

// Password Data
const passwordData = ref({
  current: '',
  new: '',
  confirm: ''
})

// Billing Data
const billingData = ref({
  plan: 'Pro Plan',
  price: 99,
  renewalDate: 'Nov 26, 2023',
  cardType: 'Visa',
  cardLast4: '1234',
  cardExpiry: '06/2025'
})

// Methods
const handleChangeAvatar = () => {
  alert('Change Avatar\n\nThis would open a file picker to upload a new avatar image.')
}

const handleRemoveAvatar = () => {
  if (confirm('Are you sure you want to remove your avatar?')) {
    alert('Avatar removed successfully!')
  }
}

const handleSaveProfile = () => {
  console.log('Saving profile:', profileData.value)
  alert('Profile Updated!\n\nYour profile information has been saved successfully.')
}

const handleUpdatePassword = () => {
  if (!passwordData.value.current) {
    alert('Error!\n\nPlease enter your current password.')
    return
  }
  if (!passwordData.value.new) {
    alert('Error!\n\nPlease enter a new password.')
    return
  }
  if (passwordData.value.new !== passwordData.value.confirm) {
    alert('Error!\n\nNew passwords do not match.')
    return
  }
  if (passwordData.value.new.length < 8) {
    alert('Error!\n\nPassword must be at least 8 characters long.')
    return
  }

  console.log('Updating password')
  alert('Password Updated!\n\nYour password has been changed successfully.')

  // Clear form
  passwordData.value = {
    current: '',
    new: '',
    confirm: ''
  }
}

const handleChangePlan = () => {
  alert('Change Plan\n\nAvailable Plans:\n- Basic: $29/month\n- Pro: $99/month (Current)\n- Enterprise: $299/month\n\nThis would open a plan selection dialog.')
}

const handleUpdatePayment = () => {
  alert('Update Payment Method\n\nThis would open a secure payment form to update your credit card information.')
}

const handleViewBillingHistory = () => {
  alert('Billing History\n\nThis would show a detailed list of all past invoices and payments.')
}
</script>
