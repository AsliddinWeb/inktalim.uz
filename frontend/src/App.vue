<template>
  <!-- RouterView — joriy route komponenti shu yerda ko'rsatiladi -->
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
import { useThemeStore } from '@/stores/theme.js'

// Tema store ni ishga tushirish — sahifa yuklanganda dark/light mode apply qiladi
const themeStore = useThemeStore()
themeStore.applyTheme()
</script>
