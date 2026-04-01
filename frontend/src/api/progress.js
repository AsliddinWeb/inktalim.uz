// Student — Progress API chaqiruvlari
// Darsni tugatilgan/tugatilmagan belgilash va progress ko'rish

import api from '@/api/axios.js'

/**
 * Darsni tugatilgan deb belgilash.
 * Javobda: { message, lesson_id, is_completed, course_progress_percent }
 * @param {string} lessonId — dars UUID
 */
export async function completeLesson(lessonId) {
  const response = await api.post(`/student/progress/lessons/${lessonId}/complete`)
  return response.data
}

/**
 * Darsni tugatilmagan qilib qaytarish (toggle uchun).
 * @param {string} lessonId — dars UUID
 */
export async function uncompleteLesson(lessonId) {
  const response = await api.delete(`/student/progress/lessons/${lessonId}/complete`)
  return response.data
}

/**
 * Foydalanuvchi barcha boshlagan kurslardagi progressni olish.
 * Faqat birorta darsini ochgan kurslar qaytariladi.
 */
export async function getAllProgress() {
  const response = await api.get('/student/progress')
  return response.data
}

/**
 * Bitta kurs bo'yicha batafsil progress.
 * Har bir dars uchun is_completed va completed_at qaytariladi.
 * @param {string} courseId — kurs UUID
 */
export async function getCourseProgress(courseId) {
  const response = await api.get(`/student/progress/${courseId}`)
  return response.data
}
