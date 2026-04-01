<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center gap-3 flex-wrap">
      <RouterLink to="/admin/courses">
        <button type="button" class="p-2 rounded-xl text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
          <ArrowLeft class="w-5 h-5" />
        </button>
      </RouterLink>
      <div class="flex-1 min-w-0">
        <h1 class="text-xl font-bold text-gray-900 dark:text-white truncate">
          {{ loadingCourses ? 'Yuklanmoqda...' : (course?.title || 'Kurs topilmadi') }}
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Kurs modullari va darslari</p>
      </div>
      <button
        type="button"
        class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:-translate-y-0.5 active:translate-y-0 transition-all"
        @click="openCreateModule"
      >
        <FolderPlus class="w-4 h-4" />
        Modul qo'shish
      </button>
    </div>

    <!-- Errors -->
    <div v-if="errorModules || errorLessons" class="rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
      <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ errorModules || errorLessons }}</p>
    </div>

    <!-- Loading -->
    <div v-if="loadingModules" class="space-y-3">
      <div v-for="i in 3" :key="i" class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 animate-pulse">
        <div class="h-5 bg-gray-200 dark:bg-gray-700 rounded-lg w-1/3 mb-3" />
        <div class="h-3 bg-gray-100 dark:bg-gray-800 rounded-lg w-full" />
      </div>
    </div>

    <!-- Modul yo'q holati -->
    <div v-else-if="!modules.length" class="rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-800 p-12 text-center">
      <div class="w-14 h-14 rounded-2xl bg-primary-50 dark:bg-primary-900/20 flex items-center justify-center mx-auto mb-4">
        <FolderOpen class="w-7 h-7 text-primary-500" />
      </div>
      <p class="text-base font-semibold text-gray-900 dark:text-white mb-1">Hali modullar yo'q</p>
      <p class="text-sm text-gray-400 mb-4">Kursni tashkil qilish uchun avval modul qo'shing</p>
      <button
        type="button"
        class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold transition-all"
        @click="openCreateModule"
      >
        <FolderPlus class="w-4 h-4" />
        Birinchi modulni qo'shish
      </button>
    </div>

    <!-- Modullar ro'yxati -->
    <div v-else class="space-y-3">
      <div
        v-for="(mod, mIdx) in modules"
        :key="mod.id"
        class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 overflow-hidden"
      >
        <!-- Modul header -->
        <div
          class="flex items-center gap-3 px-5 py-4 cursor-pointer select-none hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
          @click="toggleModule(mod.id)"
        >
          <!-- Order badge -->
          <span class="w-7 h-7 rounded-lg bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 text-xs font-bold flex items-center justify-center flex-shrink-0">
            {{ mIdx + 1 }}
          </span>

          <!-- Title & meta -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-semibold text-gray-900 dark:text-white truncate">{{ mod.title }}</span>
              <span
                class="inline-flex items-center text-xs font-semibold px-2 py-0.5 rounded-full"
                :class="mod.is_published
                  ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400'"
              >
                {{ mod.is_published ? 'Nashr' : 'Draft' }}
              </span>
            </div>
            <p class="text-xs text-gray-400 mt-0.5">{{ mod.lessons?.length ?? 0 }} ta dars</p>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-1 flex-shrink-0" @click.stop>
            <button
              class="p-1.5 rounded-lg text-gray-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
              title="Dars qo'shish"
              @click="openCreateLesson(mod)"
            >
              <Plus class="w-4 h-4" />
            </button>
            <button
              class="p-1.5 rounded-lg text-gray-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
              title="Tahrirlash"
              @click="openEditModule(mod)"
            >
              <Pencil class="w-4 h-4" />
            </button>
            <button
              class="p-1.5 rounded-lg transition-colors"
              :class="mod.is_published
                ? 'text-success-500 hover:bg-success-50 dark:hover:bg-success-900/20'
                : 'text-gray-400 hover:text-success-600 hover:bg-success-50 dark:hover:bg-success-900/20'"
              :title="mod.is_published ? 'Nashrdan olish' : 'Nashr qilish'"
              @click="handlePublishModule(mod)"
            >
              <component :is="mod.is_published ? EyeOff : Eye" class="w-4 h-4" />
            </button>
            <button
              class="p-1.5 rounded-lg text-gray-400 hover:text-danger-500 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors"
              title="O'chirish"
              @click="confirmDeleteModule(mod)"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>

          <!-- Expand chevron -->
          <ChevronDown
            class="w-4 h-4 text-gray-400 transition-transform duration-200 flex-shrink-0"
            :class="openModuleIds.has(mod.id) ? 'rotate-180' : ''"
          />
        </div>

        <!-- Darslar ro'yxati -->
        <Transition name="expand">
          <div v-if="openModuleIds.has(mod.id)" class="border-t border-gray-100 dark:border-gray-800">

            <!-- Bo'sh modul -->
            <div v-if="!mod.lessons?.length" class="px-5 py-6 text-center">
              <p class="text-sm text-gray-400 mb-3">Bu modulda hali dars yo'q</p>
              <button
                type="button"
                class="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-medium bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 hover:bg-primary-100 dark:hover:bg-primary-900/40 transition-colors"
                @click="openCreateLesson(mod)"
              >
                <Plus class="w-3.5 h-3.5" />
                Dars qo'shish
              </button>
            </div>

            <!-- Darslar -->
            <div v-else class="divide-y divide-gray-50 dark:divide-gray-800">
              <div
                v-for="(lesson, lIdx) in mod.lessons"
                :key="lesson.id"
                class="flex items-center gap-3 px-5 py-3 hover:bg-gray-50 dark:hover:bg-gray-800/30 group transition-colors"
              >
                <!-- Dars order -->
                <span class="w-6 h-6 rounded-md bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 text-xs font-bold flex items-center justify-center flex-shrink-0">
                  {{ lesson.order }}
                </span>

                <!-- Dars info -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <span class="text-sm font-medium text-gray-800 dark:text-gray-200 truncate">{{ lesson.title }}</span>
                    <span
                      class="inline-flex text-xs font-semibold px-1.5 py-0.5 rounded-full flex-shrink-0"
                      :class="lesson.is_published
                        ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
                        : 'bg-gray-100 dark:bg-gray-800 text-gray-500'"
                    >
                      {{ lesson.is_published ? 'Nashr' : 'Draft' }}
                    </span>
                  </div>
                  <div class="flex items-center gap-2 mt-0.5">
                    <span v-if="lesson.duration_minutes" class="text-xs text-gray-400">{{ lesson.duration_minutes }} daq</span>
                    <span v-if="lesson.video_url" class="text-xs text-primary-400 flex items-center gap-0.5">
                      <PlayCircle class="w-3 h-3" /> Video
                    </span>
                  </div>
                </div>

                <!-- Dars amallar -->
                <div class="flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    class="p-1.5 rounded-lg text-gray-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
                    title="Tahrirlash"
                    @click="openEditLesson(lesson)"
                  >
                    <Pencil class="w-3.5 h-3.5" />
                  </button>
                  <button
                    class="p-1.5 rounded-lg transition-colors"
                    :class="lesson.is_published
                      ? 'text-success-500 hover:bg-success-50 dark:hover:bg-success-900/20'
                      : 'text-gray-400 hover:text-success-600 hover:bg-success-50 dark:hover:bg-success-900/20'"
                    @click="handlePublishLesson(lesson)"
                  >
                    <component :is="lesson.is_published ? EyeOff : Eye" class="w-3.5 h-3.5" />
                  </button>
                  <button
                    class="p-1.5 rounded-lg transition-colors"
                    :class="lesson.has_quiz
                      ? 'text-success-500 hover:bg-success-50 dark:hover:bg-success-900/20'
                      : 'text-gray-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20'"
                    :title="lesson.has_quiz ? 'Quiz bor — boshqarish' : 'Quiz qo\'shish'"
                    @click="openQuizManager(lesson)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
                    </svg>
                  </button>
                  <button
                    class="p-1.5 rounded-lg text-gray-400 hover:text-danger-500 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors"
                    title="O'chirish"
                    @click="confirmDeleteLesson(lesson)"
                  >
                    <Trash2 class="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              <!-- Dars qo'shish tugmasi -->
              <div class="px-5 py-2.5">
                <button
                  type="button"
                  class="inline-flex items-center gap-1.5 text-xs font-medium text-gray-400 hover:text-primary-500 transition-colors"
                  @click="openCreateLesson(mod)"
                >
                  <Plus class="w-3.5 h-3.5" />
                  Dars qo'shish
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Module form modal -->
    <AppModal :show="showModuleForm" :title="editingModule ? 'Modulni tahrirlash' : 'Yangi modul'" size="md" @close="closeModuleForm">
      <ModuleForm :module="editingModule" :saving="savingModule" @submit="handleModuleSubmit" @cancel="closeModuleForm" />
    </AppModal>

    <!-- Lesson form modal -->
    <AppModal :show="showLessonForm" :title="editingLesson ? 'Darsni tahrirlash' : 'Yangi dars'" size="lg" @close="closeLessonForm">
      <LessonForm
        :lesson="editingLesson"
        :course-id="courseId"
        :module-id="lessonTargetModuleId"
        :modules="modules"
        :saving="savingLesson"
        @submit="handleLessonSubmit"
        @cancel="closeLessonForm"
      />
    </AppModal>

    <!-- Delete module confirm -->
    <AppModal :show="showDeleteModuleModal" title="Modulni o'chirish" size="sm" @close="showDeleteModuleModal = false">
      <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">
        <span class="font-semibold text-gray-900 dark:text-white">{{ deletingModule?.title }}</span> moduli va uning barcha darslari o'chiriladi!
      </p>
      <div class="flex gap-3">
        <button
          type="button"
          :disabled="deleting"
          class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-danger-500 hover:bg-danger-600 text-white text-sm font-semibold transition-all disabled:opacity-60"
          @click="handleDeleteModule"
        >
          <svg v-if="deleting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          Ha, o'chirish
        </button>
        <button type="button" class="px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-gray-700 dark:text-gray-300 text-sm hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors" @click="showDeleteModuleModal = false">Bekor</button>
      </div>
    </AppModal>

    <!-- Delete lesson confirm -->
    <AppModal :show="showDeleteLessonModal" title="Darsni o'chirish" size="sm" @close="showDeleteLessonModal = false">
      <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">
        <span class="font-semibold text-gray-900 dark:text-white">{{ deletingLesson?.title }}</span> darsini o'chirmoqchimisiz?
      </p>
      <div class="flex gap-3">
        <button
          type="button"
          :disabled="deletingLessonLoading"
          class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-danger-500 hover:bg-danger-600 text-white text-sm font-semibold transition-all disabled:opacity-60"
          @click="handleDeleteLesson"
        >
          <svg v-if="deletingLessonLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          Ha, o'chirish
        </button>
        <button type="button" class="px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-gray-700 dark:text-gray-300 text-sm hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors" @click="showDeleteLessonModal = false">Bekor</button>
      </div>
    </AppModal>

    <!-- Quiz manager modal -->
    <AppModal :show="showQuizModal" :title="`Quiz — ${quizLesson?.title ?? ''}`" size="lg" @close="closeQuizModal">
      <QuizManager v-if="quizLesson" :lesson-id="quizLesson.id" @quiz-changed="onQuizChanged" />
    </AppModal>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import {
  ArrowLeft, Plus, Pencil, Trash2, Eye, EyeOff,
  ChevronDown, FolderPlus, FolderOpen, PlayCircle,
} from 'lucide-vue-next'
import { useAdminStore } from '@/stores/admin.js'
import { storeToRefs } from 'pinia'
import AppModal from '@/components/ui/AppModal.vue'
import ModuleForm from '@/components/admin/ModuleForm.vue'
import LessonForm from '@/components/admin/LessonForm.vue'
import QuizManager from '@/components/admin/QuizManager.vue'
import { adminQuizApi } from '@/api/quiz.js'

