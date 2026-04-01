// Admin API — barcha admin endpointlari uchun chaqiruvlar
// Faqat is_admin=true foydalanuvchilar uchun

import api from '@/api/axios.js'

// ─── Kurslar ──────────────────────────────────────────────────────────────────

/**
 * Barcha kurslar ro'yxati (nashr qilingan va draft).
 * @param {Object} params - { skip, limit, published_only }
 */
export async function getCourses(params = {}) {
  const response = await api.get('/admin/courses', { params })
  return response.data
}

/**
 * Yangi kurs yaratish.
 * @param {Object} data - { title, description, thumbnail_url, is_published, order }
 */
export async function createCourse(data) {
  const response = await api.post('/admin/courses', data)
  return response.data
}

/**
 * Kursni yangilash.
 * @param {string} id   — kurs UUID
 * @param {Object} data — yangilash ma'lumotlari
 */
export async function updateCourse(id, data) {
  const response = await api.put(`/admin/courses/${id}`, data)
  return response.data
}

/**
 * Kursni o'chirish (cascade: barcha darslar ham o'chadi).
 * @param {string} id — kurs UUID
 */
export async function deleteCourse(id) {
  const response = await api.delete(`/admin/courses/${id}`)
  return response.data
}

/**
 * Kurs nashr holatini almashtirish (publish ↔ unpublish).
 * @param {string} id — kurs UUID
 */
export async function publishCourse(id) {
  const response = await api.patch(`/admin/courses/${id}/publish`)
  return response.data
}

/**
 * Kurslar tartibini yangilash.
 * @param {Array} items - [{ id, order }, ...]
 */
export async function reorderCourses(items) {
  const response = await api.put('/admin/courses/reorder', { items })
  return response.data
}

// ─── Modullar ─────────────────────────────────────────────────────────────────

export async function getModules(courseId) {
  const response = await api.get(`/admin/courses/${courseId}/modules`)
  return response.data
}

export async function createModule(courseId, data) {
  const response = await api.post(`/admin/courses/${courseId}/modules`, data)
  return response.data
}

export async function updateModule(courseId, moduleId, data) {
  const response = await api.put(`/admin/courses/${courseId}/modules/${moduleId}`, data)
  return response.data
}

export async function deleteModule(courseId, moduleId) {
  const response = await api.delete(`/admin/courses/${courseId}/modules/${moduleId}`)
  return response.data
}

export async function publishModule(courseId, moduleId) {
  const response = await api.patch(`/admin/courses/${courseId}/modules/${moduleId}/publish`)
  return response.data
}

export async function reorderModules(courseId, items) {
  const response = await api.put(`/admin/courses/${courseId}/modules/reorder`, { items })
  return response.data
}

// ─── Darslar ──────────────────────────────────────────────────────────────────

/**
 * Kursning barcha darslarini olish.
 * @param {string} courseId — kurs UUID
 */
export async function getLessons(courseId) {
  const response = await api.get(`/admin/courses/${courseId}/lessons`)
  return response.data
}

/**
 * Kursga yangi dars qo'shish.
 * @param {string} courseId — kurs UUID
 * @param {Object} data     — dars ma'lumotlari
 */
export async function createLesson(courseId, data) {
  const response = await api.post(`/admin/courses/${courseId}/lessons`, {
    ...data,
    course_id: courseId,
  })
  return response.data
}

/**
 * Darsni yangilash.
 * @param {string} courseId — kurs UUID
 * @param {string} lessonId — dars UUID
 * @param {Object} data     — yangilash ma'lumotlari
 */
export async function updateLesson(courseId, lessonId, data) {
  const response = await api.put(`/admin/courses/${courseId}/lessons/${lessonId}`, data)
  return response.data
}

/**
 * Darsni o'chirish.
 * @param {string} courseId — kurs UUID
 * @param {string} lessonId — dars UUID
 */
export async function deleteLesson(courseId, lessonId) {
  const response = await api.delete(`/admin/courses/${courseId}/lessons/${lessonId}`)
  return response.data
}

/**
 * Dars nashr holatini almashtirish.
 * @param {string} courseId — kurs UUID
 * @param {string} lessonId — dars UUID
 */
export async function publishLesson(courseId, lessonId) {
  const response = await api.patch(`/admin/courses/${courseId}/lessons/${lessonId}/publish`)
  return response.data
}

/**
 * Darslar tartibini yangilash.
 * @param {string} courseId — kurs UUID
 * @param {Array}  items    - [{ id, order }, ...]
 */
export async function reorderLessons(courseId, items) {
  const response = await api.put(`/admin/courses/${courseId}/lessons/reorder`, { items })
  return response.data
}

// ─── Foydalanuvchilar ─────────────────────────────────────────────────────────

/**
 * Foydalanuvchilar ro'yxati (pagination + search).
 * @param {Object} params - { skip, limit, search }
 */
export async function getUsers(params = {}) {
  const response = await api.get('/admin/users', { params })
  return response.data
}

/**
 * Bitta foydalanuvchi ma'lumotlari.
 * @param {string} id — foydalanuvchi UUID
 */
export async function getUser(id) {
  const response = await api.get(`/admin/users/${id}`)
  return response.data
}

/**
 * Foydalanuvchini yangilash (is_active toggle va boshqalar).
 * @param {string} id   — foydalanuvchi UUID
 * @param {Object} data — yangilash ma'lumotlari
 */
export async function updateUser(id, data) {
  const response = await api.put(`/admin/users/${id}`, data)
  return response.data
}

/**
 * Foydalanuvchini o'chirish.
 * @param {string} id — foydalanuvchi UUID
 */
export async function deleteUser(id) {
  const response = await api.delete(`/admin/users/${id}`)
  return response.data
}
