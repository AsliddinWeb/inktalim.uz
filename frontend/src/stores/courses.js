// Kurslar store — Pinia
// Kurslar ro'yxati, joriy kurs, joriy dars state lari

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getCourses, getCourse, getLesson } from '@/api/courses.js'

export const useCoursesStore = defineStore('courses', () => {
  // ─── State ─────────────────────────────────────────────────────────────────

  // Barcha kurslar ro'yxati
  const courses = ref([])

  // Joriy ochiq kurs (detail sahifa)
  const currentCourse = ref(null)

  // Joriy ochiq dars
  const currentLesson = ref(null)

  // Yuklash holatlari
  const loadingCourses = ref(false)
  const loadingCourse  = ref(false)
  const loadingLesson  = ref(false)

  // Xato xabarlari
  const errorCourses = ref('')
  const errorCourse  = ref('')
  const errorLesson  = ref('')

  // ─── Computed ───────────────────────────────────────────────────────────────

  // Boshlangan (enrolled) kurslar — birorta darsni ochgan
  const enrolledCourses = computed(() =>
    courses.value.filter(c => c.is_enrolled)
  )

  // Tugallanmagan (davom etayotgan) kurslar
  const inProgressCourses = computed(() =>
    courses.value.filter(c => c.is_enrolled && c.progress_percent < 100)
  )

  // Tugallangan kurslar
  const completedCourses = computed(() =>
    courses.value.filter(c => c.is_enrolled && c.progress_percent === 100)
  )

  // ─── Actions ────────────────────────────────────────────────────────────────

  /**
   * Barcha kurslarni API dan yuklash.
   */
  async function fetchCourses() {
    loadingCourses.value = true
    errorCourses.value = ''
    try {
      courses.value = await getCourses()
    } catch (err) {
      errorCourses.value =
        err.response?.data?.detail || 'Kurslarni yuklashda xatolik yuz berdi.'
    } finally {
      loadingCourses.value = false
    }
  }

  /**
   * Bitta kurs detail ma'lumotlarini yuklash.
   * @param {string} courseId
   */
  async function fetchCourse(courseId) {
    loadingCourse.value = true
    errorCourse.value = ''
    currentCourse.value = null
    try {
      currentCourse.value = await getCourse(courseId)
    } catch (err) {
      errorCourse.value =
        err.response?.data?.detail || 'Kursni yuklashda xatolik yuz berdi.'
    } finally {
      loadingCourse.value = false
    }
  }

  /**
   * Bitta dars ma'lumotlarini yuklash.
   * @param {string} courseId
   * @param {string} lessonId
   */
  async function fetchLesson(courseId, lessonId) {
    loadingLesson.value = true
    errorLesson.value = ''
    currentLesson.value = null
    try {
      currentLesson.value = await getLesson(courseId, lessonId)
    } catch (err) {
      errorLesson.value =
        err.response?.data?.detail || 'Darsni yuklashda xatolik yuz berdi.'
    } finally {
      loadingLesson.value = false
    }
  }

  /**
   * Joriy darsdagi is_completed ni lokal yangilash (API dan qayta yuklamasdan).
   * completeLesson / uncompleteLesson dan so'ng chaqiriladi.
   */
  function updateLessonCompletion(isCompleted) {
    if (currentLesson.value) {
      currentLesson.value.is_completed = isCompleted
    }
  }

  /**
   * Kurslar ro'yxatida bitta kurs progress foizini yangilash.
   */
  function updateCourseProgress(courseId, progressPercent) {
    const course = courses.value.find(c => c.id === courseId)
    if (course) {
      course.progress_percent = progressPercent
      if (progressPercent > 0) course.is_enrolled = true
    }
    if (currentCourse.value?.id === courseId) {
      currentCourse.value.progress_percent = progressPercent
    }
  }

  return {
    courses,
    currentCourse,
    currentLesson,
    loadingCourses,
    loadingCourse,
    loadingLesson,
    errorCourses,
    errorCourse,
    errorLesson,
    enrolledCourses,
    inProgressCourses,
    completedCourses,
    fetchCourses,
    fetchCourse,
    fetchLesson,
    updateLessonCompletion,
    updateCourseProgress,
  }
})
