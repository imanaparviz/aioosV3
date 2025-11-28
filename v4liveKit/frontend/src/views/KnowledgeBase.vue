<template>
  <div class="font-display bg-background-light dark:bg-background-dark text-slate-800 dark:text-slate-200 min-h-screen">
    <main class="flex-1 p-8 overflow-y-auto">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="flex flex-wrap justify-between items-center gap-4 mb-8">
          <div>
            <h1 class="text-slate-900 dark:text-white text-3xl font-bold tracking-tight">Knowledge Base</h1>
            <p class="text-slate-500 dark:text-slate-400 mt-1">Manage files that your voice agents use for information.</p>
          </div>
          <button
            @click="openFilePicker"
            :disabled="!selectedAgentId"
            class="flex h-10 items-center justify-center gap-2 rounded-lg bg-primary px-4 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="material-symbols-outlined" style="font-size: 20px;">upload_file</span>
            <span>Upload Files</span>
          </button>
        </header>

        <!-- Agent Selector -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            Select Agent
          </label>
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

        <!-- Drag & Drop Zone -->
        <div
          v-if="selectedAgentId"
          @click="openFilePicker"
          @dragover.prevent="isDragging = true"
          @dragleave="isDragging = false"
          @drop.prevent="handleFileDrop"
          :class="[
            'border-2 border-dashed rounded-xl p-8 text-center bg-white dark:bg-slate-900/50 transition-colors cursor-pointer mb-8',
            isDragging ? 'border-primary dark:border-primary' : 'border-slate-300 dark:border-slate-700 hover:border-primary dark:hover:border-primary'
          ]"
        >
          <div class="flex justify-center items-center">
            <div class="flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
              <span class="material-symbols-outlined text-3xl text-slate-500 dark:text-slate-400">cloud_upload</span>
            </div>
          </div>
          <p class="mt-4 text-lg font-semibold text-slate-900 dark:text-white">Drag & drop files here or click to browse</p>
          <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">Supports: TXT, CSV, PDF, DOCX, XLSX (max 10MB)</p>
          <input
            ref="fileInput"
            type="file"
            multiple
            accept=".txt,.csv,.pdf,.docx,.xlsx"
            @change="handleFileSelect"
            style="display: none"
          />
        </div>

        <!-- Upload Progress -->
        <div v-if="uploadingFiles.length > 0" class="mb-8 space-y-3">
          <div
            v-for="file in uploadingFiles"
            :key="file.name"
            class="bg-white dark:bg-slate-900 rounded-lg p-4 border border-slate-200 dark:border-slate-700"
          >
            <div class="flex items-center gap-3 mb-2">
              <span class="material-symbols-outlined text-blue-500">description</span>
              <span class="font-medium flex-1">{{ file.name }}</span>
              <span class="text-sm text-slate-500">{{ file.progress }}%</span>
            </div>
            <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5">
              <div class="bg-gradient-to-r from-blue-400 to-purple-500 h-1.5 rounded-full transition-all" :style="{ width: file.progress + '%' }"></div>
            </div>
          </div>
        </div>

        <!-- Search and Filter -->
        <div v-if="selectedAgentId && (files.length > 0 || uploadingFiles.length > 0)" class="flex flex-wrap justify-between items-center gap-4 mb-6">
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
              <button class="p-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800">
                <span class="material-symbols-outlined">grid_view</span>
              </button>
              <button class="p-2 rounded-md bg-slate-100 dark:bg-slate-800 text-primary">
                <span class="material-symbols-outlined">list</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-16">
          <div class="w-12 h-12 mx-auto mb-4 border-3 border-slate-200 border-t-primary rounded-full animate-spin"></div>
          <p class="text-slate-600 dark:text-slate-400">Loading files...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="selectedAgentId && filteredFiles.length === 0 && uploadingFiles.length === 0" class="text-center py-16">
          <span class="material-symbols-outlined text-6xl text-slate-300 dark:text-slate-600 mb-4 block">folder_open</span>
          <p class="text-xl font-semibold text-slate-700 dark:text-slate-300 mb-2">No documents uploaded yet</p>
          <p class="text-slate-500 dark:text-slate-400">Upload your first document to get started.</p>
        </div>

        <!-- Files List -->
        <div v-else-if="selectedAgentId && (filteredFiles.length > 0 || uploadingFiles.length > 0)" class="grid grid-cols-1 gap-5">
          <div
            v-for="file in filteredFiles"
            :key="file.id"
            class="bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm hover:shadow-md transition-shadow"
          >
            <div class="flex flex-col sm:flex-row gap-4">
              <div class="flex items-center gap-4">
                <div :class="['flex h-10 w-10 shrink-0 items-center justify-center rounded-lg', getFileIconClass(file.file_type)]">
                  <span class="material-symbols-outlined">{{ getFileIcon(file.file_type) }}</span>
                </div>
                <div>
                  <p class="font-semibold text-slate-900 dark:text-white">{{ file.file_name }}</p>
                  <p class="text-sm text-slate-500 dark:text-slate-400">
                    {{ formatFileSize(file.file_size_bytes) }}・Uploaded: {{ formatDate(file.created_at) }}
                  </p>
                </div>
              </div>
              <div class="flex-grow">
                <p class="text-sm text-slate-600 dark:text-slate-300 line-clamp-2">
                  {{ file.content_preview || 'No preview available' }}
                </p>
              </div>
              <div class="flex flex-col sm:items-end shrink-0 gap-2">
                <div class="flex items-center gap-2">
                  <span :class="getStatusClass(file.upload_status)">
                    {{ file.upload_status.charAt(0).toUpperCase() + file.upload_status.slice(1) }}
                  </span>
                  <p class="text-sm text-slate-500 dark:text-slate-400">{{ file.total_chunks }} chunks</p>
                </div>
                <div class="flex items-center gap-2 mt-1">
                  <button
                    @click="confirmDelete(file)"
                    class="p-1.5 text-slate-500 dark:text-slate-400 hover:text-red-500 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800"
                  >
                    <span class="material-symbols-outlined" style="font-size: 18px;">delete</span>
                  </button>
                </div>
              </div>
            </div>
            <!-- Processing Progress Bar -->
            <div v-if="file.upload_status === 'processing'" class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1 mt-3 overflow-hidden">
              <div class="bg-gradient-to-r from-blue-400 to-purple-500 h-1 rounded-full animate-pulse" style="width: 75%"></div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Delete Confirmation Dialog -->
    <div
      v-if="showDeleteDialog"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click="showDeleteDialog = false"
    >
      <div class="bg-white dark:bg-slate-900 rounded-xl p-6 max-w-md w-full mx-4" @click.stop>
        <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-2">Delete File?</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-6">
          Are you sure you want to delete <strong>{{ fileToDelete?.file_name }}</strong>?
          This will also delete all associated chunks and cannot be undone.
        </p>
        <div class="flex gap-3 justify-end">
          <button
            @click="showDeleteDialog = false"
            class="px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg font-medium hover:bg-slate-50 dark:hover:bg-slate-800"
          >
            Cancel
          </button>
          <button
            @click="deleteFile"
            class="px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// State
