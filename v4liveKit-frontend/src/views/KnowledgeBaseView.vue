<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="flex flex-wrap justify-between items-center gap-4 mb-8">
          <div>
            <h1 class="text-slate-900 dark:text-white text-3xl font-bold tracking-tight">
              Knowledge Base
            </h1>
            <p class="text-slate-500 dark:text-slate-400 mt-1">
              Manage files that your voice agents use for information.
            </p>
          </div>
          <button
            @click="$refs.fileInput.click()"
            :disabled="!selectedAgentId"
            class="flex h-10 items-center justify-center gap-2 rounded-lg bg-primary px-4 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="material-symbols-outlined" style="font-size: 20px;">upload_file</span>
            <span>Upload Files</span>
          </button>
        </header>

        <!-- Agent Selector -->
        <div class="mb-6">
          <div class="relative max-w-md">
            <select
              v-model="selectedAgentId"
              @change="onAgentChange"
              class="appearance-none w-full h-12 px-4 pr-10 border border-slate-300 dark:border-slate-700 rounded-lg text-base font-medium text-slate-900 dark:text-white bg-white dark:bg-slate-900/50 hover:bg-slate-50 dark:hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
              <option :value="null">Select an agent...</option>
              <option v-for="agent in availableAgents" :key="agent.id" :value="agent.id">
                {{ agent.name }}
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-500 dark:text-slate-400">
              <span class="material-symbols-outlined text-xl">expand_more</span>
            </div>
          </div>
        </div>

        <!-- File Upload Zone -->
        <div
          v-if="selectedAgentId"
          class="border-2 border-dashed rounded-xl p-8 text-center mb-8 cursor-pointer transition-colors"
          :class="{
            'border-primary bg-primary/5': isDragging,
            'border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900/50 hover:border-primary dark:hover:border-primary': !isDragging
          }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="$refs.fileInput.click()"
        >
          <div class="flex justify-center items-center">
            <div class="flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
              <span class="material-symbols-outlined text-3xl text-slate-500 dark:text-slate-400">cloud_upload</span>
            </div>
          </div>
          <p class="mt-4 text-lg font-semibold text-slate-900 dark:text-white">
            Drag & drop files here or click to browse
          </p>
          <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Supports: TXT, CSV, PDF, DOCX, XLSX (max 10MB)
          </p>
          <input
            ref="fileInput"
            type="file"
            class="hidden"
            accept=".txt,.csv,.pdf,.xlsx,.docx"
            multiple
            @change="handleFileSelect"
          />
        </div>

        <!-- Search and Filter Bar -->
        <div v-if="selectedAgentId && (knowledgeFiles.length > 0 || uploadingFiles.length > 0)" class="flex flex-wrap justify-between items-center gap-4 mb-6">
          <div class="relative flex-grow max-w-lg">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500">search</span>
            <input
              v-model="searchQuery"
              class="w-full h-10 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900/50 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="Search files by name..."
              type="text"
            />
          </div>
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <label class="text-sm text-slate-500 dark:text-slate-400" for="sort">Sort by:</label>
              <select
                v-model="sortBy"
                class="h-10 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900/50 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                id="sort"
              >
                <option value="date">Upload Date</option>
                <option value="name">Name</option>
                <option value="size">Size</option>
              </select>
            </div>
            <div class="flex items-center text-slate-500 dark:text-slate-400">
              <button
                @click="viewMode = 'grid'"
                class="p-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800"
                :class="{ 'bg-slate-100 dark:bg-slate-800 text-primary': viewMode === 'grid' }"
              >
                <span class="material-symbols-outlined">grid_view</span>
              </button>
              <button
                @click="viewMode = 'list'"
                class="p-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800"
                :class="{ 'bg-slate-100 dark:bg-slate-800 text-primary': viewMode === 'list' }"
              >
                <span class="material-symbols-outlined">list</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Uploaded Files List -->
        <div v-if="selectedAgentId && filteredFiles.length > 0">
          <div class="grid grid-cols-1 gap-5">
            <!-- File Cards -->
            <div
              v-for="file in filteredFiles"
              :key="file.id"
              class="bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm hover:shadow-md transition-shadow"
            >
              <div class="flex flex-col sm:flex-row gap-4">
                <div class="flex items-center gap-4">
                  <div
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg"
                    :class="getFileIconClass(file.file_type)"
                  >
                    <span class="material-symbols-outlined" :class="getFileIconColor(file.file_type)">
                      {{ getFileIcon(file.file_type) }}
                    </span>
                  </div>
                  <div>
                    <p class="font-semibold text-slate-900 dark:text-white">{{ file.file_name }}</p>
                    <p class="text-sm text-slate-500 dark:text-slate-400">
                      {{ formatFileSize(file.file_size_bytes) }} • Uploaded: {{ formatDate(file.created_at) }}
                    </p>
                  </div>
                </div>
                <div class="flex-grow">
                  <p class="text-sm text-slate-600 dark:text-slate-300 line-clamp-2">
                    {{ file.content_preview || 'Document content preview...' }}
                  </p>
                </div>
                <div class="flex flex-col sm:items-end shrink-0 gap-2">
                  <div class="flex items-center gap-2">
                    <span
                      class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                      :class="getStatusBadgeClass(file)"
                    >
                      {{ getStatusText(file) }}
                    </span>
                    <p class="text-sm text-slate-500 dark:text-slate-400">{{ file.total_chunks }} chunks</p>
                  </div>
                  <div class="flex items-center gap-2 mt-1">
                    <button
                      class="p-1.5 text-slate-500 dark:text-slate-400 hover:text-red-500 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800"
                      @click="handleDelete(file.id)"
                      title="Delete file"
                    >
                      <span class="material-symbols-outlined" style="font-size: 18px;">delete</span>
                    </button>
                  </div>
                </div>
              </div>
              <!-- Progress Bar for Processing Files -->
              <div
                v-if="file.processing"
                class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1 mt-3"
              >
                <div
                  class="bg-gradient-to-r from-blue-400 to-purple-500 h-1 rounded-full"
                  :style="{ width: (file.progress || 75) + '%' }"
                ></div>
              </div>
            </div>

            <!-- Uploading Files -->
            <div
              v-for="file in uploadingFiles"
              :key="'uploading-' + file.name"
              class="bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm"
            >
              <div class="flex flex-col sm:flex-row gap-4">
                <div class="flex items-center gap-4">
                  <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/50">
                    <span class="material-symbols-outlined text-blue-600 dark:text-blue-400">upload_file</span>
                  </div>
                  <div>
                    <p class="font-semibold text-slate-900 dark:text-white">{{ file.name }}</p>
                    <p class="text-sm text-slate-500 dark:text-slate-400">
                      {{ formatFileSize(file.size) }} • Uploading...
                    </p>
                  </div>
                </div>
                <div class="flex-grow"></div>
                <div class="flex flex-col sm:items-end shrink-0 gap-2">
                  <span class="inline-flex items-center rounded-full bg-yellow-100 dark:bg-yellow-900/50 px-2.5 py-0.5 text-xs font-medium text-yellow-800 dark:text-yellow-300">
                    Uploading
                  </span>
                </div>
              </div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1 mt-3">
                <div
                  class="bg-gradient-to-r from-blue-400 to-purple-500 h-1 rounded-full transition-all duration-300"
                  :style="{ width: file.progress + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-if="selectedAgentId && knowledgeFiles.length === 0 && !loading"
          class="flex flex-col items-center justify-center py-16 text-center"
        >
          <span class="material-symbols-outlined text-8xl text-gray-300 dark:text-gray-700 mb-4">
            folder_open
          </span>
          <p class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            No documents uploaded yet
          </p>
          <p class="text-gray-500 dark:text-gray-400">
            Upload documents to enable knowledge-based answers for this agent
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-16">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import SidebarNav from '@/components/SidebarNav.vue'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

