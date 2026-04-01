<template>
  <div>

    <!-- Loading skeleton -->
    <div v-if="coursesStore.loadingCourse" class="space-y-6">
      <div class="rounded-2xl aspect-[21/9] bg-gray-200 dark:bg-gray-800 animate-pulse" />
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-3">
          <div v-for="i in 5" :key="i" class="h-16 rounded-xl bg-gray-200 dark:bg-gray-800 animate-pulse" />
        </div>
        <div class="rounded-2xl h-64 bg-gray-200 dark:bg-gray-800 animate-pulse" />
      </div>
    </div>

    <!-- Main content -->
    <div v-else-if="course" class="space-y-6">

      <!-- Hero thumbnail -->
      <div class="rounded-2xl overflow-hidden relative min-h-[200px] bg-gray-200 dark:bg-gray-800">
        <img
          v-if="course.thumbnail_url"
          :src="getMediaUrl(course.thumbnail_url)"
          :alt="course.title"
          class="w-full aspect-[21/9] object-cover"
        />
        <div v-else class="aspect-[21/9] gradient-primary" />
        <!-- Overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent" />
        <!-- Content -->
        <div class="absolute bottom-0 left-0 right-0 px-6 lg:px-8 py-6">
          <h1 class="text-2xl lg:text-3xl font-bold text-white mb-2">{{ course.title }}</h1>
          <div class="flex flex-wrap items-center gap-3">
            <span class="inline-flex items-center gap-1.5 text-sm text-white/80">
              <PlayCircle class="size-4" />
              {{ totalLessonsCount }} ta dars
            </span>
            <span class="inline-flex items-center gap-1.5 text-sm text-white/80">
              <TrendingUp class="size-4" />
              {{ course.progress_percent ?? 0 }}% tugallangan
            </span>
          </div>
        </div>
      </div>

      <!-- Grid: lessons + sidebar -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">

        <!-- Lessons column -->
        <div class="lg:col-span-2 space-y-3">

          <!-- Modules with nested lessons -->
          <template v-if="course.modules && course.modules.length">
            <div
              v-for="mod in course.modules"
              :key="mod.id"
              class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface overflow-hidden"
            >
              <!-- Module header -->
              <button
                type="button"
                class="w-full flex items-center gap-3 px-5 py-4 text-left hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                @click="toggleModule(mod.id)"
              >
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 text-xs font-bold flex items-center justify-center">
                  {{ mod.order }}
                </span>
                <span class="flex-1 text-sm font-semibold text-gray-900 dark:text-white">{{ mod.title }}</span>
                <span class="text-xs text-gray-400 dark:text-gray-500 mr-2">{{ mod.lessons?.length ?? 0 }} dars</span>
                <ChevronDown
                  class="w-4 h-4 text-gray-400 flex-shrink-0 transition-transform duration-200"
                  :class="openModuleIds.has(mod.id) ? 'rotate-180' : ''"
                />
              </button>
              <!-- Lessons inside module -->
              <div v-if="openModuleIds.has(mod.id)" class="divide-y divide-gray-100 dark:divide-gray-800 border-t border-gray-100 dark:border-gray-800">
                <LessonItem
                  v-for="lesson in mod.lessons"
                  :key="lesson.id"
                  :lesson="lesson"
                  :active="false"
                  @click="goToLesson(lesson)"
                />
                <div v-if="!mod.lessons?.length" class="px-5 py-4 text-sm text-gray-400 text-center">
                  Bu modulda hali darslar yo'q
                </div>
              </div>
            </div>
          </template>

          <!-- Standalone lessons (no module) -->
          <div
            v-if="course.lessons && course.lessons.length"
            class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface overflow-hidden"
          >
            <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100 dark:border-gray-800">
              <h3 class="text-base font-semibold text-gray-900 dark:text-white">
                {{ course.modules?.length ? 'Boshqa darslar' : "Darslar ro'yxati" }}
              </h3>
              <span class="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">
                {{ course.lessons.length }} ta
              </span>
            </div>
            <div class="divide-y divide-gray-100 dark:divide-gray-800">
              <LessonItem
                v-for="lesson in course.lessons"
                :key="lesson.id"
                :lesson="lesson"
                :active="false"
                @click="goToLesson(lesson)"
              />
            </div>
          </div>

          <!-- Empty state -->
          <div
            v-if="!course.modules?.length && !course.lessons?.length"
            class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface px-5 py-12 text-center"
          >
            <PlayCircle class="w-10 h-10 text-gray-200 dark:text-gray-700 mx-auto mb-2" />
            <p class="text-sm text-gray-400">Hali darslar qo'shilmagan</p>
          </div>

        </div>

        <!-- Progress sidebar -->
        <div class="lg:col-span-1">
          <div class="space-y-4 lg:sticky lg:top-6">

            <!-- Progress card -->
            <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6 text-center">
              <!-- SVG circle -->
              <div class="flex justify-center mb-3">
                <svg width="140" height="140" viewBox="0 0 140 140" fill="none">
                  <circle cx="70" cy="70" r="60" stroke-width="10" class="stroke-gray-100 dark:stroke-gray-800" fill="none" />
                  <circle
                    cx="70" cy="70" r="60" stroke-width="10" stroke-linecap="round" fill="none"
                    class="stroke-primary-500"
                    transform="rotate(-90 70 70)"
                    :stroke-dasharray="2 * Math.PI * 60"
                    :stroke-dashoffset="2 * Math.PI * 60 * (1 - (course.progress_percent ?? 0) / 100)"
                    style="transition: stroke-dashoffset 0.6s ease"
                  />
                  <text x="70" y="70" text-anchor="middle" dominant-baseline="central"
                    class="fill-gray-900 dark:fill-white" style="font-size:22px;font-weight:800">
                    {{ course.progress_percent ?? 0 }}%
                  </text>
                </svg>
              </div>
              <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
                {{ completedCount }}/{{ totalLessonsCount }} dars tugallandi
              </p>
              <AppProgress :value="course.progress_percent ?? 0" size="sm" class="mb-5" />
              <RouterLink
                v-if="nextLessonPath"
                :to="nextLessonPath"
                class="w-full inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-primary-500 hover:bg-primary-600 text-white font-semibold text-sm transition-colors shadow-sm hover:shadow-md"
              >
                {{ course.is_enrolled ? (completedCount > 0 ? 'Davom etish' : 'Boshlash') : "Ro'yxatdan o'tish" }}
              </RouterLink>
            </div>

            <!-- Certificate banner (100% complete) -->
            <div
              v-if="course.progress_percent === 100"
              class="rounded-2xl overflow-hidden"
              style="background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%)"
            >
              <div class="p-5 text-center text-white">
                <Award class="w-10 h-10 mx-auto mb-2 opacity-90" />
                <h4 class="font-bold text-lg mb-1">Sertifikat olishga tayyor!</h4>
                <p class="text-sm text-white/80 mb-4">Kursni muvaffaqiyatli tugatdingiz</p>
                <button
                  type="button"
                  :disabled="certLoading"
                  class="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-white text-secondary-600 hover:bg-white/90 font-semibold text-sm transition-all disabled:opacity-60"
                  @click="handleGetCertificate"
                >
                  <Loader2 v-if="certLoading" class="size-4 animate-spin" />
                  <Eye v-else class="size-4" />
                  {{ existingCertNumber ? "Sertifikatni ko'rish" : "Sertifikat olish" }}
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>

    <!-- Error -->
    <div v-else class="text-center py-16">
      <ArrowLeft class="w-12 h-12 text-gray-200 dark:text-gray-700 mx-auto mb-3" />
      <h3 class="text-base font-semibold text-gray-400">Kurs topilmadi</h3>
      <RouterLink to="/dashboard/courses" class="mt-4 inline-block text-sm text-primary-500 font-medium">
        Kurslarga qaytish
      </RouterLink>
    </div>

  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Award, BookOpen, ChevronDown, Eye, Loader2, TrendingUp, PlayCircle } from 'lucide-vue-next'

