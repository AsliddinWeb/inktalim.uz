// Quiz store — student tomonidan quiz o'tish holati
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { studentQuizApi } from '@/api/quiz.js'

export const useQuizStore = defineStore('quiz', () => {
  // Joriy quiz ma'lumoti
  const currentQuiz = ref(null)
  // Tanlangan javoblar: { [question_id]: choice_id }
  const selectedAnswers = ref({})
  // Topshirish natijasi
  const attemptResult = ref(null)
  // Urinishlar tarixi
  const attemptHistory = ref(null)

  const loading = ref(false)
  const error = ref(null)

  // Hamma savollarga javob beriladimi?
  const isAllAnswered = computed(() => {
    if (!currentQuiz.value) return false
    const questionIds = currentQuiz.value.questions.map((q) => q.id)
    return questionIds.every((id) => id in selectedAnswers.value)
  })

  // Nechta savol bor
  const totalQuestions = computed(() => currentQuiz.value?.questions?.length ?? 0)

  // Nechta javob berildi
  const answeredCount = computed(() => Object.keys(selectedAnswers.value).length)

  async function loadQuiz(lessonId) {
    loading.value = true
    error.value = null
    try {
      const { data } = await studentQuizApi.getByLesson(lessonId)
      currentQuiz.value = data
      selectedAnswers.value = {}
      attemptResult.value = null
    } catch (err) {
      error.value = err.response?.data?.detail ?? 'Quiz yuklanmadi'
      currentQuiz.value = null
    } finally {
      loading.value = false
    }
  }

  async function loadHistory(lessonId) {
    try {
      const { data } = await studentQuizApi.getHistory(lessonId)
      attemptHistory.value = data
    } catch {
      attemptHistory.value = null
    }
  }

  function selectAnswer(questionId, choiceId) {
    selectedAnswers.value = { ...selectedAnswers.value, [questionId]: choiceId }
  }

  async function submitQuiz(lessonId) {
    if (!isAllAnswered.value) return

    loading.value = true
    error.value = null
    try {
      const answers = Object.entries(selectedAnswers.value).map(([question_id, choice_id]) => ({
        question_id,
        choice_id,
      }))
      const { data } = await studentQuizApi.submit(lessonId, answers)
      attemptResult.value = data
      // Tarixni yangilash
      await loadHistory(lessonId)
    } catch (err) {
      error.value = err.response?.data?.detail ?? 'Xatolik yuz berdi'
    } finally {
      loading.value = false
    }
  }

  function resetQuiz() {
    currentQuiz.value = null
    selectedAnswers.value = {}
    attemptResult.value = null
    attemptHistory.value = null
    error.value = null
  }

  return {
    currentQuiz,
    selectedAnswers,
    attemptResult,
    attemptHistory,
    loading,
    error,
    isAllAnswered,
    totalQuestions,
    answeredCount,
    loadQuiz,
    loadHistory,
    selectAnswer,
    submitQuiz,
    resetQuiz,
  }
})