// State
const selectedAgentId = ref(null)
const availableAgents = ref([])
const knowledgeFiles = ref([])
const uploadingFiles = ref([])
const loading = ref(false)
const isDragging = ref(false)
const fileInput = ref(null)
const searchQuery = ref('')
const sortBy = ref('date')
const viewMode = ref('list')

// Load agents on mount
onMounted(async () => {
  await loadAgents()
})

// Watch agent selection
watch(selectedAgentId, async (newAgentId) => {
  if (newAgentId) {
    await loadKnowledgeFiles()
  }
})

// Load agents
async function loadAgents() {
  try {
    const response = await apiClient.get('/api/agents')
    availableAgents.value = response.data
  } catch (error) {
    console.error('Failed to load agents:', error)
  }
}

// Load knowledge files for selected agent
async function loadKnowledgeFiles() {
  if (!selectedAgentId.value) return

  loading.value = true
  try {
    const response = await apiClient.get(`/api/knowledge/${selectedAgentId.value}`)
    knowledgeFiles.value = response.data
  } catch (error) {
    console.error('Failed to load knowledge files:', error)
  } finally {
    loading.value = false
  }
}

// Agent change handler
function onAgentChange() {
  knowledgeFiles.value = []
  if (selectedAgentId.value) {
    loadKnowledgeFiles()
  }
}

// Handle file drop
function handleDrop(event) {
  isDragging.value = false
  const files = Array.from(event.dataTransfer.files)
  uploadFiles(files)
}

// Handle file select
function handleFileSelect(event) {
  const files = Array.from(event.target.files)
  uploadFiles(files)
  // Reset input
  event.target.value = ''
}

