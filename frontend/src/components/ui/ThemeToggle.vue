<template>
  <button
    @click="themeStore.toggleTheme()"
    class="w-9 h-9 rounded-xl flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-200"
    aria-label="Mavzuni o'zgartirish"
  >
    <SunMedium v-if="themeStore.isDark" class="size-5 transition-transform duration-300 rotate-0 hover:rotate-12" />
    <Moon v-else class="size-5 transition-transform duration-300" />
  </button>
</template>

<script setup>
import { SunMedium, Moon } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme.js'

const themeStore = useThemeStore()
</script>
