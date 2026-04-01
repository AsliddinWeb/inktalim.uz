// Fayl yuklash API — thumbnail va avatar
// FormData bilan multipart/form-data so'rovlari

import api from '@/api/axios.js'

// Backend manzili (VITE_API_URL = "http://localhost:8000/api/v1")
// Media URL uchun /api/v1 qismini olib tashlaymiz
const MEDIA_BASE = import.meta.env.VITE_API_URL
  ? import.meta.env.VITE_API_URL.replace(/\/api\/v1\/?$/, '')
  : 'http://localhost:8000'


/**
 * Nisbiy media yo'ldan to'liq URL yaratish.
 *
 * @param {string|null} path  — "/media/thumbnails/uuid.jpg" yoki to'liq URL
 * @returns {string|null}     — "http://localhost:8000/media/thumbnails/uuid.jpg"
 *
 * @example
 * getMediaUrl("/media/avatars/abc.jpg")
 * // → "http://localhost:8000/media/avatars/abc.jpg"
 *
 * getMediaUrl("https://cdn.example.com/img.jpg")
 * // → "https://cdn.example.com/img.jpg"  (o'zgarmaydi)
 */
export function getMediaUrl(path) {
  if (!path) return null
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  return MEDIA_BASE + path
}


/**
 * Kurs thumbnail rasmini yuklash (faqat admin).
 *
 * @param {File} file              — brauzerdan tanlangan fayl
 * @param {Function} [onProgress]  — yuklash jarayonida (percent: number) → void
 * @returns {Promise<{ url: string }>}
 */
export async function uploadThumbnail(file, onProgress) {
  const form = new FormData()
  form.append('file', file)

  const response = await api.post('/upload/thumbnail', form, {
    onUploadProgress: (event) => {
      if (onProgress && event.total) {
        onProgress(Math.round((event.loaded / event.total) * 100))
      }
    },
  })
  return response.data
}


/**
 * Foydalanuvchi avatarini yuklash.
 * Backend avatarni saqlaydi va user.avatar_url ni yangilaydi.
 *
 * @param {File} file              — brauzerdan tanlangan fayl
 * @param {Function} [onProgress]  — yuklash jarayonida (percent: number) → void
 * @returns {Promise<{ url: string, user: object }>}
 */
export async function uploadAvatar(file, onProgress) {
  const form = new FormData()
  form.append('file', file)

  const response = await api.post('/upload/avatar', form, {
    onUploadProgress: (event) => {
      if (onProgress && event.total) {
        onProgress(Math.round((event.loaded / event.total) * 100))
      }
    },
  })
  return response.data
}


/**
 * Thumbnail rasmini o'chirish (faqat admin).
 *
 * @param {string} filename — "uuid.jpg" (yo'lsiz, faqat fayl nomi)
 * @returns {Promise<{ message: string }>}
 */
export async function deleteThumbnail(filename) {
  const response = await api.delete(`/upload/thumbnail/${filename}`)
  return response.data
}
