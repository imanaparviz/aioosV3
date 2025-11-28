<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <SidebarNav />

    <!-- Main Content -->
    <main class="flex-1 p-6 lg:p-10 overflow-y-auto">
      <div class="flex flex-col h-full">
        <!-- Header -->
        <header class="sticky top-0 backdrop-blur-sm z-10 py-4 mb-6 flex flex-wrap items-center justify-between gap-4">
          <div class="flex flex-col gap-1">
            <h1 class="text-slate-900 dark:text-white text-3xl lg:text-4xl font-black leading-tight tracking-[-0.033em]">
              Team Management
            </h1>
            <p class="text-slate-600 dark:text-slate-400 text-base">
              Organize users into teams and manage agents.
            </p>
          </div>
          <button
            @click="handleCreateTeam"
            class="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90"
          >
            <span class="material-symbols-outlined !text-[18px]">add</span>
            <span>Create New Team</span>
          </button>
        </header>

        <!-- Search and Filter -->
        <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div class="relative w-full max-w-xs">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500">
              search
            </span>
            <input
              v-model="searchQuery"
              class="w-full h-10 pl-10 pr-4 border border-slate-200 dark:border-slate-800 rounded-lg bg-white/80 backdrop-blur-md dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-primary"
              placeholder="Search teams..."
              type="text"
            />
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="showFilterMenu = !showFilterMenu"
              class="px-4 py-2 text-sm font-medium rounded-lg text-slate-600 dark:text-slate-400 hover:bg-primary/10 hover:text-primary flex items-center gap-2"
            >
              <span>Filter</span>
              <span class="material-symbols-outlined text-base">filter_list</span>
            </button>
          </div>
        </div>

        <!-- Teams Table -->
        <div class="bg-white/80 backdrop-blur-md dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="bg-slate-50/80 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800">
                  <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400">Team Name</th>
                  <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400">Members</th>
                  <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400">Assigned Agents</th>
                  <th class="p-4 text-sm font-semibold text-slate-500 dark:text-slate-400 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="team in filteredTeams"
                  :key="team.id"
                  class="border-b border-slate-200 dark:border-slate-800 last:border-b-0 hover:bg-slate-50 dark:hover:bg-slate-800/30"
                >
                  <!-- Team Name & Description -->
                  <td class="p-4 align-top">
                    <p class="font-medium text-slate-900 dark:text-white">{{ team.name }}</p>
                    <p class="text-sm text-slate-600 dark:text-slate-400">{{ team.description }}</p>
                  </td>

                  <!-- Members -->
                  <td class="p-4 align-top">
                    <div class="flex -space-x-2">
                      <div
                        v-for="(member, index) in team.members.slice(0, 3)"
                        :key="index"
                        class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-8 ring-2 ring-white dark:ring-slate-900"
                        :style="`background-image: url('${member.avatar}');`"
                        :title="member.name"
                      ></div>
                      <div
                        v-if="team.members.length > 3"
                        class="flex items-center justify-center size-8 rounded-full bg-primary/10 text-primary text-xs font-medium ring-2 ring-white dark:ring-slate-900"
                      >
                        +{{ team.members.length - 3 }}
                      </div>
                    </div>
                  </td>

                  <!-- Assigned Agents -->
                  <td class="p-4 align-top">
                    <div class="flex flex-col gap-1">
                      <span
                        v-for="agent in team.assignedAgents"
                        :key="agent"
                        class="inline-flex items-center gap-2 px-2 py-1 text-sm font-medium rounded-md bg-primary/10 text-primary w-fit"
                      >
                        {{ agent }}
                      </span>
                    </div>
                  </td>

                  <!-- Actions -->
                  <td class="p-4 align-top">
                    <div class="flex justify-end gap-2">
                      <button
                        @click="handleViewTeam(team)"
                        class="flex items-center justify-center size-8 rounded-lg hover:bg-primary/10 text-slate-500 dark:text-slate-400 hover:text-primary"
                        title="View"
                      >
                        <span class="material-symbols-outlined text-xl">visibility</span>
                      </button>
                      <button
                        @click="handleEditTeam(team)"
                        class="flex items-center justify-center size-8 rounded-lg hover:bg-primary/10 text-slate-500 dark:text-slate-400 hover:text-primary"
                        title="Edit"
                      >
                        <span class="material-symbols-outlined text-xl">edit</span>
                      </button>
                      <button
                        @click="handleDeleteTeam(team)"
                        class="flex items-center justify-center size-8 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/10 text-slate-500 dark:text-slate-400 hover:text-red-600 dark:hover:text-red-400"
                        title="Delete"
                      >
                        <span class="material-symbols-outlined text-xl">delete</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Create Team Modal -->
        <div
          v-if="showCreateTeamModal"
          class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          @click.self="showCreateTeamModal = false"
        >
          <div class="bg-white dark:bg-slate-900 rounded-lg p-6 max-w-md w-full">
            <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-4">Create New Team</h3>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Team Name
                </label>
                <input
                  v-model="newTeam.name"
                  type="text"
                  placeholder="e.g., Sales Team Alpha"
                  class="w-full px-3 py-2 border border-slate-300 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Description
                </label>
                <textarea
                  v-model="newTeam.description"
                  rows="3"
                  placeholder="Describe the team's purpose..."
                  class="w-full px-3 py-2 border border-slate-300 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                ></textarea>
              </div>
            </div>

            <div class="flex gap-3 mt-6">
              <button
                @click="showCreateTeamModal = false"
                class="flex-1 px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
              >
                Cancel
              </button>
              <button
                @click="handleSaveNewTeam"
                class="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90"
              >
                Create Team
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import SidebarNav from '@/components/SidebarNav.vue'

