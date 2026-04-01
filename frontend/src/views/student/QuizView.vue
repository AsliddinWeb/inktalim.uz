<template>
  <div class="min-h-screen bg-app py-8 px-4">

    <!-- Loading -->
    <div
      v-if="quizStore.loading && !quizStore.currentQuiz && !quizStore.attemptResult"
      class="flex flex-col items-center justify-center py-32 gap-4"
    >
      <div class="w-12 h-12 rounded-full border-4 border-primary-100 dark:border-primary-900/40 border-t-primary-500 animate-spin" />
      <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Test yuklanmoqda...</p>
    </div>

    <!-- Error state -->
    <div
      v-else-if="quizStore.error && !quizStore.currentQuiz"
      class="max-w-2xl mx-auto py-8"
    >
      <div class="rounded-2xl border border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10 p-8 text-center">
        <div class="w-14 h-14 rounded-full bg-danger-100 dark:bg-danger-900/30 flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-danger-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 class="text-base font-semibold text-danger-700 dark:text-danger-400 mb-2">Xatolik yuz berdi</h3>
        <p class="text-sm text-danger-600 dark:text-danger-400/80 mb-6">{{ quizStore.error }}</p>
        <button
          type="button"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          @click="$router.back()"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Orqaga
        </button>
      </div>
    </div>

    <!-- Result page -->
    <template v-else-if="quizStore.attemptResult">
      <div class="max-w-2xl mx-auto py-8">

        <!-- Confetti -->
        <template v-if="quizStore.attemptResult.is_passed">
          <div
            v-for="i in 20"
            :key="i"
            class="confetti-piece"
            :style="`left:${Math.random() * 100}%; animation-delay:${Math.random() * 1.5}s; background:${confettiColors[i % confettiColors.length]}`"
          />
        </template>

        <!-- Result card -->
        <div class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-8 text-center shadow-lg">

          <!-- SVG circle score -->
          <div class="flex justify-center mb-2">
            <div class="relative" style="width:180px; height:180px;">
              <svg width="180" height="180" viewBox="0 0 180 180" class="-rotate-90">
                <circle cx="90" cy="90" r="74" fill="none" stroke="currentColor" class="text-gray-100 dark:text-gray-800" stroke-width="12" />
                <circle
                  cx="90" cy="90" r="74" fill="none"
                  :stroke="quizStore.attemptResult.is_passed ? '#10B981' : '#EF4444'"
                  stroke-width="12" stroke-linecap="round"
                  :stroke-dasharray="`${2 * Math.PI * 74}`"
                  :stroke-dashoffset="`${2 * Math.PI * 74 * (1 - quizStore.attemptResult.score_percent / 100)}`"
                  style="transition: stroke-dashoffset 1s ease"
                />
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span
                  class="text-4xl font-black leading-none"
                  :class="quizStore.attemptResult.is_passed ? 'text-success-500' : 'text-danger-500'"
                >
                  {{ quizStore.attemptResult.score_percent }}%
                </span>
                <span class="text-xs text-gray-400 mt-1">ball</span>
              </div>
            </div>
          </div>

          <!-- Correct count -->
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-xs font-medium text-gray-600 dark:text-gray-400 mb-5">
            <svg class="w-3.5 h-3.5 text-success-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            {{ quizStore.attemptResult.correct_count }}/{{ quizStore.attemptResult.total_count }} to'g'ri javob
          </div>

          <!-- Title -->
          <h2
            class="text-2xl font-bold mb-2"
            :class="quizStore.attemptResult.is_passed ? 'text-success-600 dark:text-success-400' : 'text-danger-600 dark:text-danger-400'"
          >
            {{ quizStore.attemptResult.is_passed ? '🎉 Tabriklaymiz! O\'tdingiz!' : '😔 O\'tmadiniz' }}
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            O'tish uchun {{ quizStore.attemptResult.pass_percent }}% kerak edi
          </p>

          <!-- Answer breakdown -->
          <div class="mt-8 text-left">
            <h4 class="text-base font-semibold text-gray-900 dark:text-white mb-4">Javoblar tahlili</h4>
            <div class="space-y-3">
              <div
                v-for="(answer, idx) in quizStore.attemptResult.answers"
                :key="answer.question_id"
                class="rounded-xl border p-4 flex items-start gap-3"
                :class="answer.is_correct
                  ? 'border-success-200 dark:border-success-800/30 bg-success-50 dark:bg-success-900/10'
                  : 'border-danger-200 dark:border-danger-800/30 bg-danger-50 dark:bg-danger-900/10'"
              >
                <div class="flex-shrink-0 mt-0.5">
                  <svg v-if="answer.is_correct" class="w-5 h-5 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg v-else class="w-5 h-5 text-danger-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-medium text-gray-800 dark:text-gray-200">
                    {{ idx + 1 }}. {{ answer.question_text }}
                  </p>
                  <div class="mt-1 space-y-0.5">
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      <span class="font-medium">Sizning javobingiz: </span>
                      <span :class="answer.is_correct ? 'text-success-600 dark:text-success-400' : 'text-danger-600 dark:text-danger-400'">
                        {{ answer.selected_choice_text }}
                      </span>
                    </p>
                    <p v-if="!answer.is_correct" class="text-xs text-gray-500 dark:text-gray-400">
                      <span class="font-medium">To'g'ri javob: </span>
                      <span class="text-success-600 dark:text-success-400">{{ answer.correct_choice_text }}</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Attempt history -->
          <AttemptHistory :history="quizStore.attemptHistory" class="mt-8 text-left" />

          <!-- Actions -->
          <div class="mt-8 flex flex-col sm:flex-row gap-3 justify-center">
            <button
              type="button"
              class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold border border-gray-200 dark:border-gray-700 bg-white dark:bg-surface text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-150 shadow-sm"
              @click="retakeQuiz"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
              </svg>
              Qayta urinish
            </button>
            <button
              type="button"
              class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold bg-primary-500 hover:bg-primary-600 text-white shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
              @click="goBack"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 12H5m7-7l-7 7 7 7" />
              </svg>
              Darsga qaytish
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Quiz questions -->
    <template v-else-if="quizStore.currentQuiz">
      <div class="max-w-2xl mx-auto py-8">

        <!-- Top bar -->
        <div class="flex items-center justify-between mb-6">
          <button
            type="button"
            class="inline-flex items-center gap-1.5 text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
            @click="goBack"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Darsga qaytish
          </button>
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400">
            {{ quizStore.answeredCount }}/{{ quizStore.totalQuestions }} savol
          </span>
        </div>

        <!-- Title -->
        <h1 class="text-xl font-bold text-gray-900 dark:text-white mb-1">
          {{ quizStore.currentQuiz.title }}
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-5">
          O'tish uchun {{ quizStore.currentQuiz.pass_percent }}% kerak
        </p>

        <!-- Progress bar -->
        <div class="h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden mb-8">
          <div
            class="h-full rounded-full bg-gradient-to-r from-primary-600 to-primary-400 transition-all duration-500"
            :style="`width:${quizStore.totalQuestions ? (quizStore.answeredCount / quizStore.totalQuestions) * 100 : 0}%`"
          />
        </div>

        <!-- Questions -->
        <div class="space-y-6">
          <div
            v-for="(question, qIndex) in quizStore.currentQuiz.questions"
            :key="question.id"
            class="rounded-2xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-surface p-6 shadow-sm"
          >
            <p class="text-base font-semibold text-gray-900 dark:text-white mb-5">
              <span class="text-primary-500 mr-2">{{ qIndex + 1 }}.</span>
              {{ question.text }}
            </p>

            <div class="space-y-3">
              <label v-for="choice in question.choices" :key="choice.id" class="block cursor-pointer">
                <input
                  type="radio"
                  :name="`question-${question.id}`"
                  :value="choice.id"
                  class="sr-only"
                  @change="quizStore.selectAnswer(question.id, choice.id)"
                />
                <div
                  class="flex items-center gap-3 rounded-xl border-2 px-4 py-3.5 transition-all duration-150"
                  :class="quizStore.selectedAnswers[question.id] === choice.id
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/10 shadow-sm'
                    : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 hover:border-primary-300 dark:hover:border-primary-700 hover:bg-primary-50/50 dark:hover:bg-primary-900/5'"
                >
                  <div
                    class="w-5 h-5 rounded-full border-2 flex-shrink-0 flex items-center justify-center transition-all"
                    :class="quizStore.selectedAnswers[question.id] === choice.id
                      ? 'border-primary-500 bg-primary-500'
                      : 'border-gray-300 dark:border-gray-600'"
                  >
                    <div v-if="quizStore.selectedAnswers[question.id] === choice.id" class="w-2 h-2 rounded-full bg-white" />
                  </div>
                  <span
                    class="text-sm font-medium leading-relaxed transition-colors"
                    :class="quizStore.selectedAnswers[question.id] === choice.id
                      ? 'text-primary-700 dark:text-primary-300'
                      : 'text-gray-700 dark:text-gray-300'"
                  >
                    {{ choice.text }}
                  </span>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Submit area -->
        <div class="mt-8 pt-6 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between gap-4">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            <span class="font-semibold text-gray-700 dark:text-gray-300">{{ quizStore.answeredCount }}</span>
            ta javob berildi
          </p>
          <button
            type="button"
            :disabled="!quizStore.isAllAnswered || quizStore.loading"
            class="inline-flex items-center gap-2 px-7 py-3 rounded-xl text-sm font-semibold text-white bg-primary-500 hover:bg-primary-600 shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none"
            @click="submitQuiz"
          >
            <svg v-if="quizStore.loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            {{ quizStore.loading ? 'Tekshirilmoqda...' : 'Testni yakunlash' }}
          </button>
        </div>

        <!-- Attempt history (bottom) -->
        <div v-if="quizStore.attemptHistory?.attempts?.length" class="mt-8">
          <AttemptHistory :history="quizStore.attemptHistory" />
        </div>

      </div>
    </template>

  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { useQuizStore } from '@/stores/quiz.js'