const files = ref([])
const loading = ref(false)
const searchQuery = ref('')
const sortBy = ref('date')
const isDragging = ref(false)
const uploadingFiles = ref([])
const showDeleteDialog = ref(false)
const fileToDelete = ref(null)
const fileInput = ref(null)
const selectedAgentId = ref(null)
const availableAgents = ref([])

// Computed agentId - use selected or route param or default
const agentId = computed(() => selectedAgentId.value || route.params.agentId || null)

// Computed
const filteredFiles = computed(() => {
  let result = [...files.value]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(f => f.file_name.toLowerCase().includes(query))
  }

  // Sort
  result.sort((a, b) => {
    if (sortBy.value === 'date') {
      return new Date(b.created_at) - new Date(a.created_at)
    } else if (sortBy.value === 'name') {
      return a.file_name.localeCompare(b.file_name)
    } else if (sortBy.value === 'size') {
      return b.file_size_bytes - a.file_size_bytes
    }
    return 0
  })

  return result
})

// Methods
async function fetchAgents() {
  try {
    const response = await fetch('http://localhost:8000/api/agents')
    if (response.ok) {
      availableAgents.value = await response.json()
      // Auto-select first agent if none selected
      if (availableAgents.value.length > 0 && !selectedAgentId.value) {
        selectedAgentId.value = availableAgents.value[0].id
      }
    } else {
      console.error('Failed to fetch agents:', await response.text())
    }
  } catch (error) {
    console.error('Error fetching agents:', error)
  }
}

async function fetchFiles() {
  if (!agentId.value) {
    files.value = []
    return
  }

  loading.value = true
  try {
    const response = await fetch(`http://localhost:8000/api/knowledge/${agentId.value}`)
    if (response.ok) {
      files.value = await response.json()
    } else {
      console.error('Failed to fetch files:', await response.text())
    }
  } catch (error) {
    console.error('Error fetching files:', error)
  } finally {
    loading.value = false
  }
}

