<template>
  <div class="h-full">

    <!-- Loading skeleton -->
    <div v-if="coursesStore.loadingLesson" class="flex gap-6">
      <div class="flex-1 space-y-4">
        <div class="h-8 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-xl w-3/4" />
        <div class="h-64 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-2xl" />
        <div v-for="i in 6" :key="i" class="h-4 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-lg" :style="`width:${80 - i*5}%`" />
      </div>
      <div class="hidden lg:block w-72 space-y-2">
        <div v-for="i in 8" :key="i" class="h-12 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-xl" />
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="coursesStore.errorLesson" class="rounded-2xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 p-6 text-center">
      <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ coursesStore.errorLesson }}</p>
    </div>

    <!-- Content -->
    <div v-else-if="lesson" class="flex gap-6 min-h-full">

      <!-- Main column -->
      <div class="flex-1 min-w-0 space-y-5">

        <!-- Mobile sidebar toggle -->
        <div class="lg:hidden">
          <button
            type="button"
            class="inline-flex items-center gap-2 text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 transition-colors"
            @click="showMobileSidebar = !showMobileSidebar"
          >
            <List class="w-4 h-4" />
            {{ showMobileSidebar ? 'Darslarni yashirish' : 'Barcha darslar' }}
          </button>
          <Transition name="collapse">
            <div v-if="showMobileSidebar" class="mt-3 rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface overflow-hidden">
              <template v-if="courseData?.modules?.length">
                <div v-for="mod in courseData.modules" :key="mod.id">
                  <button
                    type="button"
                    class="w-full flex items-center gap-2 px-3 py-2.5 bg-gray-50 dark:bg-gray-800/60 hover:bg-gray-100 dark:hover:bg-gray-800 text-left"
                    @click="toggleSidebarModule(mod.id)"
                  >
                    <span class="w-5 h-5 rounded-full bg-primary-100 dark:bg-primary-900/40 text-primary-600 dark:text-primary-400 text-[10px] font-bold flex items-center justify-center flex-shrink-0">{{ mod.order }}</span>
                    <span class="flex-1 text-xs font-semibold text-gray-700 dark:text-gray-300 truncate">{{ mod.title }}</span>
                    <ChevronDown class="w-3 h-3 text-gray-400 flex-shrink-0 transition-transform duration-200" :class="sidebarOpenModules.has(mod.id) ? 'rotate-180' : ''" />
                  </button>
                  <div v-if="sidebarOpenModules.has(mod.id)" class="divide-y divide-gray-100 dark:divide-gray-800">
                    <LessonItem v-for="l in mod.lessons" :key="l.id" :lesson="l" :active="l.id === lesson.id" @click="goToLesson(l)" />
                  </div>
                </div>
              </template>
              <div v-if="courseData?.lessons?.length" class="divide-y divide-gray-100 dark:divide-gray-800">
                <LessonItem v-for="l in courseData.lessons" :key="l.id" :lesson="l" :active="l.id === lesson.id" @click="goToLesson(l)" />
              </div>
            </div>
          </Transition>
        </div>

        <!-- Back link -->
        <RouterLink
          :to="`/dashboard/courses/${courseId}`"
          class="inline-flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
        >
          <ArrowLeft class="w-4 h-4" />
          Kursga qaytish
        </RouterLink>

        <!-- Lesson title -->
        <div>
          <h1 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white leading-snug">
            {{ lesson.title }}
          </h1>
          <div v-if="lesson.duration_minutes" class="flex items-center gap-1.5 mt-2 text-sm text-gray-500 dark:text-gray-400">
            <Clock class="w-4 h-4" />
            {{ lesson.duration_minutes }} daqiqa
          </div>
        </div>

        <!-- Video -->
        <div v-if="lesson.video_url" class="rounded-2xl overflow-hidden bg-black aspect-video shadow-lg">
          <iframe
            v-if="isYouTube(lesson.video_url)"
            :src="youTubeEmbedUrl(lesson.video_url)"
            class="w-full h-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            frameborder="0"
          />
          <video
            v-else
            :src="lesson.video_url"
            class="w-full h-full"
            controls
          />
        </div>

        <!-- Lesson content -->
        <div
          v-if="lesson.content"
          class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6 lg:p-8"
        >
          <div
            class="prose prose-sm sm:prose max-w-none dark:prose-invert
                   prose-headings:text-gray-900 dark:prose-headings:text-white
                   prose-p:text-gray-600 dark:prose-p:text-gray-300
                   prose-a:text-primary-600 dark:prose-a:text-primary-400
                   prose-strong:text-gray-900 dark:prose-strong:text-white
                   prose-code:text-primary-700 dark:prose-code:text-primary-300
                   prose-pre:bg-gray-50 dark:prose-pre:bg-gray-900"
            v-html="lesson.content"
          />
        </div>

        <!-- Navigation buttons -->
        <div class="flex items-center justify-between gap-3 pt-2">
          <RouterLink
            v-if="lesson.prev_lesson"
            :to="`/dashboard/courses/${courseId}/lessons/${lesson.prev_lesson.id}`"
            class="flex-1 inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
          >
            <ChevronLeft class="w-4 h-4 flex-shrink-0" />
            <span class="truncate hidden sm:inline">{{ lesson.prev_lesson.title }}</span>
            <span class="sm:hidden">Oldingi</span>
          </RouterLink>
          <div v-else class="flex-1" />

          <button
            type="button"
            :disabled="progressStore.completingLesson"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200"
            :class="lesson.is_completed
              ? 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
              : 'bg-primary-500 hover:bg-primary-600 text-white shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0'"
            @click="toggleComplete"
          >
            <svg v-if="progressStore.completingLesson" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            <RotateCcw v-else-if="lesson.is_completed" class="w-4 h-4" />
            <CheckCircle v-else class="w-4 h-4" />
            <span class="hidden sm:inline">{{ lesson.is_completed ? 'Qaytarish' : 'Darsni tugatdim' }}</span>
            <span class="sm:hidden">{{ lesson.is_completed ? '↩' : '✓' }}</span>
          </button>

          <RouterLink
            v-if="lesson.next_lesson"
            :to="`/dashboard/courses/${courseId}/lessons/${lesson.next_lesson.id}`"
            class="flex-1 inline-flex items-center justify-end gap-2 px-4 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
          >
            <span class="truncate hidden sm:inline">{{ lesson.next_lesson.title }}</span>
            <span class="sm:hidden">Keyingi</span>
            <ChevronRight class="w-4 h-4 flex-shrink-0" />
          </RouterLink>
          <div v-else class="flex-1" />
        </div>

        <!-- Alerts -->
        <Transition name="alert">
          <div v-if="completedMsg" class="flex items-center gap-3 rounded-xl border border-success-200 dark:border-success-800/30 bg-success-50 dark:bg-success-900/10 px-4 py-3">
            <CheckCircle class="w-4 h-4 text-success-500 flex-shrink-0" />
            <p class="text-sm font-medium text-success-700 dark:text-success-400">{{ completedMsg }}</p>
          </div>
        </Transition>
        <Transition name="alert">
          <div v-if="errorMsg" class="flex items-center gap-3 rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
            <p class="text-sm font-medium text-danger-700 dark:text-danger-400">{{ errorMsg }}</p>
          </div>
        </Transition>

        <!-- Quiz banner -->
        <div
          v-if="hasQuiz"
          class="rounded-2xl border border-primary-200 dark:border-primary-800/40 bg-primary-50 dark:bg-primary-900/10 p-5 flex items-center justify-between gap-4"
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
              </svg>
            </div>
            <div>
              <p class="text-sm font-semibold text-primary-700 dark:text-primary-300">Bu darsda test mavjud</p>
              <p class="text-xs text-primary-600/70 dark:text-primary-400/60">Bilimingizni sinab ko'ring</p>
            </div>
          </div>
          <RouterLink
            :to="`/dashboard/courses/${courseId}/lessons/${lessonId}/quiz`"
            class="flex-shrink-0 px-4 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md transition-all duration-200 hover:-translate-y-0.5 active:translate-y-0"
          >
            Testni boshlash
          </RouterLink>
        </div>

      </div>

      <!-- Desktop sidebar -->
      <aside class="hidden lg:block w-72 flex-shrink-0">
        <div class="sticky top-24">
          <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface overflow-hidden">
            <div class="px-4 py-3.5 border-b border-gray-100 dark:border-gray-800">
              <h3 class="text-sm font-semibold text-gray-900 dark:text-white truncate">{{ currentCourseTitle }}</h3>
            </div>
            <div class="max-h-[calc(100vh-16rem)] overflow-y-auto">

              <!-- Modules -->
              <template v-if="courseData?.modules?.length">
                <div v-for="mod in courseData.modules" :key="mod.id">
                  <!-- Module header -->
                  <button
                    type="button"
                    class="w-full flex items-center gap-2 px-3 py-2.5 bg-gray-50 dark:bg-gray-800/60 hover:bg-gray-100 dark:hover:bg-gray-800 text-left transition-colors"
                    @click="toggleSidebarModule(mod.id)"
                  >
                    <span class="w-5 h-5 rounded-full bg-primary-100 dark:bg-primary-900/40 text-primary-600 dark:text-primary-400 text-[10px] font-bold flex items-center justify-center flex-shrink-0">
                      {{ mod.order }}
                    </span>
                    <span class="flex-1 text-xs font-semibold text-gray-700 dark:text-gray-300 truncate">{{ mod.title }}</span>
                    <ChevronDown
                      class="w-3 h-3 text-gray-400 flex-shrink-0 transition-transform duration-200"
                      :class="sidebarOpenModules.has(mod.id) ? 'rotate-180' : ''"
                    />
                  </button>
                  <!-- Module lessons -->
                  <div v-if="sidebarOpenModules.has(mod.id)" class="divide-y divide-gray-100 dark:divide-gray-800">
                    <LessonItem
                      v-for="l in mod.lessons"
                      :key="l.id"
                      :lesson="l"
                      :active="l.id === lesson.id"
                      @click="goToLesson(l)"
                    />
                  </div>
                </div>
              </template>

              <!-- Standalone lessons -->
              <div
                v-if="courseData?.lessons?.length"
                class="divide-y divide-gray-100 dark:divide-gray-800"
                :class="courseData?.modules?.length ? 'border-t border-gray-100 dark:border-gray-800' : ''"
              >
                <LessonItem
                  v-for="l in courseData.lessons"
                  :key="l.id"
                  :lesson="l"
                  :active="l.id === lesson.id"
                  @click="goToLesson(l)"
                />
              </div>

            </div>
          </div>
        </div>
      </aside>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import {
  ArrowLeft, ChevronDown, ChevronLeft, ChevronRight,
  Clock, CheckCircle, List, RotateCcw,
} from 'lucide-vue-next'