const route = useRoute()
const courseId = computed(() => route.params.id)

const adminStore = useAdminStore()
const {
  modules, loadingModules, savingModule, errorModules,
  savingLesson, errorLessons,
  currentCourse, loadingCourses,
} = storeToRefs(adminStore)

const course = currentCourse

// Ochiq modul IDlari (accordion)
const openModuleIds = ref(new Set())

function toggleModule(id) {
  if (openModuleIds.value.has(id)) openModuleIds.value.delete(id)
  else openModuleIds.value.add(id)
}

// ─── Module CRUD ─────────────────────────────────────────────────────────────
const showModuleForm   = ref(false)
const editingModule    = ref(null)

const showDeleteModuleModal = ref(false)
const deletingModule        = ref(null)
const deleting              = ref(false)

function openCreateModule() {
  editingModule.value = null
  showModuleForm.value = true
}

function openEditModule(mod) {
  editingModule.value = mod
  showModuleForm.value = true
}

function closeModuleForm() {
  showModuleForm.value = false
  editingModule.value = null
}

async function handleModuleSubmit(data) {
  try {
    if (editingModule.value) {
      await adminStore.updateModule(courseId.value, editingModule.value.id, data)
    } else {
      const mod = await adminStore.createModule(courseId.value, data)
      openModuleIds.value.add(mod.id)
    }
    closeModuleForm()
  } catch (err) {
    errorModules.value = err.message
  }
}

