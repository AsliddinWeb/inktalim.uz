<template>
  <div class="inline-flex items-center gap-0.5 rounded-xl bg-gray-100 dark:bg-gray-800 p-0.5">
    <button
      @click="store.decrease()"
      :disabled="!store.canDecrease()"
      class="w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold text-gray-500 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-transparent"
      aria-label="Shriftni kichiklashtirish"
    >
      A-
    </button>
    <button
      @click="store.increase()"
      :disabled="!store.canIncrease()"
      class="w-7 h-7 rounded-lg flex items-center justify-center text-sm font-bold text-gray-500 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-transparent"
      aria-label="Shriftni kattalashtirish"
    >
      A+
    </button>
  </div>
</template>

<script setup>
import { useFontSizeStore } from '@/stores/fontSize.js'

const store = useFontSizeStore()
</script>