const searchQuery = ref('')
const showFilterMenu = ref(false)
const showCreateTeamModal = ref(false)

const newTeam = ref({
  name: '',
  description: ''
})

// Mock teams data
const teams = ref([
  {
    id: 1,
    name: 'Sales Team Alpha',
    description: 'Handles all inbound sales inquiries.',
    members: [
      {
        name: 'John Doe',
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDZvZqTs0XbbQPhfuXsEtpg0RgbdK7vda6UaSIidcC52g7Icjqf_J7WcxBNgFgJ2QWLUkQmHR3apkqUNZVy9mFJO45cVtOTXXpfaFHUEsLa80vPk9wn2ySogsR0RC7RWCBNvGSVz-41Niqmc9kRlEOrXrIzQ3mTDc9sxG_Ppmk4Azqrsvx6s8rnG1LxPFpPkuVzUaRSLhfzx-BZkM2nxJyJMZBO1aYXgp9Dj4KQdBOv4JC_hxXQreTfQuT8i-c8N0_hA41n7NTqC6oU'
      },
      {
        name: 'Jane Smith',
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAbwhnkamiubIn5UYkQyj8m-cZ88KrwFmjW62ZGrKTIxFkBNC4gMf7ctx7l0P4FwHtXsmF08xuuV71PekShK6nx5U0RRv6mFIk8Dx1aovhmxCftK5Lw8spHo-HYtyAeKI6mfT4nS6qyk1STX7B4RKeMAV2Wp519iyr8A9s80Hne8OavbmUhBfq5YxzhDLRqvOF0GMsjHOQNpZclhZObJEDcE_maqcX2KsVKbU7DVw40j7KfvYwSwnJMYujG46E4gw6oMa2ig0byt3CO'
      },
      {
        name: 'Mike Johnson',
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBezwgNmOs5HFKLMN1GLXLf8HNIAEbepSSTqvESemyoztZ3OIM9ISbKSUEMdse-tKsCzPlGQyPK5rTpNFiiaxXPydf8Qdk20Sxo8iAJ3QZCs_NXTpG4MbsCL71Eb0eGYPv2fJcf7oa9_c89grLKY3jbc9FpLv9zuIctVFZoOLwQG3F-m4bDBAoviMIGiE_z5Dv7ltZI3AtOzdsKf2n3CTKOUB5bCXX8LgSxxxEhdevvN25YLMo3gF8sKu4CkBdHQz4tHEmWdKSpyGur'
      },
      { name: 'Sarah Williams', avatar: '' },
      { name: 'Tom Brown', avatar: '' },
      { name: 'Emily Davis', avatar: '' },
      { name: 'Chris Wilson', avatar: '' },
      { name: 'Lisa Anderson', avatar: '' }
    ],
    assignedAgents: ['Agent "Clara"', 'Agent "David"']
  },
  {
    id: 2,
    name: 'Support Team Bravo',
    description: 'Provides technical support and troubleshooting.',
    members: [
      {
        name: 'Robert Taylor',
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuABqGqFR63NmgXm_w1p3BZveFelDUFsg2ldsAlK4O-MzZhXg52URvXX_Yc7HiNiVxY45GjjRr19wiVTzb0YV-yQIt-F3QPMD5lUmdeuW1X-132KKZv2KWg44G5OVQgpVbEmfh8IAedrxYXZgqcmZuJmtHNe6Fdg6nUSP84-Ezms4xvG6XvIR582Dk4qwbtMq7maHL11bCWcjh5Dmsa80SmxlzXEZV797UanytKutyTogbS9odhr30kcGfv3wLe78N_7ILd5-SRCFPzu'
      },
      {
        name: 'Anna Martinez',
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD7en75rh7BadAklPSu-ymISepL5J9x02vQ8sAKsekyWDbTQt4DkimrRzm22X-bOxpaiz-GRA7dWLWtqWNGQiBZRvuYoBn4wWmQ2eGL5q77unADkNNT3iKGtazgV1wT2EjqM16KX5cAggR0ExqWe046-DHvgQCVicJm4n9Hu2EuRHt_7QsCV6N7W4xO5LtZmWA7IPJl5-SmUDZQoL-8IBg_i1B0YG1dSi5b4EG54PotkQ9Nu_t6s7tR0-dvN7qhSSMY9PGNCJ10-D3T'
      }
    ],
    assignedAgents: ['Agent "Echo"']
  },
  {
    id: 3,
    name: 'Customer Success',
    description: 'Onboarding and account management.',
    members: [
      {
        name: 'David Lee',
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCLN7Hz_UApXzRBc6-2x4hZDlHa12idQt4KKSx92dK4SlKqtrtefGAj98nJ50HWdN0qrWA1VACD6lLV9wTj7yg_H2E-UfuwogErcHyA9fcSp8tadnZconnapVLIZh6-ca4QXoIiy2zp0YBKBQY4QFuJ18ixyQR7JZYSUdoPZ_mJEkGibdpAzz9dfyM9HJWw6gAO26a7irN-wJRniFP0FhvVYAw_6kOfQaec9qeCqtd2CN9Qq8ulYjYSXL5bcKAn68_AwJJcGQWZ1iI1'
      },
      {
        name: 'Michelle Garcia',
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBIIpLbipoAGIXbcrIxuJZKzWVl7-7vnRcuAkoLQoKQKwcyE5py-TNs-AvgYhLqjmKwjTB6GsfSrHpxN5PCRly0k3zYxcfupYZwvGyoBK-QrjU0KL1M1cRiEqKbBgr5MHGLv7STsXOfK_qjw4fUIcvDtnTAm_XAINFA2M7q27FXNCDbGETRlWDuYd5l1qBuKsnlbTIh5SaOyT_Xiv0wAXfcak_jhnZ4g06OuVFChON1fkhywFqgm0c7p4Opq-uGv60dqW3gbsjEDTOj'
      },
      {
        name: 'Kevin Rodriguez',
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAr6gktWygT_s7xSgwPl8nhIy1Diixxpnu_1qU6FFRfF9l0nrPUXADdDImuoPLcXdwTPffaAuHG60bAE7cnfss4EYDfPZDXm9ydIqoOy0YxDjzgMgLxKHckd1tfxSyd4opOvmNLXpwDex5M5615PpeIQNz8WlNE56DKMdR3NyZQHkW6ynYveAz1Cxjfl0TSNt1Bc5WhyU0U6jFpYerPtgskRN8ED-7AJjv4dhASnc45PXs01yUShKCgQX4uo-PcwuJ51-YmyOdAEV6k'
      }
    ],
    assignedAgents: ['Agent "Frank"', 'Agent "Grace"']
  }
])