function onAgentChange() {
  files.value = []
  if (selectedAgentId.value) {
    fetchFiles()
  }
}

function openFilePicker() {
  fileInput.value?.click()
}

function handleFileSelect(event) {
  const selectedFiles = Array.from(event.target.files)
  uploadFiles(selectedFiles)
  event.target.value = ''
}

function handleFileDrop(event) {
  isDragging.value = false
  const droppedFiles = Array.from(event.dataTransfer.files)
  uploadFiles(droppedFiles)
}

async function uploadFiles(filesToUpload) {
  for (const file of filesToUpload) {
    // Validate file size
    if (file.size > 10 * 1024 * 1024) {
      alert(`File ${file.name} is too large. Maximum size is 10MB.`)
      continue
    }

    // Validate file type
    const validTypes = ['txt', 'csv', 'pdf', 'docx', 'xlsx']
    const extension = file.name.split('.').pop().toLowerCase()
    if (!validTypes.includes(extension)) {
      alert(`File ${file.name} has unsupported format.`)
      continue
    }

    // Add to uploading list
    const uploadItem = {
      name: file.name,
      progress: 0
    }
    uploadingFiles.value.push(uploadItem)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('agent_id', agentId.value)

      // Simulate progress
      const progressInterval = setInterval(() => {
        if (uploadItem.progress < 90) {
          uploadItem.progress += 10
        }
      }, 200)

      const response = await fetch('http://localhost:8000/api/knowledge/upload', {
        method: 'POST',
        body: formData
      })

      clearInterval(progressInterval)
      uploadItem.progress = 100

      if (response.ok) {
        setTimeout(() => {
          uploadingFiles.value = uploadingFiles.value.filter(f => f.name !== uploadItem.name)
        }, 1000)
        await fetchFiles()
      } else {
        const error = await response.text()
        alert(`Failed to upload ${file.name}: ${error}`)
        uploadingFiles.value = uploadingFiles.value.filter(f => f.name !== uploadItem.name)
      }
    } catch (error) {
      console.error('Upload error:', error)
      uploadingFiles.value = uploadingFiles.value.filter(f => f.name !== uploadItem.name)
    }
  }
}

function confirmDelete(file) {
  fileToDelete.value = file
  showDeleteDialog.value = true
}

async function deleteFile() {
  if (!fileToDelete.value) return

  try {
    const response = await fetch(`http://localhost:8000/api/knowledge/${fileToDelete.value.id}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      await fetchFiles()
    } else {
      console.error('Delete failed:', await response.text())
    }
  } catch (error) {
    console.error('Delete error:', error)
  } finally {
    showDeleteDialog.value = false
    fileToDelete.value = null
  }
}

// Utility functions
function getFileIcon(fileType) {
  const icons = {
    pdf: 'picture_as_pdf',
    docx: 'description',
    txt: 'description',
    csv: 'table_chart',
    xlsx: 'table_chart'
  }
  return icons[fileType] || 'description'
}

function getFileIconClass(fileType) {
  const classes = {
    pdf: 'bg-red-100 dark:bg-red-900/50 text-red-600 dark:text-red-400',
    docx: 'bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400',
    txt: 'bg-green-100 dark:bg-green-900/50 text-green-600 dark:text-green-400',
    csv: 'bg-purple-100 dark:bg-purple-900/50 text-purple-600 dark:text-purple-400',
    xlsx: 'bg-green-100 dark:bg-green-900/50 text-green-600 dark:text-green-400'
  }
  return classes[fileType] || 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'
}

function getStatusClass(status) {
  const classes = {
    completed: 'inline-flex items-center rounded-full bg-green-100 dark:bg-green-900/50 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:text-green-300',
    processing: 'inline-flex items-center rounded-full bg-yellow-100 dark:bg-yellow-900/50 px-2.5 py-0.5 text-xs font-medium text-yellow-800 dark:text-yellow-300',
    failed: 'inline-flex items-center rounded-full bg-red-100 dark:bg-red-900/50 px-2.5 py-0.5 text-xs font-medium text-red-800 dark:text-red-300'
  }
  return classes[status] || classes.processing
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// Lifecycle
onMounted(async () => {
  await fetchAgents()
  if (agentId.value) {
    await fetchFiles()
  }
})

// Watch for agent changes
watch(selectedAgentId, (newAgentId) => {
  if (newAgentId) {
    fetchFiles()
  }
})
</script>

<style scoped>
@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}
</style>