async function handlePublishModule(mod) {
  try {
    await adminStore.togglePublishModule(courseId.value, mod.id)
  } catch (err) {
    errorModules.value = err.message
  }
}

function confirmDeleteModule(mod) {
  deletingModule.value = mod
  showDeleteModuleModal.value = true
}

async function handleDeleteModule() {
  if (!deletingModule.value) return
  deleting.value = true
  try {
    await adminStore.deleteModule(courseId.value, deletingModule.value.id)
    showDeleteModuleModal.value = false
    deletingModule.value = null
  } catch (err) {
    errorModules.value = err.message
  } finally {
    deleting.value = false
  }
}

// ─── Lesson CRUD ─────────────────────────────────────────────────────────────
const showLessonForm       = ref(false)
const editingLesson        = ref(null)
const lessonTargetModuleId = ref(null)

const showDeleteLessonModal  = ref(false)
const deletingLesson         = ref(null)
const deletingLessonLoading  = ref(false)

function openCreateLesson(mod) {
  editingLesson.value = null
  lessonTargetModuleId.value = mod.id
  showLessonForm.value = true
}

function openEditLesson(lesson) {
  editingLesson.value = lesson
  lessonTargetModuleId.value = lesson.module_id
  showLessonForm.value = true
}

function closeLessonForm() {
  showLessonForm.value = false
  editingLesson.value = null
  lessonTargetModuleId.value = null
}

