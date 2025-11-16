import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { supabase } from '@/lib/supabase'

// DEV MODE: Set be true baraye mock authentication (bedone Supabase)
// IMPORTANT: Set to FALSE for production to use real Supabase authentication!
const DEV_MODE = false

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const session = ref(null)
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!session.value)
  const currentUser = computed(() => user.value)

  // Actions
  async function signup(name, email, password) {
    loading.value = true
    try {
      // 1. Aval user ro to SupabaseAuth besaz
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: name
          }
        }
      })

      if (authError) throw authError

      // 2. Set user va session
      if (authData.user) {
        user.value = {
          id: authData.user.id,
          email: authData.user.email,
          name: name
        }
        session.value = authData.session

        // Save session to localStorage bara API client
        if (authData.session) {
          localStorage.setItem('auth-session', JSON.stringify(authData.session))
        }
      }

      return { success: true, user: authData.user }
    } catch (error) {
      console.error('Signup error:', error)
      throw new Error(error.message || 'Failed to create account')
    } finally {
      loading.value = false
    }
  }

  async function login(email, password) {
    loading.value = true
    try {
      // DEV MODE: Mock authentication
      if (DEV_MODE) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500))

        user.value = {
          id: 'dev-user-123',
          email: email,
          name: 'Admin User'
        }
        session.value = {
          access_token: 'dev-token-' + Date.now(),
          user: user.value
        }

        // Save to localStorage
        localStorage.setItem('auth-session', JSON.stringify(session.value))

        return { success: true, user: user.value }
      }

      // PRODUCTION: Supabase authentication
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      })

      if (error) throw error

      // Set user va session
      if (data.user) {
        user.value = {
          id: data.user.id,
          email: data.user.email,
          name: data.user.user_metadata?.full_name || data.user.email
        }
        session.value = data.session

        // Save session to localStorage bara API client
        localStorage.setItem('auth-session', JSON.stringify(data.session))
      }

      return { success: true, user: data.user }
    } catch (error) {
      console.error('Login error:', error)
      throw new Error(error.message || 'Invalid email or password')
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    try {
      // DEV MODE: Mock logout
      if (DEV_MODE) {
        localStorage.removeItem('auth-session')
        user.value = null
        session.value = null
        return
      }

      // PRODUCTION: Supabase logout
      const { error } = await supabase.auth.signOut()
      if (error) throw error

      // Clear localStorage
      localStorage.removeItem('auth-session')

      user.value = null
      session.value = null
    } catch (error) {
      console.error('Logout error:', error)
      throw new Error(error.message || 'Failed to logout')
    } finally {
      loading.value = false
    }
  }

  async function initAuth() {
    // DEV MODE: Check localStorage baraye session
    if (DEV_MODE) {
      const savedSession = localStorage.getItem('auth-session')
      if (savedSession) {
        try {
          session.value = JSON.parse(savedSession)
          user.value = session.value.user
        } catch (error) {
          console.error('Failed to parse saved session:', error)
          localStorage.removeItem('auth-session')
        }
      }
      return
    }

    // PRODUCTION: Check Supabase session
    const { data: { session: currentSession } } = await supabase.auth.getSession()

    if (currentSession) {
      session.value = currentSession
      user.value = {
        id: currentSession.user.id,
        email: currentSession.user.email,
        name: currentSession.user.user_metadata?.full_name || currentSession.user.email
      }

      // Save to localStorage bara API client
      localStorage.setItem('auth-session', JSON.stringify(currentSession))
    }

    // Listen be auth changes (login, logout, etc)
    supabase.auth.onAuthStateChange((_event, newSession) => {
      session.value = newSession

      if (newSession?.user) {
        user.value = {
          id: newSession.user.id,
          email: newSession.user.email,
          name: newSession.user.user_metadata?.full_name || newSession.user.email
        }

        // Save to localStorage bara API client
        localStorage.setItem('auth-session', JSON.stringify(newSession))
      } else {
        user.value = null
        localStorage.removeItem('auth-session')
      }
    })
  }

  return {
    user,
    session,
    loading,
    isAuthenticated,
    currentUser,
    login,
    signup,
    logout,
    initAuth
  }
})
