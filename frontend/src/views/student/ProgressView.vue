<template>
  <div class="space-y-6">

    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Mening progressim</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">O'rganish natijalari</p>
    </div>

    <!-- Error -->
    <div v-if="progressStore.errorAll" class="rounded-xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 px-4 py-3">
      <p class="text-sm font-medium text-danger-600 dark:text-danger-400">{{ progressStore.errorAll }}</p>
    </div>

    <!-- Loading -->
    <template v-if="progressStore.loadingAll">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div v-for="i in 3" :key="i" class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-5 animate-pulse">
          <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full w-1/2 mb-3" />
          <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded-lg w-1/3" />
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="i in 4" :key="i" class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-5 h-28 animate-pulse" />
      </div>
    </template>

    <template v-else>
      <!-- Stats row -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-5">
          <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">Boshlangan kurslar</p>
          <p class="text-3xl font-black text-primary-600 dark:text-primary-400">
            {{ progressStore.startedCoursesCount }}
          </p>
        </div>
        <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-5">
          <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">O'rtacha progress</p>
          <p class="text-3xl font-black text-secondary-600 dark:text-secondary-400">
            {{ progressStore.averageProgress }}%
          </p>
        </div>
        <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-5">
          <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">Tugatilgan kurslar</p>
          <p class="text-3xl font-black text-success-600 dark:text-success-400">
            {{ progressStore.completedCoursesCount }}
          </p>
        </div>
      </div>

      <!-- Progress cards grid -->
      <div
        v-if="progressStore.allProgress.length"
        class="grid grid-cols-1 md:grid-cols-2 gap-4"
      >
        <ProgressCard
          v-for="item in progressStore.allProgress"
          :key="item.course_id"
          :progress="item"
        />
      </div>

      <!-- Empty state -->
      <div
        v-else
        class="rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700 p-16 text-center"
      >
        <TrendingUp class="w-12 h-12 text-gray-200 dark:text-gray-700 mx-auto mb-4" />
        <h3 class="text-base font-semibold text-gray-400 mb-1">Hali hech qanday kurs boshlanmagan</h3>
        <p class="text-sm text-gray-400 mb-5">Birinchi kursni boshlaganingizdan keyin progress shu yerda ko'rinadi</p>
        <RouterLink
          to="/dashboard/courses"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold transition-all shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0"
        >
          <BookOpen class="w-4 h-4" />
          Kurslarga o'tish
        </RouterLink>
      </div>
    </template>

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { TrendingUp, BookOpen } from 'lucide-vue-next'

import { useProgressStore } from '@/stores/progress.js'
import ProgressCard from '@/components/student/ProgressCard.vue'
import AppAlert     from '@/components/ui/AppAlert.vue'
import AppButton    from '@/components/ui/AppButton.vue'
import AppSkeleton  from '@/components/ui/AppSkeleton.vue'

const progressStore = useProgressStore()

onMounted(() => {
  progressStore.fetchAllProgress()
})
</script>
