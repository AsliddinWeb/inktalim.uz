// Vue Router konfiguratsiyasi — barcha route larni va navigation guard larni belgilaydi
// requiresAuth: token talab qiluvchi sahifalar
// requiresAdmin: faqat admin uchun sahifalar

import { createRouter, createWebHistory } from 'vue-router'

// ─── Lazy-loaded view larni import qilish ────────────────────────────────────

// Auth sahifalari
const LoginView    = () => import('@/views/auth/LoginView.vue')
const RegisterView = () => import('@/views/auth/RegisterView.vue')

// 404 sahifa
const NotFoundView = () => import('@/views/NotFoundView.vue')

// Student sahifalari
const StudentDashboard    = () => import('@/views/student/DashboardView.vue')
const StudentCourses      = () => import('@/views/student/CoursesView.vue')
const StudentCourseDetail = () => import('@/views/student/CourseDetailView.vue')
const StudentLesson       = () => import('@/views/student/LessonView.vue')
const StudentQuiz         = () => import('@/views/student/QuizView.vue')
const StudentCertificates = () => import('@/views/student/CertificatesView.vue')
const StudentCertificate  = () => import('@/views/student/CertificateView.vue')

// Landing (ochiq sahifa)
const LandingView = () => import('@/views/LandingView.vue')
const StudentProgress     = () => import('@/views/student/ProgressView.vue')
const StudentProfile      = () => import('@/views/student/ProfileView.vue')

// Admin sahifalari
const AdminDashboard    = () => import('@/views/admin/AdminDashboardView.vue')
const AdminCourses      = () => import('@/views/admin/AdminCoursesView.vue')
const AdminCourseDetail = () => import('@/views/admin/AdminCourseDetailView.vue')
const AdminUsers        = () => import('@/views/admin/AdminUsersView.vue')
const AdminProfile      = () => import('@/views/admin/AdminProfileView.vue')

// ─── Layoutlar ───────────────────────────────────────────────────────────────
const AuthLayout    = () => import('@/layouts/AuthLayout.vue')
const StudentLayout = () => import('@/layouts/StudentLayout.vue')
const AdminLayout   = () => import('@/layouts/AdminLayout.vue')

// ─── Route lari ───────────────────────────────────────────────────────────────
const routes = [
  // ─── Landing sahifa — hammaga ochiq ──────────────────────────────────────
  {
    path: '/',
    name: 'Landing',
    component: LandingView,
    meta: { title: 'InkTalim.Uz — Bepul Online Ta\'lim Platformasi' },
  },

  // ─── Auth sahifalari (faqat login bo'lmaganlar uchun) ───────────────────
  {
    path: '/login',
    component: AuthLayout,
    meta: { guestOnly: true },
    children: [
      {
        path: '',
        name: 'Login',
        component: LoginView,
        meta: { title: 'Kirish — InkTalim.Uz', guestOnly: true },
      },
    ],
  },
  {
    path: '/register',
    component: AuthLayout,
    meta: { guestOnly: true },
    children: [
      {
        path: '',
        name: 'Register',
        component: RegisterView,
        meta: { title: 'Ro\'yxatdan o\'tish — InkTalim.Uz', guestOnly: true },
      },
    ],
  },

  // ─── Student sahifalari (login bo'lgan har qanday foydalanuvchi) ─────────
  {
    path: '/dashboard',
    component: StudentLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'StudentDashboard',
        component: StudentDashboard,
        meta: { title: 'Dashboard — InkTalim.Uz', requiresAuth: true },
      },
      {
        path: 'courses',
        name: 'StudentCourses',
        component: StudentCourses,
        meta: { title: 'Kurslar — InkTalim.Uz', requiresAuth: true },
      },
      {
        path: 'courses/:id',
        name: 'StudentCourseDetail',
        component: StudentCourseDetail,
        meta: { title: 'Kurs — InkTalim.Uz', requiresAuth: true },
      },
      {
        path: 'courses/:courseId/lessons/:lessonId',
        name: 'lesson',
        component: StudentLesson,
        meta: { title: 'Dars — InkTalim.Uz', requiresAuth: true },
      },
      {
        path: 'courses/:courseId/lessons/:lessonId/quiz',
        name: 'quiz',
        component: StudentQuiz,
        meta: { title: 'Test — InkTalim.Uz', requiresAuth: true },
      },
      {
        path: 'progress',
        name: 'StudentProgress',
        component: StudentProgress,
        meta: { title: 'Mening progressim — InkTalim.Uz', requiresAuth: true },
      },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: StudentProfile,
        meta: { title: 'Profilim — InkTalim.Uz', requiresAuth: true },
      },
      {
        path: 'certificates',
        name: 'StudentCertificates',
        component: StudentCertificates,
        meta: { title: 'Sertifikatlarim — InkTalim.Uz', requiresAuth: true },
      },
      {
        path: 'certificates/:number',
        name: 'StudentCertificate',
        component: StudentCertificate,
        meta: { title: 'Sertifikat — InkTalim.Uz', requiresAuth: true },
      },
    ],
  },

  // ─── Admin sahifalari (faqat admin rolida) ────────────────────────────────
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { title: 'Admin Panel — InkTalim.Uz', requiresAuth: true, requiresAdmin: true },
      },
      {
        path: 'courses',
        name: 'AdminCourses',
        component: AdminCourses,
        meta: { title: 'Kurslar boshqaruvi — InkTalim.Uz', requiresAuth: true, requiresAdmin: true },
      },
      {
        path: 'courses/:id',
        name: 'AdminCourseDetail',
        component: AdminCourseDetail,
        meta: { title: 'Kurs darslar — InkTalim.Uz', requiresAuth: true, requiresAdmin: true },
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers,
        meta: { title: 'Foydalanuvchilar — InkTalim.Uz', requiresAuth: true, requiresAdmin: true },
      },
      {
        path: 'profile',
        name: 'AdminProfile',
        component: AdminProfile,
        meta: { title: 'Admin Profil — InkTalim.Uz', requiresAuth: true, requiresAdmin: true },
      },
    ],
  },

  // ─── 404 — Topilmadi ─────────────────────────────────────────────────────
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView,
    meta: { title: 'Sahifa topilmadi — InkTalim.Uz' },
  },
]

// ─── Router yaratish ──────────────────────────────────────────────────────────
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
})

// ─── Navigation Guard ─────────────────────────────────────────────────────────
router.beforeEach((to, from, next) => {
  if (to.meta?.title) {
    document.title = to.meta.title
  }

  const accessToken = localStorage.getItem('edu-access-token')
  const userRaw     = localStorage.getItem('edu-user')
  const user        = userRaw ? JSON.parse(userRaw) : null
  const isAuthenticated = !!accessToken && !!user
  const isAdmin         = user?.is_admin === true

  // Faqat mehmonlar uchun sahifalar
  if (to.meta?.guestOnly && isAuthenticated) {
    return next(isAdmin ? '/admin' : '/dashboard')
  }

  // Autentifikatsiya talab qiluvchan sahifalar
  if (to.meta?.requiresAuth && !isAuthenticated) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  // Admin talab qiluvchan sahifalar
  if (to.meta?.requiresAdmin && !isAdmin) {
    return next('/dashboard')
  }

  next()
})

export default router
