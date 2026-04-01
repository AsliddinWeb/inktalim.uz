<template>
  <button
    type="button"
    class="flex items-center gap-3 px-4 py-3 w-full text-left transition-colors duration-150 cursor-pointer"
    :class="itemClass"
    @click="$emit('click')"
  >
    <!-- Status indicator -->
    <div
      class="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-xs font-bold transition-colors"
      :class="numberClass"
    >
      <CheckCircle v-if="lesson.is_completed" class="size-4" />
      <span v-else>{{ lesson.order ?? '•' }}</span>
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <p class="text-sm font-medium leading-snug line-clamp-2">
        {{ lesson.title }}
      </p>
      <p v-if="lesson.duration" class="text-xs text-gray-400 dark:text-gray-500 mt-0.5 flex items-center gap-1">
        <Clock class="size-3" />
        {{ lesson.duration }}
      </p>
    </div>

    <!-- Quiz indicator -->
    <FileQuestion
      v-if="lesson.has_quiz"
      class="size-4 text-primary-400 dark:text-primary-500 flex-shrink-0 ml-auto"
    />
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { CheckCircle, Clock, FileQuestion } from 'lucide-vue-next'

defineEmits(['click'])

const props = defineProps({
  lesson: {
    type: Object,
    required: true,
  },
  // Joriy ko'rilayotgan dars
  active: {
    type: Boolean,
    default: false,
  },
})

// Element umumiy klassi
const itemClass = computed(() => {
  if (props.active) {
    return 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 border-r-2 border-primary-500'
  }
  return 'hover:bg-gray-50 dark:hover:bg-gray-800/60 text-gray-700 dark:text-gray-300'
})

// Raqam doirasi klassi
const numberClass = computed(() => {
  if (props.lesson.is_completed) {
    return 'bg-success-100 dark:bg-success-900/20 text-success-600'
  }
  if (props.active) {
    return 'bg-primary-500 text-white shadow-sm'
  }
  return 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400'
})
</script>
