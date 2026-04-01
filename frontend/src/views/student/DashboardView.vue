<template>
  <div class="space-y-8">

    <!-- Greeting -->
    <div>
      <h1 class="text-2xl lg:text-3xl font-bold text-gray-900 dark:text-white">
        Xush kelibsiz, {{ firstName }}! 👋
      </h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        {{ new Date().toLocaleDateString('uz-UZ', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}
      </p>
    </div>

    <!-- Stat cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
      <!-- Kurslar -->
      <div class="rounded-2xl bg-white dark:bg-surface border border-gray-100 dark:border-gray-800 p-5 flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-primary-100 dark:bg-primary-900/20 flex items-center justify-center flex-shrink-0">
          <BookOpen class="size-6 text-primary-600 dark:text-primary-400" />
        </div>
        <div class="min-w-0">
          <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ coursesStore.courses.length }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 truncate">Kurslar</p>
        </div>
      </div>
      <!-- Davom etayotgan -->
      <div class="rounded-2xl bg-white dark:bg-surface border border-gray-100 dark:border-gray-800 p-5 flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-blue-100 dark:bg-blue-900/20 flex items-center justify-center flex-shrink-0">
          <PlayCircle class="size-6 text-blue-600 dark:text-blue-400" />
        </div>
        <div class="min-w-0">
          <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ coursesStore.inProgressCourses.length }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 truncate">Davomda</p>
        </div>
      </div>
      <!-- Tugatilgan -->
      <div class="rounded-2xl bg-white dark:bg-surface border border-gray-100 dark:border-gray-800 p-5 flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-success-100 dark:bg-success-900/20 flex items-center justify-center flex-shrink-0">
          <CheckCircle class="size-6 text-success-600 dark:text-success-400" />
        </div>
        <div class="min-w-0">
          <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ coursesStore.completedCourses?.length ?? 0 }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 truncate">Tugallandi</p>
        </div>
      </div>
      <!-- Sertifikatlar -->
      <div class="rounded-2xl bg-white dark:bg-surface border border-gray-100 dark:border-gray-800 p-5 flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-secondary-100 dark:bg-secondary-900/20 flex items-center justify-center flex-shrink-0">
          <Award class="size-6 text-secondary-600 dark:text-secondary-400" />
        </div>
        <div class="min-w-0">
          <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ certCount }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 truncate">Sertifikat</p>
        </div>
      </div>
    </div>

    <!-- Latest certificate banner -->
    <div
      v-if="latestCert"
      class="rounded-2xl border border-secondary-200 dark:border-secondary-800/30 bg-secondary-50 dark:bg-secondary-900/10 p-4 flex items-center gap-4"
    >
      <div class="w-10 h-10 rounded-xl bg-secondary-100 dark:bg-secondary-900/30 flex items-center justify-center flex-shrink-0">
        <Award class="size-5 text-secondary-500" />
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-sm font-semibold text-secondary-900 dark:text-secondary-300">Oxirgi sertifikat</p>
        <p class="text-xs font-mono text-secondary-600 dark:text-secondary-400 truncate mt-0.5">
          {{ latestCert.certificate_number }}
        </p>
      </div>
      <RouterLink
        :to="`/dashboard/certificates/${latestCert.certificate_number}`"
        class="flex-shrink-0 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-semibold bg-secondary-500 hover:bg-secondary-600 text-white transition-colors"
      >
        <TrendingUp class="size-4" />
        Ko'rish
      </RouterLink>
    </div>

    <!-- Active courses section -->
    <div>
      <div class="flex items-center justify-between mb-5">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Davom etayotgan kurslar</h2>
        <RouterLink
          to="/dashboard/courses"
          class="text-sm text-primary-500 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
        >
          Barchasini ko'rish →
        </RouterLink>
      </div>

      <!-- Loading -->
      <div v-if="coursesStore.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="i in 3"
          :key="i"
          class="rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden animate-pulse"
        >
          <div class="aspect-video bg-gray-200 dark:bg-gray-800" />
          <div class="p-5 space-y-3">
            <div class="h-4 bg-gray-200 dark:bg-gray-800 rounded-lg w-3/4" />
            <div class="h-3 bg-gray-200 dark:bg-gray-800 rounded-lg" />
            <div class="h-8 bg-gray-200 dark:bg-gray-800 rounded-xl mt-4" />
          </div>
        </div>
      </div>

      <!-- Courses grid -->
      <div v-else-if="inProgressSlice.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <CourseCard
          v-for="course in inProgressSlice"
          :key="course.id"
          :course="course"
        />
      </div>

      <!-- Empty state -->
      <div
        v-else
        class="rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700 p-10 text-center"
      >
        <BookOpen class="w-12 h-12 text-gray-200 dark:text-gray-700 mx-auto mb-3" />
        <h3 class="text-base font-semibold text-gray-400 mb-1">Hali hech qanday kurs boshlanmagan</h3>
        <p class="text-sm text-gray-400 mb-5">O'rganishni boshlash uchun kurs tanlang</p>
        <RouterLink
          to="/dashboard/courses"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold transition-colors shadow-sm"
        >
          Kurslarga o'tish
        </RouterLink>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { Award, BookOpen, CheckCircle, TrendingUp, PlayCircle } from 'lucide-vue-next'

import { useAuthStore }    from '@/stores/auth.js'
import { useCoursesStore } from '@/stores/courses.js'
import { getAllCertificates } from '@/api/certificate.js'
import CourseCard    from '@/components/student/CourseCard.vue'
import AppSkeleton  from '@/components/ui/AppSkeleton.vue'
import AppAlert     from '@/components/ui/AppAlert.vue'
import AppButton    from '@/components/ui/AppButton.vue'

const authStore    = useAuthStore()
const coursesStore = useCoursesStore()

// Sertifikat statistikasi
const certCount  = ref(0)
const latestCert = ref(null)

// Foydalanuvchi ismi (birinchi so'z)
const firstName = computed(() =>
  authStore.user?.full_name?.split(' ')[0] || 'Foydalanuvchi'
)

// Davom etayotgan kurslar (max 3 ta dashboard da)
const inProgressSlice = computed(() =>
  coursesStore.inProgressCourses.slice(0, 3)
)

onMounted(async () => {
  coursesStore.fetchCourses()
  try {
    const { data } = await getAllCertificates()
    certCount.value = data.length
    latestCert.value = data[0] ?? null
  } catch {
    // sertifikat bo'lmasa — 0 ko'rinadi
  }
})
</script>
