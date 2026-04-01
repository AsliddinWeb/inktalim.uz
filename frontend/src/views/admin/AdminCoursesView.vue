<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center justify-between gap-4 flex-wrap">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Kurslar</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Jami: {{ coursesTotal }} ta kurs</p>
      </div>
      <button
        type="button"
        class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
        @click="openCreate"
      >
        <Plus class="w-4 h-4" />
        Yangi kurs
      </button>
    </div>

    <!-- Error -->
    <div v-if="errorCourses" class="flex items-center justify-between gap-3 rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
      <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ errorCourses }}</p>
      <button type="button" class="text-danger-400 hover:text-danger-600 transition-colors" @click="errorCourses = ''">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Table card -->
    <AppCard :padding="false">
      <AppTable :columns="columns" :rows="courses" :loading="loadingCourses" sticky-header>

        <!-- Course name -->
        <template #cell-title="{ row }">
          <div class="flex items-center gap-3 max-w-xs">
            <div
              class="w-9 h-9 flex-shrink-0 rounded-xl bg-cover bg-center bg-gray-100 dark:bg-gray-800 overflow-hidden"
            >
              <img v-if="row.thumbnail_url" :src="getMediaUrl(row.thumbnail_url)" :alt="row.title" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center">
                <BookOpen class="w-4 h-4 text-primary-400" />
              </div>
            </div>
            <div class="min-w-0">
              <p class="font-medium text-gray-900 dark:text-white truncate">{{ row.title }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ row.lessons_count ?? 0 }} ta dars</p>
            </div>
          </div>
        </template>

        <!-- Status -->
        <template #cell-is_published="{ row }">
          <span
            class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold"
            :class="row.is_published
              ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400'"
          >
            {{ row.is_published ? 'Nashr' : 'Draft' }}
          </span>
        </template>

        <!-- Order -->
        <template #cell-order="{ row }">
          <span class="text-gray-500 dark:text-gray-400 text-sm">{{ row.order }}</span>
        </template>

        <!-- Actions -->
        <template #cell-actions="{ row }">
          <div class="flex items-center gap-0.5">
            <RouterLink :to="`/admin/courses/${row.id}`">
              <button
                type="button"
                class="p-1.5 rounded-lg text-gray-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
                title="Darslar"
              >
                <List class="w-4 h-4" />
              </button>
            </RouterLink>
            <button
              type="button"
              class="p-1.5 rounded-lg text-gray-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
              title="Tahrirlash"
              @click="openEdit(row)"
            >
              <Pencil class="w-4 h-4" />
            </button>
            <button
              type="button"
              class="p-1.5 rounded-lg transition-colors"
              :class="row.is_published
                ? 'text-success-500 hover:bg-success-50 dark:hover:bg-success-900/20'
                : 'text-gray-400 hover:text-success-600 hover:bg-success-50 dark:hover:bg-success-900/20'"
              :title="row.is_published ? 'Nashrdan olish' : 'Nashr qilish'"
              @click="handlePublish(row)"
            >
              <component :is="row.is_published ? EyeOff : Eye" class="w-4 h-4" />
            </button>
            <button
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
          :total="coursesTotal"
          :per-page="perPage"
          :current-page="currentPage"
          @change="onPageChange"
        />
      </div>
    </AppCard>

    <!-- Create/Edit modal -->
    <AppModal
      :show="showForm"
      :title="editingCourse ? 'Kursni tahrirlash' : 'Yangi kurs'"
      size="lg"
      @close="closeForm"
    >
      <CourseForm
        :course="editingCourse"
        :saving="savingCourse"
        @submit="handleSubmit"
        @cancel="closeForm"
      />
    </AppModal>

    <!-- Delete confirm -->
    <AppModal :show="showDeleteModal" title="Kursni o'chirish" size="sm" @close="showDeleteModal = false">
      <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">
        <span class="font-semibold text-gray-900 dark:text-white">{{ deletingCourse?.title }}</span> kursini
        o'chirmoqchimisiz? Barcha darslar ham o'chib ketadi.
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
import { RouterLink } from 'vue-router'
import { getMediaUrl } from '@/api/upload.js'
import { BookOpen, Plus, Pencil, Trash2, Eye, EyeOff, List } from 'lucide-vue-next'
import { useAdminStore } from '@/stores/admin.js'
import { storeToRefs } from 'pinia'
import AppCard from '@/components/ui/AppCard.vue'
import AppTable from '@/components/ui/AppTable.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppAlert from '@/components/ui/AppAlert.vue'
import CourseForm from '@/components/admin/CourseForm.vue'

const adminStore = useAdminStore()
const { courses, coursesTotal, loadingCourses, savingCourse, errorCourses } = storeToRefs(adminStore)

const perPage     = 10
const currentPage = ref(1)

const showForm     = ref(false)
const editingCourse = ref(null)

const showDeleteModal = ref(false)
const deletingCourse  = ref(null)
const deleting        = ref(false)

const columns = [
  { key: 'title',        label: 'Kurs',    width: '' },
  { key: 'order',        label: 'Tartib',  width: '80px' },
  { key: 'is_published', label: 'Holati',  width: '100px' },
  { key: 'actions',      label: 'Amallar', width: '120px' },
]

async function loadCourses() {
  await adminStore.fetchCourses({
    skip:  (currentPage.value - 1) * perPage,
    limit: perPage,
  })
}

function onPageChange(page) {
  currentPage.value = page
  loadCourses()
}

function openCreate() {
  editingCourse.value = null
  showForm.value = true
}

function openEdit(course) {
  editingCourse.value = course
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingCourse.value = null
}

async function handleSubmit(data) {
  try {
    if (editingCourse.value) {
      await adminStore.updateCourse(editingCourse.value.id, data)
    } else {
      await adminStore.createCourse(data)
    }
    closeForm()
  } catch (err) {
    errorCourses.value = err.message
  }
}

async function handlePublish(course) {
  try {
    await adminStore.togglePublishCourse(course.id)
  } catch (err) {
    errorCourses.value = err.message
  }
}

function confirmDelete(course) {
  deletingCourse.value = course
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deletingCourse.value) return
  deleting.value = true
  try {
    await adminStore.deleteCourse(deletingCourse.value.id)
    showDeleteModal.value = false
    deletingCourse.value = null
    if (courses.value.length === 0 && currentPage.value > 1) {
      currentPage.value--
    }
  } catch (err) {
    errorCourses.value = err.message
  } finally {
    deleting.value = false
  }
}

onMounted(loadCourses)
</script>
