// Tema store — dark/light mode holati va boshqaruvi
// localStorage dan o'qiydi, document.documentElement ga 'dark' class qo'shadi

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // ─── State ───────────────────────────────────────────────────────────────

  // localStorage da saqlangan tema (default: light)
  const isDark = ref(
    localStorage.getItem('edu-theme') === 'dark' ||
    // Foydalanuvchi tizim sozlamasini ham hisobga olish
    (!localStorage.getItem('edu-theme') &&
      window.matchMedia('(prefers-color-scheme: dark)').matches)
  )

  // ─── Computed ─────────────────────────────────────────────────────────────

  const currentTheme = computed(() => isDark.value ? 'dark' : 'light')

  // ─── Actions ──────────────────────────────────────────────────────────────

  /**
   * Tema o'zgartirish — dark ↔ light toggle
   */
  function toggleTheme() {
    isDark.value = !isDark.value
    applyTheme()
  }

  /**
   * Hozirgi tema holatini DOM ga qo'llash.
   * App yuklanganda va toggle paytida chaqiriladi.
   */
  function applyTheme() {
    const html = document.documentElement

    if (isDark.value) {
      html.classList.add('dark')
      localStorage.setItem('edu-theme', 'dark')
    } else {
      html.classList.remove('dark')
      localStorage.setItem('edu-theme', 'light')
    }
  }

  /**
   * Aniq temani o'rnatish
   */
  function setTheme(dark) {
    isDark.value = dark
    applyTheme()
  }

  return {
    isDark,
    currentTheme,
    toggleTheme,
    applyTheme,
    setTheme,
  }
})
