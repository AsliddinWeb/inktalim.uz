<template>
  <section id="courses" class="py-20 bg-white dark:bg-gray-950">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <!-- ─── Sarlavha ────────────────────────────────────────────────── -->
      <div class="text-center mb-12 section-header">
        <span class="inline-block px-4 py-1.5 text-xs font-bold uppercase tracking-widest rounded-full mb-4
                     bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400
                     border border-primary-200 dark:border-primary-800">
          Kurslar
        </span>
        <h2 class="text-3xl sm:text-4xl font-black text-gray-900 dark:text-white mb-4">
          Bizning kurslarimiz
        </h2>
        <p class="text-gray-500 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
          Zamonaviy texnologiyalar bo'yicha professional kurslar. Hamma kurslar O'zbek tilida va to'liq bepul.
        </p>
      </div>

      <!-- ─── Skeleton loading ───────────────────────────────────────── -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="i in 3"
          :key="i"
          class="rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-900"
        >
          <div class="h-44 bg-gray-200 dark:bg-gray-800 animate-pulse" />
          <div class="p-5 space-y-3">
            <div class="h-4 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-lg w-3/4" />
            <div class="h-3 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-lg" />
            <div class="h-3 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-lg w-5/6" />
          </div>
        </div>
      </div>

      <!-- ─── Kurslar grid ────────────────────────────────────────────── -->
      <div
        v-else-if="visibleCourses.length"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <div
          v-for="(course, i) in visibleCourses"
          :key="course.id"
          class="group rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800
                 bg-white dark:bg-gray-900
                 hover:border-primary-200 dark:hover:border-primary-800
                 hover:shadow-[0_8px_32px_rgba(108,99,255,0.15)]
                 transition-all duration-300 course-card"
          :style="`animation-delay: ${i * 0.07}s`"
        >
          <!-- Thumbnail -->
          <div class="relative h-44 overflow-hidden bg-gray-100 dark:bg-gray-800">
            <img
              v-if="course.thumbnail_url"
              :src="thumbnailUrl(course.thumbnail_url)"
              :alt="course.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <div
              v-else
              class="w-full h-full gradient-primary flex items-center justify-center"
            >
              <BookOpen class="w-10 h-10 text-white/60" />
            </div>

            <!-- "Bepul" badge -->
            <div class="absolute top-3 left-3">
              <span class="px-2.5 py-1 text-xs font-bold rounded-lg
                           bg-green-500 text-white shadow-sm">
                Bepul
              </span>
            </div>
          </div>

          <!-- Kontent -->
          <div class="p-5 flex flex-col flex-1">
            <h3 class="font-bold text-gray-900 dark:text-white mb-2 line-clamp-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
              {{ course.title }}
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed line-clamp-3 mb-4 flex-1">
              {{ course.description }}
            </p>

            <!-- Darslar soni -->
            <div class="flex items-center gap-1.5 text-xs text-gray-400 mb-4">
              <PlayCircle class="w-3.5 h-3.5" />
              <span>{{ course.lessons_count ?? 0 }} ta dars</span>
            </div>

            <!-- Tugma -->
            <component
              :is="isAuthenticated ? RouterLink : RouterLink"
              :to="isAuthenticated ? `/dashboard/courses/${course.id}` : '/register'"
              class="flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-semibold rounded-xl
                     bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400
                     hover:bg-primary-500 hover:text-white dark:hover:bg-primary-500 dark:hover:text-white
                     border border-primary-200 dark:border-primary-800 hover:border-transparent
                     transition-all duration-200 group/btn"
            >
              <span>{{ isAuthenticated ? 'Kursga o\'tish' : 'Kursni boshlash' }}</span>
              <ArrowRight class="w-4 h-4 transition-transform group-hover/btn:translate-x-0.5" />
            </component>
          </div>
        </div>
      </div>

      <!-- ─── Bo'sh holat ─────────────────────────────────────────────── -->
      <div v-else class="text-center py-16">
        <BookOpen class="w-12 h-12 text-gray-300 dark:text-gray-700 mx-auto mb-3" />
        <p class="text-gray-400 dark:text-gray-600">Hozircha kurslar mavjud emas</p>
      </div>

      <!-- ─── "Barcha kurslar" tugmasi ───────────────────────────────── -->
      <div v-if="hasMore" class="text-center mt-10">
        <RouterLink
          :to="isAuthenticated ? '/dashboard/courses' : '/register'"
          class="inline-flex items-center gap-2 px-7 py-3 text-sm font-semibold rounded-2xl
                 border border-primary-300 dark:border-primary-700
                 text-primary-700 dark:text-primary-400
                 hover:bg-primary-500 hover:text-white hover:border-transparent
                 dark:hover:bg-primary-500 dark:hover:text-white
                 transition-all duration-200"
        >
          Barcha kurslarni ko'rish
          <ArrowRight class="w-4 h-4" />
        </RouterLink>
      </div>

    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowRight, BookOpen, PlayCircle } from 'lucide-vue-next'

const props = defineProps({
  courses: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const MAX_VISIBLE = 6

const isAuthenticated = computed(() => !!localStorage.getItem('edu-access-token'))

const visibleCourses = computed(() => props.courses.slice(0, MAX_VISIBLE))
const hasMore = computed(() => props.courses.length > MAX_VISIBLE)

function thumbnailUrl(path) {
  if (!path) return null
  if (path.startsWith('http')) return path
  const base = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1')
    .replace('/api/v1', '')
  return `${base}${path}`
}
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.section-header {
  animation: fadeInUp 0.6s ease both;
}
.course-card {
  animation: fadeInUp 0.55s ease both;
}
</style>
