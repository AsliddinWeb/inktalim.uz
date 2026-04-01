// Student — Kurs API chaqiruvlari
// Faqat nashr qilingan kurslar va darslar

import api from '@/api/axios.js'

/**
 * Barcha nashr qilingan kurslar ro'yxatini olish.
 * Javobda har bir kursda progress ma'lumotlari ham bor.
 */
export async function getCourses() {
  const response = await api.get('/student/courses')
  return response.data
}

/**
 * Bitta kurs detail ma'lumotlari + darslar ro'yxati.
 * @param {string} courseId — kurs UUID
 */
export async function getCourse(courseId) {
  const response = await api.get(`/student/courses/${courseId}`)
  return response.data
}

/**
 * Dars to'liq ma'lumotlari (content, video_url, prev/next).
 * Bu endpoint darsni ochganda progress avtomatik boshlanadi (side effect).
 * @param {string} courseId  — kurs UUID
 * @param {string} lessonId  — dars UUID
 */
export async function getLesson(courseId, lessonId) {
  const response = await api.get(`/student/courses/${courseId}/lessons/${lessonId}`)
  return response.data
}
