// Progress store — Pinia
// Foydalanuvchi kurslardagi progress holati

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  completeLesson,
  uncompleteLesson,
  getAllProgress,
  getCourseProgress,
} from '@/api/progress.js'
import { useCoursesStore } from '@/stores/courses.js'

export const useProgressStore = defineStore('progress', () => {
  // ─── State ─────────────────────────────────────────────────────────────────

  // Barcha kurslardagi progress ro'yxati
  const allProgress = ref([])

  // Bitta kurs batafsil progressi
  const courseProgress = ref(null)

  // Dars tugallash jarayoni (loading)
  const completingLesson = ref(false)

  // Yuklash holati
  const loadingAll    = ref(false)
  const loadingCourse = ref(false)

  // Xato xabarlari
  const errorAll    = ref('')
  const errorCourse = ref('')

  // ─── Computed ───────────────────────────────────────────────────────────────

  // Boshlangan kurslar soni
  const startedCoursesCount = computed(() => allProgress.value.length)

  // O'rtacha progress foizi
  const averageProgress = computed(() => {
    if (!allProgress.value.length) return 0
    const sum = allProgress.value.reduce((acc, p) => acc + p.progress_percent, 0)
    return Math.round(sum / allProgress.value.length)
  })

  // Tugallangan kurslar soni
  const completedCoursesCount = computed(() =>
    allProgress.value.filter(p => p.progress_percent === 100).length
  )

  // ─── Actions ────────────────────────────────────────────────────────────────

  /**
   * Barcha kurslardagi progressni yuklash.
   */
  async function fetchAllProgress() {
    loadingAll.value = true
    errorAll.value = ''
    try {
      allProgress.value = await getAllProgress()
    } catch (err) {
      errorAll.value =
        err.response?.data?.detail || 'Progressni yuklashda xatolik yuz berdi.'
    } finally {
      loadingAll.value = false
    }
  }

  /**
   * Bitta kurs batafsil progressini yuklash.
   * @param {string} courseId
   */
  async function fetchCourseProgress(courseId) {
    loadingCourse.value = true
    errorCourse.value = ''
    courseProgress.value = null
    try {
      courseProgress.value = await getCourseProgress(courseId)
    } catch (err) {
      errorCourse.value =
        err.response?.data?.detail || 'Kurs progressini yuklashda xatolik yuz berdi.'
    } finally {
      loadingCourse.value = false
    }
  }

  /**
   * Darsni tugatilgan deb belgilash.
   * Courses store dagi local state ham yangilanadi.
   * @param {string} lessonId
   * @param {string} courseId — kurs progress foizini yangilash uchun
   * @returns {number} yangilangan kurs progress foizi
   */
  async function markComplete(lessonId, courseId) {
    completingLesson.value = true
    try {
      const result = await completeLesson(lessonId)

      // Courses store ni yangilash
      const coursesStore = useCoursesStore()
      coursesStore.updateLessonCompletion(true)
      coursesStore.updateCourseProgress(courseId, result.course_progress_percent)

      return result.course_progress_percent
    } catch (err) {
      throw new Error(
        err.response?.data?.detail || 'Darsni tugatishda xatolik yuz berdi.'
      )
    } finally {
      completingLesson.value = false
    }
  }

  /**
   * Darsni tugatilmagan qilib qaytarish.
   * @param {string} lessonId
   * @param {string} courseId
   */
  async function markUncomplete(lessonId, courseId) {
    completingLesson.value = true
    try {
      const result = await uncompleteLesson(lessonId)

      const coursesStore = useCoursesStore()
      coursesStore.updateLessonCompletion(false)
      coursesStore.updateCourseProgress(courseId, result.course_progress_percent)

      return result.course_progress_percent
    } catch (err) {
      throw new Error(
        err.response?.data?.detail || 'Darsni qaytarishda xatolik yuz berdi.'
      )
    } finally {
      completingLesson.value = false
    }
  }

  return {
    allProgress,
    courseProgress,
    completingLesson,
    loadingAll,
    loadingCourse,
    errorAll,
    errorCourse,
    startedCoursesCount,
    averageProgress,
    completedCoursesCount,
    fetchAllProgress,
    fetchCourseProgress,
    markComplete,
    markUncomplete,
  }
})
