<template>
  <div
    v-if="totalPages > 1"
    class="flex items-center justify-between gap-4 flex-wrap"
  >
    <!-- Ma'lumot -->
    <p class="text-sm text-app-secondary">
      Jami: <span class="font-semibold text-app-primary">{{ total }}</span> ta yozuv,
      {{ currentPage }}/{{ totalPages }} sahifa
    </p>

    <!-- Tugmalar -->
    <div class="flex items-center gap-1">
      <!-- Oldingi -->
      <button
        :disabled="currentPage <= 1"
        class="rounded-xl w-9 h-9 flex items-center justify-center border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        aria-label="Oldingi sahifa"
        @click="emit('change', currentPage - 1)"
      >
        <ChevronLeft class="size-4" />
      </button>

      <!-- Sahifa raqamlari -->
      <template v-for="page in visiblePages" :key="page">
        <!-- Ellipsis -->
        <span
          v-if="page === '...'"
          class="px-2 text-gray-400 text-sm select-none"
        >…</span>

        <!-- Raqam -->
        <button
          v-else
          class="rounded-xl w-9 h-9 flex items-center justify-center border text-sm font-medium transition-colors"
          :class="
            page === currentPage
              ? 'bg-primary-500 text-white border-primary-500 font-semibold shadow-sm'
              : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-surface hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400'
          "
          @click="emit('change', page)"
        >
          {{ page }}
        </button>
      </template>

      <!-- Keyingi -->
      <button
        :disabled="currentPage >= totalPages"
        class="rounded-xl w-9 h-9 flex items-center justify-center border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        aria-label="Keyingi sahifa"
        @click="emit('change', currentPage + 1)"
      >
        <ChevronRight class="size-4" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  total: { type: Number, default: 0 },
  perPage: { type: Number, default: 10 },
  currentPage: { type: Number, default: 1 },
})

const emit = defineEmits(['change'])

const totalPages = computed(() => Math.ceil(props.total / props.perPage))

// Ko'rinadigan sahifa raqamlari (ellipsis bilan)
const visiblePages = computed(() => {
  const total = totalPages.value
  const current = props.currentPage
  const pages = []

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }

  pages.push(1)

  if (current > 3) pages.push('...')

  const start = Math.max(2, current - 1)
  const end   = Math.min(total - 1, current + 1)

  for (let i = start; i <= end; i++) pages.push(i)

  if (current < total - 2) pages.push('...')

  pages.push(total)
  return pages
})
</script>
