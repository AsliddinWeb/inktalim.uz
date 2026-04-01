<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Kurslar</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Jami {{ coursesStore.courses.length }} ta kurs mavjud
        </p>
      </div>
    </div>

    <!-- Search bar -->
    <div class="bg-white dark:bg-surface rounded-2xl border border-gray-100 dark:border-gray-800 p-4 flex flex-col sm:flex-row gap-3">
      <div class="relative flex-1">
        <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 size-4 text-gray-400 pointer-events-none" />
        <input
          v-model="searchQuery"
          type="search"
          placeholder="Kurs qidirish..."
          class="w-full h-11 pl-10 pr-4 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-xl text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all duration-200"
        />
      </div>
      <button
        v-if="searchQuery"
        type="button"
        class="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        @click="searchQuery = ''"
      >
        <X class="size-4" />
        Tozalash
      </button>
    </div>

    <!-- Loading -->
    <div v-if="coursesStore.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="i in 6"
        :key="i"
        class="rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden animate-pulse"
      >
        <div class="aspect-video bg-gray-200 dark:bg-gray-800" />
        <div class="p-5 space-y-3">
          <div class="h-4 bg-gray-200 dark:bg-gray-800 rounded-lg w-3/4" />
          <div class="h-3 bg-gray-200 dark:bg-gray-800 rounded-lg" />
          <div class="h-2.5 bg-gray-200 dark:bg-gray-800 rounded-full mt-4" />
          <div class="h-9 bg-gray-200 dark:bg-gray-800 rounded-xl mt-2" />
        </div>
      </div>
    </div>

    <!-- Error -->
    <AppAlert v-else-if="coursesStore.error" type="error">
      {{ coursesStore.error }}
    </AppAlert>

    <!-- Course grid -->
    <div
      v-else-if="filteredCourses.length"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5"
    >
      <CourseCard
        v-for="course in filteredCourses"
        :key="course.id"
        :course="course"
      />
    </div>

    <!-- Empty search result -->
    <div v-else-if="searchQuery" class="text-center py-16">
      <Search class="w-12 h-12 text-gray-200 dark:text-gray-700 mx-auto mb-3" />
      <h3 class="text-base font-semibold text-gray-400 mb-1">"{{ searchQuery }}" bo'yicha natija topilmadi</h3>
      <button
        type="button"
        class="mt-4 text-sm text-primary-500 hover:text-primary-600 font-medium transition-colors"
        @click="searchQuery = ''"
      >
        Qidiruvni tozalash
      </button>
    </div>

    <!-- Empty all -->
    <div v-else class="text-center py-16">
      <BookOpen class="w-12 h-12 text-gray-200 dark:text-gray-700 mx-auto mb-3" />
      <h3 class="text-base font-semibold text-gray-400">Hali kurslar mavjud emas</h3>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { BookOpen, Search, X } from 'lucide-vue-next'

import { useCoursesStore } from '@/stores/courses.js'
import CourseCard   from '@/components/student/CourseCard.vue'
import AppBadge     from '@/components/ui/AppBadge.vue'
import AppSkeleton  from '@/components/ui/AppSkeleton.vue'
import AppAlert     from '@/components/ui/AppAlert.vue'

const coursesStore = useCoursesStore()

// Qidiruv so'zi
const searchQuery = ref('')

// Frontend side filter — kurs nomi bo'yicha
const filteredCourses = computed(() => {
  if (!searchQuery.value.trim()) return coursesStore.courses
  const q = searchQuery.value.toLowerCase()
  return coursesStore.courses.filter(c =>
    c.title.toLowerCase().includes(q) ||
    c.description.toLowerCase().includes(q)
  )
})

onMounted(() => {
  coursesStore.fetchCourses()
})
</script>