import AttemptHistory from '@/components/student/AttemptHistory.vue'

const route = useRoute()
const router = useRouter()
const quizStore = useQuizStore()

const lessonId = route.params.lessonId

const confettiColors = ['#14B8A6', '#06B6D4', '#22C55E', '#F59E0B', '#8B5CF6', '#EC4899']

onMounted(async () => {
  await quizStore.loadQuiz(lessonId)
  await quizStore.loadHistory(lessonId)
})

onBeforeUnmount(() => {
  quizStore.resetQuiz()
})

// Savollar tugamagan bo'lsa, sahifadan chiqishni ogohlantirib qo'yish
onBeforeRouteLeave((_to, _from, next) => {
  if (
    quizStore.currentQuiz
    && !quizStore.attemptResult
    && quizStore.answeredCount > 0
  ) {
    const confirmed = window.confirm('Quiz tugallanmadi. Sahifadan chiqmoqchimisiz?')
    if (!confirmed) return next(false)
  }
  next()
})

async function submitQuiz() {
  await quizStore.submitQuiz(lessonId)
  // Natija kelib qolsa — yuqoriga scroll
  if (quizStore.attemptResult) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

function goBack() {
  router.push({
    name: 'lesson',
    params: { courseId: route.params.courseId, lessonId },
  })
}

function retakeQuiz() {
  quizStore.selectedAnswers = {}
  quizStore.attemptResult = null
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
@keyframes confetti-fall {
  0% { transform: translateY(-20px) rotate(0deg); opacity: 1; }
  100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}
.confetti-piece {
  position: fixed;
  width: 10px;
  height: 10px;
  top: 0;
  border-radius: 2px;
  animation: confetti-fall 3s ease-in forwards;
  pointer-events: none;
  z-index: 9999;
}
</style>