import { useCoursesStore }  from '@/stores/courses.js'
import { useProgressStore } from '@/stores/progress.js'
import { studentQuizApi } from '@/api/quiz.js'
import LessonItem  from '@/components/student/LessonItem.vue'
import AppCard     from '@/components/ui/AppCard.vue'
import AppButton   from '@/components/ui/AppButton.vue'
import AppAlert    from '@/components/ui/AppAlert.vue'
import AppSkeleton from '@/components/ui/AppSkeleton.vue'

const route         = useRoute()
const router        = useRouter()
const coursesStore  = useCoursesStore()
const progressStore = useProgressStore()

const courseId = route.params.courseId
const lessonId = route.params.lessonId

// Mobil sidebar holati
const showMobileSidebar = ref(false)

// Sidebar module accordion
const sidebarOpenModules = ref(new Set())
function toggleSidebarModule(id) {
  if (sidebarOpenModules.value.has(id)) {
    sidebarOpenModules.value.delete(id)
  } else {
    sidebarOpenModules.value.add(id)
  }
  sidebarOpenModules.value = new Set(sidebarOpenModules.value)
}

// Xabar holatlari
const completedMsg = ref('')
const errorMsg     = ref('')

// Bu darsda quiz bormi?
const hasQuiz = ref(false)

