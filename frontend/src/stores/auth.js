// Auth store — foydalanuvchi autentifikatsiyasi holati
// localStorage da tokenlar va user ma'lumotlari saqlanadi

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios.js'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()

  // ─── State ───────────────────────────────────────────────────────────────

  // Foydalanuvchi ma'lumotlari (localStorage dan tiklanadi)
  const user = ref(
    JSON.parse(localStorage.getItem('edu-user') || 'null')
  )

  // JWT tokenlar
  const accessToken = ref(localStorage.getItem('edu-access-token') || null)
  const refreshToken = ref(localStorage.getItem('edu-refresh-token') || null)

  // Yuklash holati
  const loading = ref(false)
  const error = ref(null)

  // ─── Computed ─────────────────────────────────────────────────────────────

  // Autentifikatsiya qilinganmi?
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

  // Admin rolidami?
  const isAdmin = computed(() => user.value?.is_admin === true)

  // ─── Yordamchi funksiyalar ────────────────────────────────────────────────

  /**
   * Tokenlarni saqlash — state va localStorage ga
   */
  function _saveTokens(access, refresh) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('edu-access-token', access)
    localStorage.setItem('edu-refresh-token', refresh)
  }

  /**
   * Foydalanuvchi ma'lumotlarini saqlash
   */
  function _saveUser(userData) {
    user.value = userData
    localStorage.setItem('edu-user', JSON.stringify(userData))
  }

  /**
   * Barcha auth ma'lumotlarni tozalash
   */
  function _clearAuth() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('edu-access-token')
    localStorage.removeItem('edu-refresh-token')
    localStorage.removeItem('edu-user')
  }

  // ─── Actions ──────────────────────────────────────────────────────────────

  /**
   * Tizimga kirish — email yoki telefon bilan
   * @param {Object} credentials - { login, password }
   */
  async function login(credentials) {
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/login', credentials)
      const { access_token, refresh_token } = response.data

      _saveTokens(access_token, refresh_token)

      // Foydalanuvchi ma'lumotlarini olish
      await fetchMe()

      // Rolga qarab yo'naltirish
      if (user.value?.is_admin) {
        router.push('/admin')
      } else {
        router.push('/dashboard')
      }

      return { success: true }
    } catch (err) {
      const message = err.response?.data?.detail || 'Kirish muvaffaqiyatsiz tugadi.'
      error.value = message
      return { success: false, error: message }
    } finally {
      loading.value = false
    }
  }

  /**
   * Yangi foydalanuvchi ro'yxatdan o'tkazish
   * @param {Object} data - { full_name, email, phone, password }
   */
  async function register(data) {
    loading.value = true
    error.value = null

    try {
      await api.post('/auth/register', data)
      // Ro'yxatdan keyin avtomatik login
      return await login({ login: data.email, password: data.password })
    } catch (err) {
      const message = err.response?.data?.detail || 'Ro\'yxatdan o\'tish muvaffaqiyatsiz.'
      error.value = message
      return { success: false, error: message }
    } finally {
      loading.value = false
    }
  }

  /**
   * Tizimdan chiqish
   */
  async function logout() {
    _clearAuth()
    await router.push('/login')
  }

  /**
   * Joriy foydalanuvchi ma'lumotlarini API dan yangilash
   */
  async function fetchMe() {
    try {
      const response = await api.get('/auth/me')
      _saveUser(response.data)
    } catch {
      // Token eskirgan bo'lsa auth tozalanadi
      _clearAuth()
    }
  }

  /**
   * Xato xabarini tozalash
   */
  function clearError() {
    error.value = null
  }

  return {
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    fetchMe,
    clearError,
  }
})
