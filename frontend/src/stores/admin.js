// Admin store — Pinia
// Kurslar, darslar va foydalanuvchilar boshqaruvi uchun markaziy holat

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as adminApi from '@/api/admin.js'

export const useAdminStore = defineStore('admin', () => {
  // ─── Kurslar state ─────────────────────────────────────────────────────────
  const courses      = ref([])
  const coursesTotal = ref(0)
  const currentCourse = ref(null)

  const loadingCourses = ref(false)
  const savingCourse   = ref(false)
  const errorCourses   = ref('')

  // ─── Darslar state ─────────────────────────────────────────────────────────
  const lessons      = ref([])
  const loadingLessons = ref(false)
  const savingLesson   = ref(false)
  const errorLessons   = ref('')

  // ─── Foydalanuvchilar state ─────────────────────────────────────────────────
  const users      = ref([])
  const usersTotal = ref(0)

  const loadingUsers = ref(false)
  const savingUser   = ref(false)
  const errorUsers   = ref('')

  // ─── Dashboard statistika ────────────────────────────────────────────────────
  const stats = ref({
    totalCourses: 0,
    totalLessons: 0,
    totalUsers:   0,
    activeUsers:  0,
    recentUsers:  [],
  })
  const loadingStats = ref(false)

  // ─── Computed ──────────────────────────────────────────────────────────────
  const publishedCourses = computed(() => courses.value.filter(c => c.is_published))
  const draftCourses     = computed(() => courses.value.filter(c => !c.is_published))

  // ─── Kurs actions ──────────────────────────────────────────────────────────

  async function fetchCourses(params = {}) {
    loadingCourses.value = true
    errorCourses.value = ''
    try {
      const data = await adminApi.getCourses(params)
      courses.value      = data.items
      coursesTotal.value = data.total
    } catch (err) {
      errorCourses.value = err.response?.data?.detail || 'Kurslarni yuklashda xatolik.'
    } finally {
      loadingCourses.value = false
    }
  }

  async function fetchCourse(id) {
    loadingCourses.value = true
    errorCourses.value = ''
    currentCourse.value = null
    try {
      currentCourse.value = await adminApi.getCourses({ limit: 1 })
        .then(() => adminApi.getCourses())
        .catch(() => null)
      // To'g'ridan-to'g'ri kursni kurslar ro'yxatidan topamiz
      const list = await adminApi.getCourses({ limit: 100 })
      currentCourse.value = list.items.find(c => c.id === id) || null
    } catch (err) {
      errorCourses.value = err.response?.data?.detail || 'Kursni yuklashda xatolik.'
    } finally {
      loadingCourses.value = false
    }
  }

  async function createCourse(data) {
    savingCourse.value = true
    try {
      const course = await adminApi.createCourse(data)
      courses.value.unshift(course)
      coursesTotal.value++
      return course
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Kurs yaratishda xatolik.')
    } finally {
      savingCourse.value = false
    }
  }

  async function updateCourse(id, data) {
    savingCourse.value = true
    try {
      const updated = await adminApi.updateCourse(id, data)
      const idx = courses.value.findIndex(c => c.id === id)
      if (idx !== -1) courses.value[idx] = updated
      if (currentCourse.value?.id === id) currentCourse.value = updated
      return updated
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Kursni yangilashda xatolik.')
    } finally {
      savingCourse.value = false
    }
  }

  async function deleteCourse(id) {
    try {
      await adminApi.deleteCourse(id)
      courses.value = courses.value.filter(c => c.id !== id)
      coursesTotal.value = Math.max(0, coursesTotal.value - 1)
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Kursni o\'chirishda xatolik.')
    }
  }

  async function togglePublishCourse(id) {
    try {
      const updated = await adminApi.publishCourse(id)
      const idx = courses.value.findIndex(c => c.id === id)
      if (idx !== -1) courses.value[idx] = { ...courses.value[idx], ...updated }
      return updated
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Nashr holatini o\'zgartirishda xatolik.')
    }
  }

  // ─── Modul state ──────────────────────────────────────────────────────────
  const modules      = ref([])
  const loadingModules = ref(false)
  const savingModule   = ref(false)
  const errorModules   = ref('')

  // ─── Modul actions ──────────────────────────────────────────────────────────

  async function fetchModules(courseId) {
    loadingModules.value = true
    errorModules.value = ''
    try {
      modules.value = await adminApi.getModules(courseId)
    } catch (err) {
      errorModules.value = err.response?.data?.detail || 'Modullarni yuklashda xatolik.'
    } finally {
      loadingModules.value = false
    }
  }

  async function createModule(courseId, data) {
    savingModule.value = true
    try {
      const mod = await adminApi.createModule(courseId, data)
      modules.value.push(mod)
      modules.value.sort((a, b) => a.order - b.order)
      return mod
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Modul yaratishda xatolik.')
    } finally {
      savingModule.value = false
    }
  }

  async function updateModule(courseId, moduleId, data) {
    savingModule.value = true
    try {
      const updated = await adminApi.updateModule(courseId, moduleId, data)
      const idx = modules.value.findIndex(m => m.id === moduleId)
      if (idx !== -1) modules.value[idx] = { ...modules.value[idx], ...updated }
      return updated
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Modulni yangilashda xatolik.')
    } finally {
      savingModule.value = false
    }
  }

  async function deleteModule(courseId, moduleId) {
    try {
      await adminApi.deleteModule(courseId, moduleId)
      modules.value = modules.value.filter(m => m.id !== moduleId)
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Modulni o\'chirishda xatolik.')
    }
  }

  async function togglePublishModule(courseId, moduleId) {
    try {
      const updated = await adminApi.publishModule(courseId, moduleId)
      const idx = modules.value.findIndex(m => m.id === moduleId)
      if (idx !== -1) modules.value[idx] = { ...modules.value[idx], ...updated }
      return updated
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Modul nashr holatida xatolik.')
    }
  }

  // ─── Dars actions ──────────────────────────────────────────────────────────

  async function fetchLessons(courseId) {
    loadingLessons.value = true
    errorLessons.value = ''
    try {
      const data = await adminApi.getLessons(courseId)
      lessons.value = data.items
    } catch (err) {
      errorLessons.value = err.response?.data?.detail || 'Darslarni yuklashda xatolik.'
    } finally {
      loadingLessons.value = false
    }
  }

  async function createLesson(courseId, data) {
    savingLesson.value = true
    try {
      const lesson = await adminApi.createLesson(courseId, data)
      lessons.value.push(lesson)
      lessons.value.sort((a, b) => a.order - b.order)
      return lesson
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Dars yaratishda xatolik.')
    } finally {
      savingLesson.value = false
    }
  }

  async function updateLesson(courseId, lessonId, data) {
    savingLesson.value = true
    try {
      const updated = await adminApi.updateLesson(courseId, lessonId, data)
      const idx = lessons.value.findIndex(l => l.id === lessonId)
      if (idx !== -1) lessons.value[idx] = updated
      return updated
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Darsni yangilashda xatolik.')
    } finally {
      savingLesson.value = false
    }
  }

  async function deleteLesson(courseId, lessonId) {
    try {
      await adminApi.deleteLesson(courseId, lessonId)
      lessons.value = lessons.value.filter(l => l.id !== lessonId)
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Darsni o\'chirishda xatolik.')
    }
  }

  async function togglePublishLesson(courseId, lessonId) {
    try {
      const updated = await adminApi.publishLesson(courseId, lessonId)
      const idx = lessons.value.findIndex(l => l.id === lessonId)
      if (idx !== -1) lessons.value[idx] = { ...lessons.value[idx], ...updated }
      return updated
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Dars nashr holatida xatolik.')
    }
  }

  async function moveLessonUp(courseId, lesson) {
    const idx = lessons.value.findIndex(l => l.id === lesson.id)
    if (idx <= 0) return
    const items = lessons.value.map((l, i) => {
      if (i === idx)     return { id: l.id, order: lessons.value[idx - 1].order }
      if (i === idx - 1) return { id: l.id, order: lesson.order }
      return { id: l.id, order: l.order }
    })
    try {
      await adminApi.reorderLessons(courseId, items)
      await fetchLessons(courseId)
    } catch (err) {
      throw new Error('Tartibni o\'zgartirishda xatolik.')
    }
  }

  async function moveLessonDown(courseId, lesson) {
    const idx = lessons.value.findIndex(l => l.id === lesson.id)
    if (idx >= lessons.value.length - 1) return
    const items = lessons.value.map((l, i) => {
      if (i === idx)     return { id: l.id, order: lessons.value[idx + 1].order }
      if (i === idx + 1) return { id: l.id, order: lesson.order }
      return { id: l.id, order: l.order }
    })
    try {
      await adminApi.reorderLessons(courseId, items)
      await fetchLessons(courseId)
    } catch (err) {
      throw new Error('Tartibni o\'zgartirishda xatolik.')
    }
  }

  // ─── Foydalanuvchi actions ────────────────────────────────────────────────

  async function fetchUsers(params = {}) {
    loadingUsers.value = true
    errorUsers.value = ''
    try {
      const data = await adminApi.getUsers(params)
      users.value      = data.items
      usersTotal.value = data.total
    } catch (err) {
      errorUsers.value = err.response?.data?.detail || 'Foydalanuvchilarni yuklashda xatolik.'
    } finally {
      loadingUsers.value = false
    }
  }

  async function toggleUserActive(id, currentState) {
    savingUser.value = true
    try {
      const updated = await adminApi.updateUser(id, { is_active: !currentState })
      const idx = users.value.findIndex(u => u.id === id)
      if (idx !== -1) users.value[idx] = updated
      return updated
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Foydalanuvchi holatini o\'zgartirishda xatolik.')
    } finally {
      savingUser.value = false
    }
  }

  async function deleteUser(id) {
    try {
      await adminApi.deleteUser(id)
      users.value = users.value.filter(u => u.id !== id)
      usersTotal.value = Math.max(0, usersTotal.value - 1)
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Foydalanuvchini o\'chirishda xatolik.')
    }
  }

  // ─── Dashboard statistika ─────────────────────────────────────────────────

  async function fetchStats() {
    loadingStats.value = true
    try {
      // /admin/stats endpoint yo'q — kurslar va foydalanuvchilar dan hisoblash
      const [coursesData, usersData] = await Promise.all([
        adminApi.getCourses({ limit: 100 }),
        adminApi.getUsers({ limit: 5 }),
      ])

      const totalLessons = coursesData.items.reduce((sum, c) => sum + (c.lessons_count || 0), 0)

      stats.value = {
        totalCourses: coursesData.total,
        totalLessons,
        totalUsers:   usersData.total,
        activeUsers:  usersData.items.filter(u => u.is_active).length,
        recentUsers:  usersData.items.slice(0, 5),
        coursesList:  coursesData.items.slice(0, 6),
      }
    } catch (err) {
      // Statistikani yuklab bo'lmasa — jimgina o'tkazib yuboramiz
      console.warn('Statistikani yuklashda xatolik:', err.message)
    } finally {
      loadingStats.value = false
    }
  }

  return {
    // Kurslar
    courses, coursesTotal, currentCourse,
    loadingCourses, savingCourse, errorCourses,
    publishedCourses, draftCourses,
    fetchCourses, fetchCourse, createCourse, updateCourse,
    deleteCourse, togglePublishCourse,

    // Modullar
    modules, loadingModules, savingModule, errorModules,
    fetchModules, createModule, updateModule, deleteModule, togglePublishModule,

    // Darslar
    lessons, loadingLessons, savingLesson, errorLessons,
    fetchLessons, createLesson, updateLesson, deleteLesson,
    togglePublishLesson, moveLessonUp, moveLessonDown,

    // Foydalanuvchilar
    users, usersTotal, loadingUsers, savingUser, errorUsers,
    fetchUsers, toggleUserActive, deleteUser,

    // Dashboard
    stats, loadingStats, fetchStats,
  }
})