const lesson     = computed(() => coursesStore.currentLesson)
const courseData = computed(() => coursesStore.currentCourse)

const currentCourseTitle = computed(() =>
  courseData.value?.title ?? 'Kurs darslari'
)

// YouTube URL ni embed URL ga o'girish
function isYouTube(url) {
  return url && (url.includes('youtube.com') || url.includes('youtu.be'))
}
function youTubeEmbedUrl(url) {
  const match = url.match(/(?:v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/)
  if (match) return `https://www.youtube.com/embed/${match[1]}`
  return url
}

// Dars complete toggle
async function toggleComplete() {
  completedMsg.value = ''
  errorMsg.value = ''
  try {
    if (lesson.value.is_completed) {
      await progressStore.markUncomplete(lessonId, courseId)
      completedMsg.value = ''
    } else {
      await progressStore.markComplete(lessonId, courseId)
      completedMsg.value = 'Dars muvaffaqiyatli tugatildi! 🎉'
      setTimeout(() => { completedMsg.value = '' }, 4000)
    }
    // Sidebar dagi holat uchun kursni qayta yuklaymiz
    if (courseData.value) {
      await coursesStore.fetchCourse(courseId)
    }
  } catch (err) {
    errorMsg.value = err.message
    setTimeout(() => { errorMsg.value = '' }, 5000)
  }
}

function goToLesson(l) {
  showMobileSidebar.value = false
  router.push(`/dashboard/courses/${courseId}/lessons/${l.id}`)
}

onMounted(async () => {
  // Dars va kurs ma'lumotlarini parallel yuklash
  await Promise.all([
    coursesStore.fetchLesson(courseId, lessonId),
    coursesStore.fetchCourse(courseId),
  ])
  // Auto-open the module that contains the current lesson
  if (courseData.value?.modules?.length) {
    const activeModule = courseData.value.modules.find(m =>
      m.lessons?.some(l => l.id === lessonId)
    )
    if (activeModule) {
      sidebarOpenModules.value = new Set([activeModule.id])
    } else {
      sidebarOpenModules.value = new Set([courseData.value.modules[0].id])
    }
  }
  // Quiz borligini tekshirish
  try {
    await studentQuizApi.getByLesson(lessonId)
    hasQuiz.value = true
  } catch {
    hasQuiz.value = false
  }
})
</script>

<style scoped>
.collapse-enter-active, .collapse-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.collapse-enter-from, .collapse-leave-to {
  opacity: 0;
  max-height: 0;
}
.collapse-enter-to, .collapse-leave-from {
  max-height: 500px;
}
.alert-enter-active, .alert-leave-active { transition: all 0.3s ease; }
.alert-enter-from, .alert-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
