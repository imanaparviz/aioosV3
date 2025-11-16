/**
 * AIOOS Platform API Client
 * Axios-based client bara communicate ba FastAPI backend
 */

import axios from 'axios'

// Backend API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance ba default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 seconds
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor - bara ezafe kardane auth token
apiClient.interceptors.request.use(
  (config) => {
    // Get auth token az localStorage
    const authSession = localStorage.getItem('auth-session')
    if (authSession) {
      try {
        const session = JSON.parse(authSession)
        if (session.access_token) {
          config.headers.Authorization = `Bearer ${session.access_token}`
        }
      } catch (error) {
        console.error('Failed to parse auth session:', error)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - bara handle kardane errors
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      // Server responded ba error
      console.error('API Error:', error.response.status, error.response.data)

      // Age 401 Unauthorized bood, logout kon
      if (error.response.status === 401) {
        localStorage.removeItem('auth-session')
        window.location.href = '/login'
      }
    } else if (error.request) {
      // Request send shod vali response nayomad
      console.error('No response from server:', error.request)
    } else {
      // Error to request setup
      console.error('Request error:', error.message)
    }
    return Promise.reject(error)
  }
)

// ==================== API Methods ====================

/**
 * Health Check - check kardane backend status
 */
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/api/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}

/**
 * Search Products - search kardane products
 * @param {string} query - Search query
 * @param {number} maxResults - Maximum number of results (default: 10)
 */
export const searchProducts = async (query, maxResults = 10) => {
  try {
    const response = await apiClient.post('/api/search', {
      query,
      max_results: maxResults
    })
    return response.data
  } catch (error) {
    console.error('Product search failed:', error)
    throw error
  }
}

/**
 * Get Agents - gereftan e list e agents
 */
export const getAgents = async () => {
  try {
    const response = await apiClient.get('/api/agents')
    return response.data
  } catch (error) {
    console.error('Failed to fetch agents:', error)
    throw error
  }
}

/**
 * Get Agent by ID - gereftan e yek agent ba ID
 * @param {string} agentId - Agent ID
 */
export const getAgentById = async (agentId) => {
  try {
    const response = await apiClient.get(`/api/agents/${agentId}`)
    return response.data
  } catch (error) {
    console.error(`Failed to fetch agent ${agentId}:`, error)
    throw error
  }
}

/**
 * Create Agent - sakhtane agent e jadid
 * @param {object} agentData - Agent configuration
 * @example
 * createAgent({
 *   name: "Customer Support Bot",
 *   description: "24/7 customer support agent",
 *   language: "en",
 *   llm_model: "gpt-4o-mini",
 *   temperature: 0.7,
 *   system_instructions: "You are a helpful customer support agent..."
 * })
 */
export const createAgent = async (agentData) => {
  try {
    const response = await apiClient.post('/api/agents', agentData)
    return response.data
  } catch (error) {
    console.error('Failed to create agent:', error)
    throw error
  }
}

/**
 * Update Agent - update kardane agent
 * @param {string} agentId - Agent ID
 * @param {object} agentData - Agent configuration
 */
export const updateAgent = async (agentId, agentData) => {
  try {
    const response = await apiClient.put(`/api/agents/${agentId}`, agentData)
    return response.data
  } catch (error) {
    console.error(`Failed to update agent ${agentId}:`, error)
    throw error
  }
}

/**
 * Delete Agent - hazf kardane agent
 * @param {string} agentId - Agent ID
 */
export const deleteAgent = async (agentId) => {
  try {
    const response = await apiClient.delete(`/api/agents/${agentId}`)
    return response.data
  } catch (error) {
    console.error(`Failed to delete agent ${agentId}:`, error)
    throw error
  }
}

/**
 * Get Call Logs - gereftan e call logs
 * @param {object} filters - Optional filters (agent_id, date_from, date_to)
 */
export const getCallLogs = async (filters = {}) => {
  try {
    const response = await apiClient.get('/api/calls', { params: filters })
    return response.data
  } catch (error) {
    console.error('Failed to fetch call logs:', error)
    throw error
  }
}

/**
 * Get Call by ID - gereftan e yek call log ba ID
 * @param {string} callId - Call ID
 */
export const getCallById = async (callId) => {
  try {
    const response = await apiClient.get(`/api/calls/${callId}`)
    return response.data
  } catch (error) {
    console.error(`Failed to fetch call ${callId}:`, error)
    throw error
  }
}

/**
 * Get Platform Stats - gereftan e platform statistics
 */
export const getStats = async () => {
  try {
    const response = await apiClient.get('/api/stats')
    return response.data
  } catch (error) {
    console.error('Failed to fetch stats:', error)
    throw error
  }
}

/**
 * Get Calendar Events - gereftan e calendar events az Supabase
 */
export const getCalendarEvents = async (startDate, endDate) => {
  try {
    const params = {
      start_date: startDate,
      end_date: endDate
    }
    const response = await apiClient.get('/api/calendar/events', { params })
    return response.data
  } catch (error) {
    console.error('Failed to fetch calendar events:', error)
    throw error
  }
}

/**
 * Create Calendar Event - sakhtane event jadid
 */
export const createCalendarEvent = async (eventData) => {
  try {
    const response = await apiClient.post('/api/calendar/events', eventData)
    return response.data
  } catch (error) {
    console.error('Failed to create calendar event:', error)
    throw error
  }
}

// Export default client ham bara advanced usage
export default apiClient