async function handleLessonSubmit(data) {
  try {
    if (editingLesson.value) {
      await adminStore.updateLesson(courseId.value, editingLesson.value.id, data)
    } else {
      await adminStore.createLesson(courseId.value, data)
    }
    // Modullarni qayta yuklash (darslar tarkibi o'zgardi)
    await loadModulesWithQuizInfo()
    closeLessonForm()
  } catch (err) {
    errorLessons.value = err.message
  }
}

async function handlePublishLesson(lesson) {
  try {
    await adminStore.togglePublishLesson(courseId.value, lesson.id)
    await loadModulesWithQuizInfo()
  } catch (err) {
    errorLessons.value = err.message
  }
}

function confirmDeleteLesson(lesson) {
  deletingLesson.value = lesson
  showDeleteLessonModal.value = true
}

async function handleDeleteLesson() {
  if (!deletingLesson.value) return
  deletingLessonLoading.value = true
  try {
    await adminStore.deleteLesson(courseId.value, deletingLesson.value.id)
    await loadModulesWithQuizInfo()
    showDeleteLessonModal.value = false
    deletingLesson.value = null
  } catch (err) {
    errorLessons.value = err.message
  } finally {
    deletingLessonLoading.value = false
  }
}

// ─── Quiz ─────────────────────────────────────────────────────────────────────
const showQuizModal = ref(false)
const quizLesson    = ref(null)

function openQuizManager(lesson) {
  quizLesson.value = lesson
  showQuizModal.value = true
}

function closeQuizModal() {
  showQuizModal.value = false
  quizLesson.value = null
}

async function onQuizChanged() {
  await loadModulesWithQuizInfo()
}

// ─── Load ─────────────────────────────────────────────────────────────────────
async function loadModulesWithQuizInfo() {
  await adminStore.fetchModules(courseId.value)
  // Har bir dars uchun quiz borligini tekshirish
  for (const mod of modules.value) {
    for (const lesson of (mod.lessons || [])) {
      try {
        await adminQuizApi.getByLesson(lesson.id)
        lesson.has_quiz = true
      } catch {
        lesson.has_quiz = false
      }
    }
  }
}

onMounted(async () => {
  await Promise.all([
    adminStore.fetchCourse(courseId.value),
    loadModulesWithQuizInfo(),
  ])
  // Birinchi modulni ochib qo'yish
  if (modules.value.length) {
    openModuleIds.value.add(modules.value[0].id)
  }
})
</script>

<style scoped>
.expand-enter-active { transition: all 0.2s ease; }
.expand-leave-active { transition: all 0.15s ease; }
.expand-enter-from, .expand-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
