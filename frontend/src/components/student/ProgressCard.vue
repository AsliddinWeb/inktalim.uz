<template>
  <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6 flex items-center gap-6 hover:shadow-md transition-shadow duration-200">

    <!-- SVG doira progress (88px) -->
    <div class="flex-shrink-0" style="width:88px;height:88px">
      <svg width="88" height="88" viewBox="0 0 88 88" fill="none">
        <!-- Track -->
        <circle
          cx="44" cy="44" r="38"
          stroke-width="8"
          class="stroke-gray-100 dark:stroke-gray-800"
          fill="none"
        />
        <!-- Progress -->
        <circle
          cx="44" cy="44" r="38"
          stroke-width="8"
          stroke-linecap="round"
          fill="none"
          :stroke="circleColor"
          transform="rotate(-90 44 44)"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="dashOffset"
          style="transition: stroke-dashoffset 0.5s ease"
        />
        <!-- Center text -->
        <text
          x="44" y="44"
          text-anchor="middle"
          dominant-baseline="central"
          style="font-size:14px;font-weight:800"
          class="fill-gray-900 dark:fill-white"
        >{{ progress.progress_percent ?? 0 }}%</text>
      </svg>
    </div>

    <!-- Right: info -->
    <div class="flex-1 min-w-0">
      <h4 class="text-base font-semibold text-gray-900 dark:text-white mb-1 line-clamp-2">
        {{ progress.course_title }}
      </h4>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">
        {{ progress.completed_lessons ?? 0 }} ta darsdan
        {{ progress.total_lessons ?? 0 }} tasi tugallandi
      </p>
      <AppProgress :value="progress.progress_percent ?? 0" size="sm" />
      <RouterLink
        :to="`/dashboard/courses/${progress.course_id}`"
        class="mt-3 inline-flex items-center gap-1 text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
      >
        Kursni ko'rish
        <ArrowRight class="size-4" />
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Check, ArrowRight } from 'lucide-vue-next'
import AppProgress from '@/components/ui/AppProgress.vue'

const props = defineProps({
  progress: {
    type: Object,
    required: true,
  },
})

// SVG doira hisob-kitoblari
const radius = 40
const circumference = 2 * Math.PI * radius

const dashOffset = computed(() =>
  circumference - (props.progress.progress_percent / 100) * circumference
)

const circleColor = computed(() =>
  props.progress.progress_percent === 100 ? '#10B981' : '#6C63FF'
)
</script>