import { useCoursesStore } from '@/stores/courses.js'
import { getCertificate } from '@/api/certificate.js'
import { getMediaUrl } from '@/api/upload.js'
import LessonItem  from '@/components/student/LessonItem.vue'
import AppCard     from '@/components/ui/AppCard.vue'
import AppBadge    from '@/components/ui/AppBadge.vue'
import AppProgress from '@/components/ui/AppProgress.vue'
import AppSkeleton from '@/components/ui/AppSkeleton.vue'
import AppAlert    from '@/components/ui/AppAlert.vue'
import AppButton   from '@/components/ui/AppButton.vue'

const route        = useRoute()
const router       = useRouter()
const coursesStore = useCoursesStore()

const courseId = route.params.id

const course = computed(() => coursesStore.currentCourse)

// Accordion state for modules
const openModuleIds = ref(new Set())
function toggleModule(id) {
  if (openModuleIds.value.has(id)) {
    openModuleIds.value.delete(id)
  } else {
    openModuleIds.value.add(id)
  }
  openModuleIds.value = new Set(openModuleIds.value)
}

// All lessons flattened (modules + standalone)
const allLessons = computed(() => {
  const fromModules = course.value?.modules?.flatMap(m => m.lessons ?? []) ?? []
  const standalone  = course.value?.lessons ?? []
  return [...fromModules, ...standalone]
})

const totalLessonsCount = computed(() => allLessons.value.length)

// Tugatilgan darslar soni
const completedCount = computed(() =>
  allLessons.value.filter(l => l.is_completed).length
)

// Eng birinchi tugatilmagan dars — "Davom etish" uchun
const nextLesson = computed(() =>
  allLessons.value.find(l => !l.is_completed) ?? allLessons.value[0]
)

const nextLessonPath = computed(() =>
  nextLesson.value
    ? `/dashboard/courses/${courseId}/lessons/${nextLesson.value.id}`
    : null
)

// Sertifikat holati
const certLoading = ref(false)
const existingCertNumber = ref(null)

function goToLesson(lesson) {
  router.push(`/dashboard/courses/${courseId}/lessons/${lesson.id}`)
}

async function handleGetCertificate() {
  certLoading.value = true
  try {
    const { data } = await getCertificate(courseId)
    existingCertNumber.value = data.certificate_number
    router.push(`/dashboard/certificates/${data.certificate_number}`)
  } catch (err) {
    console.error('Sertifikat olishda xatolik:', err)
  } finally {
    certLoading.value = false
  }
}

onMounted(async () => {
  await coursesStore.fetchCourse(courseId)
  // First module auto-open
  if (course.value?.modules?.length) {
    openModuleIds.value = new Set([course.value.modules[0].id])
  }
  // Kurs tugallangan bo'lsa mavjud sertifikatni tekshirish
  if (course.value?.progress_percent === 100) {
    try {
      const { data } = await getCertificate(courseId)
      existingCertNumber.value = data.certificate_number
    } catch {
      // Sertifikat hali yo'q — tugma ko'rinadi
    }
  }
})
</script>
