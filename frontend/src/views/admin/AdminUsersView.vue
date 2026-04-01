<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center justify-between gap-4 flex-wrap">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Foydalanuvchilar</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Jami: {{ usersTotal }} ta</p>
      </div>
      <div class="relative w-full sm:w-64">
        <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
        <input
          v-model="search"
          type="text"
          placeholder="Ism yoki email..."
          class="w-full h-11 pl-10 pr-4 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all duration-200"
          @input="onSearch"
        />
      </div>
    </div>

    <!-- Error -->
    <div v-if="errorUsers" class="rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
      <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ errorUsers }}</p>
    </div>

    <!-- Table -->
    <AppCard :padding="false">
      <AppTable :columns="columns" :rows="users" :loading="loadingUsers">

        <!-- User -->
        <template #cell-full_name="{ row }">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 flex-shrink-0 rounded-full bg-primary-100 dark:bg-primary-900/20 flex items-center justify-center">
              <span class="text-xs font-bold text-primary-600 dark:text-primary-400">
                {{ (row.full_name || row.email || '?')[0].toUpperCase() }}
              </span>
            </div>
            <div class="min-w-0">
              <p class="font-medium text-gray-900 dark:text-white truncate">{{ row.full_name || 'Ismsiz' }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ row.email }}</p>
            </div>
          </div>
        </template>

        <!-- Phone -->
        <template #cell-phone="{ row }">
          <span class="text-sm text-gray-500 dark:text-gray-400">{{ row.phone || '—' }}</span>
        </template>

        <!-- Role -->
        <template #cell-is_admin="{ row }">
          <span
            class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold"
            :class="row.is_admin
              ? 'bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400'"
          >
            {{ row.is_admin ? 'Admin' : 'Student' }}
          </span>
        </template>

        <!-- Status -->
        <template #cell-is_active="{ row }">
          <span
            class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold"
            :class="row.is_active
              ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
              : 'bg-danger-100 dark:bg-danger-900/20 text-danger-700 dark:text-danger-400'"
          >
            {{ row.is_active ? 'Faol' : 'Bloklangan' }}
          </span>
        </template>

        <!-- Actions -->
        <template #cell-actions="{ row }">
          <div class="flex items-center gap-0.5">
            <button
              type="button"
              class="p-1.5 rounded-lg transition-colors"
              :class="row.is_active
                ? 'text-gray-400 hover:text-danger-500 hover:bg-danger-50 dark:hover:bg-danger-900/20'
                : 'text-gray-400 hover:text-success-600 hover:bg-success-50 dark:hover:bg-success-900/20'"
              :title="row.is_active ? 'Bloklash' : 'Faollashtirish'"
              @click="handleToggleActive(row)"
            >
              <component :is="row.is_active ? UserX : UserCheck" class="w-4 h-4" />
            </button>
            <button
              v-if="!row.is_admin"
              type="button"
              class="p-1.5 rounded-lg text-gray-400 hover:text-danger-500 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors"
              title="O'chirish"
              @click="confirmDelete(row)"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </template>

      </AppTable>

      <!-- Pagination -->
      <div class="px-4 py-3 border-t border-gray-100 dark:border-gray-800">
        <AppPagination
          :total="usersTotal"
          :per-page="perPage"
          :current-page="currentPage"
          @change="onPageChange"
        />
      </div>
    </AppCard>

    <!-- Delete confirm -->
    <AppModal :show="showDeleteModal" title="Foydalanuvchini o'chirish" size="sm" @close="showDeleteModal = false">
      <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">
        <span class="font-semibold text-gray-900 dark:text-white">{{ deletingUser?.full_name || deletingUser?.email }}</span> ni o'chirmoqchimisiz?
      </p>
      <div class="flex gap-3">
        <button
          type="button"
          :disabled="deleting"
          class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-danger-500 hover:bg-danger-600 text-white text-sm font-semibold transition-all disabled:opacity-60"
          @click="handleDelete"
        >
          <svg v-if="deleting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          Ha, o'chirish
        </button>
        <button
          type="button"
          class="px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-gray-700 dark:text-gray-300 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
          @click="showDeleteModal = false"
        >
          Bekor
        </button>
      </div>
    </AppModal>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Trash2, UserCheck, UserX } from 'lucide-vue-next'
import { useAdminStore } from '@/stores/admin.js'
import { storeToRefs } from 'pinia'
import AppCard from '@/components/ui/AppCard.vue'
import AppTable from '@/components/ui/AppTable.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppAlert from '@/components/ui/AppAlert.vue'

const adminStore = useAdminStore()
const { users, usersTotal, loadingUsers, savingUser, errorUsers } = storeToRefs(adminStore)

const perPage     = 10
const currentPage = ref(1)
const search      = ref('')

let searchTimer = null

const showDeleteModal = ref(false)
const deletingUser    = ref(null)
const deleting        = ref(false)

const columns = [
  { key: 'full_name',  label: 'Foydalanuvchi', width: '' },
  { key: 'phone',      label: 'Telefon',        width: '140px' },
  { key: 'is_admin',   label: 'Rol',            width: '90px' },
  { key: 'is_active',  label: 'Holati',         width: '100px' },
  { key: 'actions',    label: 'Amallar',        width: '80px' },
]

function loadUsers() {
  adminStore.fetchUsers({
    skip:   (currentPage.value - 1) * perPage,
    limit:  perPage,
    search: search.value || undefined,
  })
}

function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    loadUsers()
  }, 400)
}

function onPageChange(page) {
  currentPage.value = page
  loadUsers()
}

async function handleToggleActive(user) {
  try {
    await adminStore.toggleUserActive(user.id, user.is_active)
  } catch (err) {
    errorUsers.value = err.message
  }
}

function confirmDelete(user) {
  deletingUser.value = user
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deletingUser.value) return
  deleting.value = true
  try {
    await adminStore.deleteUser(deletingUser.value.id)
    showDeleteModal.value = false
    deletingUser.value = null
  } catch (err) {
    errorUsers.value = err.message
  } finally {
    deleting.value = false
  }
}

onMounted(loadUsers)
</script>
