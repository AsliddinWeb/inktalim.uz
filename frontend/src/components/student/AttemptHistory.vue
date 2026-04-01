<template>
  <div v-if="history?.attempts?.length" class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface overflow-hidden">

    <!-- Accordion header -->
    <button
      type="button"
      class="w-full flex items-center justify-between px-5 py-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
      @click="open = !open"
    >
      <div class="flex items-center gap-2.5">
        <History class="size-4 text-gray-400" />
        <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">Urinishlar tarixi</span>
        <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">
          {{ history.attempts.length }}
        </span>
      </div>
      <ChevronDown
        class="size-4 text-gray-400 transition-transform duration-200"
        :class="open ? 'rotate-180' : ''"
      />
    </button>

    <!-- Attempts list -->
    <div v-show="open" class="divide-y divide-gray-100 dark:divide-gray-800">
      <div
        v-for="(attempt, i) in history.attempts"
        :key="i"
        class="flex items-center justify-between px-5 py-3.5"
      >
        <span class="text-xs text-gray-400 dark:text-gray-500">
          {{ formatDate(attempt.completed_at) }}
        </span>
        <span
          class="rounded-full px-3 py-1 text-sm font-bold"
          :class="attempt.is_passed
            ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
            : 'bg-danger-100 dark:bg-danger-900/20 text-danger-700 dark:text-danger-400'"
        >
          {{ attempt.score_percent ?? 0 }}%
        </span>
        <span
          class="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold"
          :class="attempt.is_passed
            ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
            : 'bg-danger-100 dark:bg-danger-900/20 text-danger-700 dark:text-danger-400'"
        >
          {{ attempt.is_passed ? "O'tdi" : "O'tmadi" }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { History, ChevronDown } from 'lucide-vue-next'

defineProps({
  history: { type: Object, default: null },
})

const open = ref(false)

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString('uz-UZ', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
