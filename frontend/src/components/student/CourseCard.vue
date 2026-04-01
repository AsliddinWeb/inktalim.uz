<template>
  <RouterLink
    :to="`/dashboard/courses/${course.id}`"
    class="group flex flex-col rounded-2xl overflow-hidden border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface shadow-sm hover:shadow-xl hover:shadow-primary-500/10 hover:-translate-y-1.5 transition-all duration-300"
  >
    <!-- Thumbnail -->
    <div class="relative aspect-video overflow-hidden bg-gray-100 dark:bg-gray-800 flex-shrink-0">
      <img
        v-if="course.thumbnail_url"
        :src="getMediaUrl(course.thumbnail_url)"
        :alt="course.title"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      <div v-else class="w-full h-full gradient-primary flex items-center justify-center">
        <BookOpen class="w-10 h-10 text-white/50" />
      </div>
    </div>

    <!-- Content -->
    <div class="p-5 flex flex-col flex-1">
      <h3 class="text-base font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors leading-snug">
        {{ course.title }}
      </h3>

      <!-- Progress area -->
      <div class="mt-auto pt-3 border-t border-gray-50 dark:border-gray-800/80">
        <div class="flex justify-between items-center mb-1.5">
          <span class="text-xs text-gray-400 dark:text-gray-500">
            {{ course.completed_lessons ?? 0 }}/{{ course.lessons_count ?? 0 }} dars
          </span>
          <span class="text-xs font-bold text-primary-600 dark:text-primary-400">
            {{ course.progress_percent ?? 0 }}%
          </span>
        </div>
        <AppProgress :value="course.progress_percent ?? 0" size="sm" />
      </div>

      <!-- Button -->
      <button
        class="mt-3 w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200"
        :class="buttonClass"
      >
        {{ buttonLabel }}
        <Check v-if="course.progress_percent === 100" class="size-4" />
      </button>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { BookOpen, Check } from 'lucide-vue-next'
import AppProgress from '@/components/ui/AppProgress.vue'
import { getMediaUrl } from '@/api/upload.js'

const props = defineProps({
  course: {
    type: Object,
    required: true,
  },
})

// Tugma matni — progress ga qarab
const buttonLabel = computed(() => {
  if (props.course.progress_percent === 100) return '✓ Tugatildi'
  if (props.course.is_enrolled) return 'Davom etish →'
  return 'Boshlash'
})

// Tugma rangi
const buttonClass = computed(() => {
  if (props.course.progress_percent === 100) {
    return 'bg-success-50 text-success-700 dark:bg-success-900/30 dark:text-success-400'
  }
  if (props.course.is_enrolled) {
    return 'bg-primary-500 text-white hover:bg-primary-600 shadow-sm hover:shadow-md hover:-translate-y-0.5'
  }
  return 'bg-primary-50 text-primary-700 hover:bg-primary-500 hover:text-white dark:bg-primary-900/20 dark:text-primary-400 dark:hover:bg-primary-500 dark:hover:text-white border border-primary-200 dark:border-primary-800 hover:border-transparent'
})
</script>
