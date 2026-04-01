// Axios instance — barcha API so'rovlari uchun markaziy konfiguratsiya
// Request interceptor: Bearer token qo'shish
// Response interceptor: 401 da refresh token bilan yangilash

import axios from 'axios'

// Asosiy API URL — .env dan olinadi
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 15000, // 15 sekund kutish vaqti
})

// ─── Request Interceptor ─────────────────────────────────────────────────────
// Har bir so'rovga Authorization headerini qo'shish

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('edu-access-token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ─── Response Interceptor ─────────────────────────────────────────────────────
// 401 xatosida refresh token bilan yangi access token olish

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  // Muvaffaqiyatli javob — o'zgartirishsiz qaytarish
  (response) => response,

  // Xato javob
  async (error) => {
    const originalRequest = error.config

    // 401 xatosi va bu allaqachon retry so'rovi emas
    if (error.response?.status === 401 && !originalRequest._retry) {
      // Refresh token mavjudmi?
      const refreshToken = localStorage.getItem('edu-refresh-token')

      if (!refreshToken) {
        // Refresh token yo'q — logout
        _forceLogout()
        return Promise.reject(error)
      }

      // Yangilanish jarayoni allaqachon bormi?
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        // Yangi access token olish
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/auth/refresh`,
          { refresh_token: refreshToken }
        )

        const { access_token, refresh_token } = response.data

        // Yangi tokenlarni saqlash
        localStorage.setItem('edu-access-token', access_token)
        localStorage.setItem('edu-refresh-token', refresh_token)

        // Keyingi so'rovlar uchun header yangilash
        api.defaults.headers.common.Authorization = `Bearer ${access_token}`
        originalRequest.headers.Authorization = `Bearer ${access_token}`

        processQueue(null, access_token)
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh ham muvaffaqiyatsiz — logout
        processQueue(refreshError, null)
        _forceLogout()
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

// Majburiy logout — tokenlar o'chiriladi, login sahifaga yo'naltiriladi
function _forceLogout() {
  localStorage.removeItem('edu-access-token')
  localStorage.removeItem('edu-refresh-token')
  localStorage.removeItem('edu-user')
  // Router import qilmasdan to'g'ridan-to'g'ri yo'naltirish
  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

export default api
