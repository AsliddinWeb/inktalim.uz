<template>
  <div class="space-y-4">

    <!-- No quiz -->
    <template v-if="!quiz">
      <div v-if="!showCreateQuiz" class="text-center py-8">
        <div class="w-14 h-14 rounded-2xl bg-primary-50 dark:bg-primary-900/20 flex items-center justify-center mx-auto mb-3">
          <svg class="w-7 h-7 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
        </div>
        <p class="text-gray-500 dark:text-gray-400 text-sm mb-3">Bu darsda hali quiz yo'q</p>
        <button
          type="button"
          class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
          @click="showCreateQuiz = true"
        >
          Quiz yaratish
        </button>
      </div>

      <!-- Create quiz form -->
      <div v-else class="rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-4">
        <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-4">Yangi quiz</h3>
        <QuizForm :lesson-id="lessonId" :loading="saving" @submit="createQuiz" @cancel="showCreateQuiz = false" />
      </div>
    </template>

    <!-- Quiz exists -->
    <template v-else>

      <!-- Quiz header -->
      <div class="flex items-start justify-between gap-3">
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 flex-wrap">
            <h3 class="text-sm font-semibold text-gray-900 dark:text-white truncate">{{ quiz.title }}</h3>
            <span
              class="text-xs px-2 py-0.5 rounded-full font-medium"
              :class="quiz.is_active
                ? 'bg-success-100 dark:bg-success-900/20 text-success-700 dark:text-success-400'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400'"
            >
              {{ quiz.is_active ? 'Faol' : 'Nofaol' }}
            </span>
            <span class="text-xs text-gray-400">O'tish: {{ quiz.pass_percent }}%</span>
          </div>
          <p v-if="quiz.description" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-1">{{ quiz.description }}</p>
        </div>
        <div class="flex items-center gap-0.5 flex-shrink-0">
          <button
            type="button"
            class="p-1.5 text-gray-400 hover:text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors"
            title="Tahrirlash"
            @click="showEditQuiz = !showEditQuiz"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
          </button>
          <button
            type="button"
            class="p-1.5 text-gray-400 hover:text-danger-500 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-lg transition-colors"
            title="O'chirish"
            @click="confirmDeleteQuiz"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Edit quiz -->
      <div v-if="showEditQuiz" class="rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-4">
        <QuizForm :quiz="quiz" :loading="saving" @submit="updateQuiz" @cancel="showEditQuiz = false" />
      </div>

      <!-- Questions section -->
      <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            Savollar ({{ quiz.questions?.length ?? 0 }})
          </span>
          <button
            v-if="!showAddQuestion"
            type="button"
            class="text-xs text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-colors"
            @click="showAddQuestion = true"
          >
            + Savol qo'shish
          </button>
        </div>

        <!-- Add question form -->
        <div v-if="showAddQuestion" class="rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-4 mb-3">
          <h4 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-3">Yangi savol</h4>
          <QuestionForm :loading="saving" @submit="(d) => createQuestion(d)" @cancel="showAddQuestion = false" />
        </div>

        <!-- Questions list -->
        <div v-if="quiz.questions?.length" class="space-y-2">
          <div
            v-for="(question, qIndex) in quiz.questions"
            :key="question.id"
            class="rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden"
          >
            <!-- Question header -->
            <div
              class="flex items-start gap-3 p-3 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
              @click="toggleQuestion(question.id)"
            >
              <span class="text-xs font-bold text-primary-500 flex-shrink-0 mt-0.5">{{ qIndex + 1 }}.</span>
              <p class="flex-1 text-sm text-gray-800 dark:text-gray-200 line-clamp-2">{{ question.text }}</p>
              <div class="flex items-center gap-1 flex-shrink-0">
                <span class="text-xs text-gray-400">{{ question.choices?.length ?? 0 }} variant</span>
                <button
                  type="button"
                  class="p-1 text-gray-400 hover:text-primary-500 rounded transition-colors"
                  @click.stop="startEditQuestion(question)"
                >
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                </button>
                <button
                  type="button"
                  class="p-1 text-gray-400 hover:text-danger-500 rounded transition-colors"
                  @click.stop="deleteQuestion(question)"
                >
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
                <svg
                  class="w-4 h-4 text-gray-400 transition-transform"
                  :class="openQuestions.has(question.id) ? 'rotate-180' : ''"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </div>

            <!-- Edit question -->
            <div
              v-if="editingQuestionId === question.id"
              class="border-t border-gray-200 dark:border-gray-700 p-3 bg-gray-50 dark:bg-gray-800/30"
            >
              <QuestionForm
                :question="question"
                :loading="saving"
                @submit="(d) => updateQuestion(question, d)"
                @cancel="editingQuestionId = null"
              />
            </div>

            <!-- Choices list -->
            <div
              v-else-if="openQuestions.has(question.id)"
              class="border-t border-gray-200 dark:border-gray-700 p-3 space-y-1.5 bg-gray-50/50 dark:bg-gray-800/20"
            >
              <div v-for="choice in question.choices" :key="choice.id" class="flex items-center gap-2 text-sm">
                <div
                  class="w-4 h-4 rounded-full flex-shrink-0 flex items-center justify-center"
                  :class="choice.is_correct ? 'bg-success-500' : 'bg-gray-200 dark:bg-gray-600'"
                >
                  <svg v-if="choice.is_correct" class="w-2.5 h-2.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <span
                  class="text-gray-700 dark:text-gray-300"
                  :class="choice.is_correct ? 'font-medium text-success-700 dark:text-success-400' : ''"
                >
                  {{ choice.text }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-4 text-sm text-gray-400">
          Hali savollar yo'q
        </div>
      </div>
    </template>

    <!-- Error -->
    <p v-if="error" class="text-xs text-danger-500">{{ error }}</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { adminQuizApi } from '@/api/quiz.js'
import QuizForm from './QuizForm.vue'
import QuestionForm from './QuestionForm.vue'

const props = defineProps({
  lessonId: { type: String, required: true },
})

const quiz = ref(null)
const saving = ref(false)
const error = ref(null)

const showCreateQuiz = ref(false)
const showEditQuiz = ref(false)
const showAddQuestion = ref(false)
const openQuestions = ref(new Set())
const editingQuestionId = ref(null)

async function loadQuiz() {
  error.value = null
  try {
    const { data } = await adminQuizApi.getByLesson(props.lessonId)
    quiz.value = data
  } catch (e) {
    if (e.response?.status !== 404) {
      error.value = e.response?.data?.detail ?? 'Xatolik'
    }
    quiz.value = null
  }
}

async function createQuiz(payload) {
  saving.value = true
  error.value = null
  try {
    await adminQuizApi.create(payload)
    showCreateQuiz.value = false
    await loadQuiz()
  } catch (e) {
    error.value = e.response?.data?.detail ?? 'Xatolik'
  } finally {
    saving.value = false
  }
}

async function updateQuiz(payload) {
  saving.value = true
  error.value = null
  try {
    await adminQuizApi.update(quiz.value.id, payload)
    showEditQuiz.value = false
    await loadQuiz()
  } catch (e) {
    error.value = e.response?.data?.detail ?? 'Xatolik'
  } finally {
    saving.value = false
  }
}

async function confirmDeleteQuiz() {
  if (!confirm('Quizni o\'chirmoqchimisiz? Barcha savollar ham o\'chadi.')) return
  saving.value = true
  try {
    await adminQuizApi.remove(quiz.value.id)
    quiz.value = null
  } catch (e) {
    error.value = e.response?.data?.detail ?? 'Xatolik'
  } finally {
    saving.value = false
  }
}

function toggleQuestion(id) {
  if (editingQuestionId.value === id) return
  if (openQuestions.value.has(id)) {
    openQuestions.value.delete(id)
  } else {
    openQuestions.value.add(id)
  }
  openQuestions.value = new Set(openQuestions.value)
}

function startEditQuestion(question) {
  editingQuestionId.value = question.id
  openQuestions.value.delete(question.id)
  openQuestions.value = new Set(openQuestions.value)
}

async function createQuestion(payload) {
  saving.value = true
  error.value = null
  try {
    await adminQuizApi.createQuestion(quiz.value.id, payload)
    showAddQuestion.value = false
    await loadQuiz()
  } catch (e) {
    error.value = e.response?.data?.detail ?? 'Xatolik'
  } finally {
    saving.value = false
  }
}

async function updateQuestion(question, payload) {
  saving.value = true
  error.value = null
  try {
    // Savolni yangilash
    await adminQuizApi.updateQuestion(quiz.value.id, question.id, {
      text: payload.text,
      order: payload.order,
    })
    // Variantlarni qayta yaratish (sodda yondashuv)
    // Avval mavjud variantlarni o'chirish, keyin yangisini qo'shish
    for (const choice of question.choices ?? []) {
      await adminQuizApi.deleteChoice(quiz.value.id, question.id, choice.id)
    }
    for (const choice of payload.choices) {
      await adminQuizApi.createChoice(quiz.value.id, question.id, choice)
    }
    editingQuestionId.value = null
    await loadQuiz()
  } catch (e) {
    error.value = e.response?.data?.detail ?? 'Xatolik'
  } finally {
    saving.value = false
  }
}

async function deleteQuestion(question) {
  if (!confirm('Savolni o\'chirmoqchimisiz?')) return
  saving.value = true
  try {
    await adminQuizApi.deleteQuestion(quiz.value.id, question.id)
    openQuestions.value.delete(question.id)
    openQuestions.value = new Set(openQuestions.value)
    await loadQuiz()
  } catch (e) {
    error.value = e.response?.data?.detail ?? 'Xatolik'
  } finally {
    saving.value = false
  }
}

onMounted(loadQuiz)
</script>
