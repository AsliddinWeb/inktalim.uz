// Quiz API — admin va student endpointlari

import api from './axios.js'

// ─── Admin ───────────────────────────────────────────────────────────────────

export const adminQuizApi = {
  // Quiz CRUD
  create: (data) => api.post('/admin/quizzes', data),
  getById: (quizId) => api.get(`/admin/quizzes/${quizId}`),
  getByLesson: (lessonId) => api.get(`/admin/quizzes/by-lesson/${lessonId}`),
  update: (quizId, data) => api.patch(`/admin/quizzes/${quizId}`, data),
  remove: (quizId) => api.delete(`/admin/quizzes/${quizId}`),

  // Questions
  createQuestion: (quizId, data) => api.post(`/admin/quizzes/${quizId}/questions`, data),
  updateQuestion: (quizId, questionId, data) =>
    api.patch(`/admin/quizzes/${quizId}/questions/${questionId}`, data),
  deleteQuestion: (quizId, questionId) =>
    api.delete(`/admin/quizzes/${quizId}/questions/${questionId}`),
  reorderQuestions: (quizId, items) =>
    api.post(`/admin/quizzes/${quizId}/questions/reorder`, { items }),

  // Choices
  createChoice: (quizId, questionId, data) =>
    api.post(`/admin/quizzes/${quizId}/questions/${questionId}/choices`, data),
  updateChoice: (quizId, questionId, choiceId, data) =>
    api.patch(`/admin/quizzes/${quizId}/questions/${questionId}/choices/${choiceId}`, data),
  deleteChoice: (quizId, questionId, choiceId) =>
    api.delete(`/admin/quizzes/${quizId}/questions/${questionId}/choices/${choiceId}`),
}

// ─── Student ─────────────────────────────────────────────────────────────────

export const studentQuizApi = {
  getByLesson: (lessonId) => api.get(`/student/quizzes/by-lesson/${lessonId}`),
  submit: (lessonId, answers) =>
    api.post(`/student/quizzes/by-lesson/${lessonId}/submit`, { answers }),
  getHistory: (lessonId) => api.get(`/student/quizzes/by-lesson/${lessonId}/history`),
}
