<template>
  <div class="w-full">
    <!-- Label qatori -->
    <div v-if="label && !showLabel" class="mb-1.5">
      <span class="text-xs font-medium text-app-secondary">{{ label }}</span>
    </div>

    <!-- Bar + label (inline) -->
    <div :class="showLabel ? 'flex items-center gap-3' : ''">
      <!-- Track -->
      <div
        :class="[
          showLabel ? 'flex-1' : 'w-full',
          'bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden',
          trackSizes[size],
        ]"
        role="progressbar"
        :aria-valuenow="value"
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <!-- Fill -->
        <div
          class="bg-gradient-to-r from-primary-600 to-primary-400 h-full rounded-full transition-all duration-500 ease-out"
          :style="{ width: `${Math.min(Math.max(value, 0), 100)}%` }"
        />
      </div>

      <!-- Label foiz -->
      <span
        v-if="showLabel"
        class="text-sm font-semibold text-primary-600 dark:text-primary-400 min-w-[3rem] text-right"
      >
        {{ Math.round(value) }}%
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // Foiz qiymati (0–100)
  value: {
    type: Number,
    default: 0,
  },
  // Rang
  color: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'success', 'warning', 'danger'].includes(v),
  },
  // Balandlik
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  // Foiz yozuvini ko'rsatish
  showLabel: {
    type: Boolean,
    default: false,
  },
  // Chap tomon yozuv
  label: {
    type: String,
    default: '',
  },
})

const trackSizes = { sm: 'h-1.5', md: 'h-2.5', lg: 'h-4' }

const labelColors = {
  primary: 'text-primary-600 dark:text-primary-400',
  success: 'text-success-600 dark:text-success-400',
  warning: 'text-secondary-600 dark:text-secondary-400',
  danger:  'text-danger-600 dark:text-danger-400',
}

const labelColorClass = computed(() => labelColors[props.color])
</script>
