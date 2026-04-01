<template>
  <div class="space-y-6">

    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Platformaning umumiy holati</p>
    </div>

    <!-- Stat cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        :icon="BookOpen"
        label="Jami kurslar"
        :value="stats.totalCourses"
        :loading="loadingStats"
        icon-bg="bg-primary-100 dark:bg-primary-900/20"
        icon-color="text-primary-600 dark:text-primary-400"
      />
      <StatCard
        :icon="PlayCircle"
        label="Jami darslar"
        :value="stats.totalLessons"
        :loading="loadingStats"
        icon-bg="bg-secondary-100 dark:bg-secondary-900/20"
        icon-color="text-secondary-600 dark:text-secondary-400"
      />
      <StatCard
        :icon="Users"
        label="Foydalanuvchilar"
        :value="stats.totalUsers"
        :loading="loadingStats"
        icon-bg="bg-success-100 dark:bg-success-900/20"
        icon-color="text-success-600 dark:text-success-400"
      />
      <StatCard
        :icon="UserCheck"
        label="Faol foydalanuvchilar"
        :value="stats.activeUsers"
        :loading="loadingStats"
        icon-bg="bg-blue-100 dark:bg-blue-900/20"
        icon-color="text-blue-600 dark:text-blue-400"
      />
    </div>

    <!-- Courses + Users panels -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- Courses list -->
      <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-semibold text-gray-900 dark:text-white">Kurslar</h2>
          <RouterLink to="/admin/courses" class="text-xs text-primary-500 hover:text-primary-600 font-medium transition-colors">
            Barchasi →
          </RouterLink>
        </div>

        <div v-if="loadingStats" class="space-y-3">
          <div v-for="i in 4" :key="i" class="flex items-center gap-3 animate-pulse">
            <div class="w-8 h-8 bg-gray-200 dark:bg-gray-700 rounded-xl flex-shrink-0" />
            <div class="flex-1 space-y-1.5">
              <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-lg w-3/4" />
              <div class="h-2.5 bg-gray-100 dark:bg-gray-800 rounded-lg w-1/2" />
            </div>
          </div>
        </div>

        <div v-else-if="!stats.coursesList?.length" class="text-center py-8 text-sm text-gray-400">
          Hali kurs yo'q
        </div>

        <ul v-else class="space-y-3">
          <li v-for="course in stats.coursesList" :key="course.id" class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-xl bg-primary-50 dark:bg-primary-900/20 flex items-center justify-center flex-shrink-0">
              <BookOpen class="w-4 h-4 text-primary-500" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ course.title }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ course.lessons_count ?? 0 }} ta dars</p>
            </div>
            <span
              class="flex-shrink-0 inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold"
              :class="course.is_published
                ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400'"
            >
              {{ course.is_published ? 'Nashr' : 'Draft' }}
            </span>
          </li>
        </ul>
      </div>

      <!-- Recent users -->
      <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-semibold text-gray-900 dark:text-white">So'nggi foydalanuvchilar</h2>
          <RouterLink to="/admin/users" class="text-xs text-primary-500 hover:text-primary-600 font-medium transition-colors">
            Barchasi →
          </RouterLink>
        </div>

        <div v-if="loadingStats" class="space-y-3">
          <div v-for="i in 5" :key="i" class="flex items-center gap-3 animate-pulse">
            <div class="w-8 h-8 bg-gray-200 dark:bg-gray-700 rounded-full flex-shrink-0" />
            <div class="flex-1 space-y-1.5">
              <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-lg w-2/3" />
              <div class="h-2.5 bg-gray-100 dark:bg-gray-800 rounded-lg w-1/2" />
            </div>
          </div>
        </div>

        <div v-else-if="!stats.recentUsers?.length" class="text-center py-8 text-sm text-gray-400">
          Hali foydalanuvchi yo'q
        </div>

        <ul v-else class="space-y-3">
          <li v-for="user in stats.recentUsers" :key="user.id" class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/20 flex items-center justify-center flex-shrink-0">
              <span class="text-xs font-bold text-primary-600 dark:text-primary-400">
                {{ (user.full_name || user.email || '?')[0].toUpperCase() }}
              </span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ user.full_name || 'Ismsiz' }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ user.email }}</p>
            </div>
            <span
              class="flex-shrink-0 inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold"
              :class="user.is_active
                ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
                : 'bg-danger-100 dark:bg-danger-900/20 text-danger-700 dark:text-danger-400'"
            >
              {{ user.is_active ? 'Faol' : 'Bloklangan' }}
            </span>
          </li>
        </ul>
      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { BookOpen, PlayCircle, Users, UserCheck } from 'lucide-vue-next'
import { useAdminStore } from '@/stores/admin.js'
import { storeToRefs } from 'pinia'
import StatCard from '@/components/admin/StatCard.vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

const adminStore = useAdminStore()
const { stats, loadingStats } = storeToRefs(adminStore)

onMounted(() => adminStore.fetchStats())
</script>