// Upload files
async function uploadFiles(files) {
  if (!selectedAgentId.value) {
    alert('Please select an agent first')
    return
  }

  for (const file of files) {
    // Validate file type
    const allowedTypes = ['txt', 'csv', 'pdf', 'xlsx', 'docx']
    const extension = file.name.split('.').pop().toLowerCase()
    if (!allowedTypes.includes(extension)) {
      alert(`File type .${extension} is not supported`)
      continue
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      alert(`File ${file.name} is too large (max 10MB)`)
      continue
    }

    // Add to uploading list
    const uploadingFile = {
      name: file.name,
      size: file.size,
      progress: 0
    }
    uploadingFiles.value.push(uploadingFile)

    // Upload file
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('agent_id', selectedAgentId.value)

      // Simulate progress (in real app, use upload progress events)
      const progressInterval = setInterval(() => {
        if (uploadingFile.progress < 90) {
          uploadingFile.progress += 10
        }
      }, 200)

      const response = await apiClient.post('/api/knowledge/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      clearInterval(progressInterval)
      uploadingFile.progress = 100

      // Remove from uploading list after a delay
      setTimeout(() => {
        uploadingFiles.value = uploadingFiles.value.filter(f => f.name !== uploadingFile.name)
      }, 1000)

      // Reload knowledge files
      await loadKnowledgeFiles()

    } catch (error) {
      console.error('Upload failed:', error)
      alert(`Failed to upload ${file.name}: ${error.response?.data?.detail || error.message}`)
      uploadingFiles.value = uploadingFiles.value.filter(f => f.name !== uploadingFile.name)
    }
  }
}

// Delete file
async function handleDelete(fileId) {
  if (!confirm('Are you sure you want to delete this file?')) {
    return
  }

  try {
    await apiClient.delete(`/api/knowledge/${fileId}`)
    // Remove from list
    knowledgeFiles.value = knowledgeFiles.value.filter(f => f.id !== fileId)
  } catch (error) {
    console.error('Delete failed:', error)
    alert('Failed to delete file')
  }
}

// Format file size
function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + ' KB'
  return Math.round(bytes / (1024 * 1024)) + ' MB'
}

// Format date
function formatDate(dateString) {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(date)
}

// Filtered and sorted files
const filteredFiles = computed(() => {
  let files = [...knowledgeFiles.value]

  // Apply search filter
  if (searchQuery.value) {
    files = files.filter(file =>
      file.file_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Apply sorting
  files.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.file_name.localeCompare(b.file_name)
      case 'size':
        return (b.file_size_bytes || 0) - (a.file_size_bytes || 0)
      case 'date':
      default:
        return new Date(b.created_at) - new Date(a.created_at)
    }
  })

  return files
})

// Get file icon based on type
function getFileIcon(fileType) {
  const icons = {
    'pdf': 'picture_as_pdf',
    'docx': 'description',
    'doc': 'description',
    'txt': 'description',
    'csv': 'table_chart',
    'xlsx': 'table_chart',
    'xls': 'table_chart'
  }
  return icons[fileType?.toLowerCase()] || 'description'
}

// Get file icon background class
function getFileIconClass(fileType) {
  const classes = {
    'pdf': 'bg-red-100 dark:bg-red-900/50',
    'docx': 'bg-blue-100 dark:bg-blue-900/50',
    'doc': 'bg-blue-100 dark:bg-blue-900/50',
    'txt': 'bg-green-100 dark:bg-green-900/50',
    'csv': 'bg-purple-100 dark:bg-purple-900/50',
    'xlsx': 'bg-purple-100 dark:bg-purple-900/50',
    'xls': 'bg-purple-100 dark:bg-purple-900/50'
  }
  return classes[fileType?.toLowerCase()] || 'bg-slate-100 dark:bg-slate-800'
}

// Get file icon color class
function getFileIconColor(fileType) {
  const colors = {
    'pdf': 'text-red-600 dark:text-red-400',
    'docx': 'text-blue-600 dark:text-blue-400',
    'doc': 'text-blue-600 dark:text-blue-400',
    'txt': 'text-green-600 dark:text-green-400',
    'csv': 'text-purple-600 dark:text-purple-400',
    'xlsx': 'text-purple-600 dark:text-purple-400',
    'xls': 'text-purple-600 dark:text-purple-400'
  }
  return colors[fileType?.toLowerCase()] || 'text-slate-600 dark:text-slate-400'
}

// Get status badge class
function getStatusBadgeClass(file) {
  if (file.processing) {
    return 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300'
  }
  if (file.total_chunks > 0) {
    return 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300'
  }
  return 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300'
}

// Get status text
function getStatusText(file) {
  if (file.processing) return 'Processing'
  if (file.total_chunks > 0) return 'Completed'
  return 'Failed'
}
</script>