// Filtered teams based on search
const filteredTeams = computed(() => {
  if (!searchQuery.value) return teams.value

  const query = searchQuery.value.toLowerCase()
  return teams.value.filter(team =>
    team.name.toLowerCase().includes(query) ||
    team.description.toLowerCase().includes(query)
  )
})

// Methods
const handleCreateTeam = () => {
  showCreateTeamModal.value = true
}

const handleSaveNewTeam = () => {
  if (!newTeam.value.name) {
    alert('Please enter a team name')
    return
  }

  const team = {
    id: teams.value.length + 1,
    name: newTeam.value.name,
    description: newTeam.value.description,
    members: [],
    assignedAgents: []
  }

  teams.value.push(team)
  showCreateTeamModal.value = false
  newTeam.value = { name: '', description: '' }

  alert('Team created successfully!')
}

const handleViewTeam = (team) => {
  alert(`View Team: ${team.name}\n\nMembers: ${team.members.length}\nAgents: ${team.assignedAgents.join(', ')}`)
}

const handleEditTeam = (team) => {
  alert(`Edit Team: ${team.name}\n\nThis would open an edit dialog for the team.`)
}

const handleDeleteTeam = (team) => {
  if (confirm(`Are you sure you want to delete "${team.name}"?`)) {
    teams.value = teams.value.filter(t => t.id !== team.id)
    alert('Team deleted successfully!')
  }
}
</script>
