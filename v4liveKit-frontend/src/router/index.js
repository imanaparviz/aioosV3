import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('@/views/LandingView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('@/views/SignupView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/pricing',
      name: 'pricing',
      component: () => import('@/views/PricingView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/solutions',
      name: 'solutions',
      component: () => import('@/views/SolutionsView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/features',
      name: 'features',
      component: () => import('@/views/FeaturesView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/agents/create',
      name: 'create-agent',
      component: () => import('@/views/CreateAgentView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/agents/configure',
      name: 'configure-agent',
      component: () => import('@/views/ConfigureAgentView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/agents/phone',
      name: 'agent-phone',
      component: () => import('@/views/PhoneNumberView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/agents/test/widget',
      name: 'agent-test',
      component: () => import('@/views/AgentTestView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/agents/:id',
      name: 'agent-detail',
      component: () => import('@/views/AgentDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('@/views/AnalyticsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/call-logs',
      name: 'call-logs',
      component: () => import('@/views/CallLogsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: () => import('@/views/CalendarView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/knowledge',
      name: 'knowledge',
      component: () => import('@/views/KnowledgeBaseView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/call-logs/:id',
      name: 'call-detail',
      component: () => import('@/views/CallDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/webhooks',
      name: 'webhooks',
      component: () => import('@/views/WebhooksView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('@/views/HelpView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('@/views/UserManagementView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/billing',
      name: 'billing',
      component: () => import('@/views/BillingView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/phone-numbers',
      name: 'phone-numbers',
      component: () => import('@/views/PhoneNumbersManagementView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/teams',
      name: 'teams',
      component: () => import('@/views/TeamManagementView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/audit-log',
      name: 'audit-log',
      component: () => import('@/views/AuditLogView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/product-search',
      name: 'product-search',
      component: () => import('@/views/ProductSearchView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

// Navigation guard baraye check kardane authentication
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth

  if (requiresAuth && !authStore.isAuthenticated) {
    // Agar route niaz be auth dare va user login nakarde, befreste be login
    next('/login')
  } else if (!requiresAuth && authStore.isAuthenticated && (to.name === 'login' || to.name === 'signup' || to.name === 'landing')) {
    // Agar user login karde va mikhad bere login/signup/landing, befreste be dashboard
    next('/dashboard')
  } else {
    next()
  }
})

export default router
