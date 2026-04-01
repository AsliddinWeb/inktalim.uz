# Barcha v1 routerlarni birlashtiruvchi asosiy router
# app/main.py da shu router /api/v1 prefiksi bilan ulanadi

from fastapi import APIRouter, Depends

from app.api.v1 import auth
from app.api.v1 import upload
from app.api.v1 import public as public_routes
from app.api.v1.admin import courses as admin_courses
from app.api.v1.admin import lessons as admin_lessons
from app.api.v1.admin import modules as admin_modules
from app.api.v1.admin import quizzes as admin_quizzes
from app.api.v1.admin import users as admin_users
from app.api.v1.student import courses as student_courses
from app.api.v1.student import lessons as student_lessons
from app.api.v1.student import progress as student_progress
from app.api.v1.student import quizzes as student_quizzes
from app.api.v1.student import certificates as student_certificates
from app.core.dependencies import get_current_user

# Asosiy v1 router
api_router = APIRouter()

# ─── Ochiq endpointlar — /api/v1/public/... (token talab qilinmaydi) ─────────
api_router.include_router(
    public_routes.router,
    prefix="/public",
    tags=["Ochiq — Kurslar"],
)

# ─── Auth endpointlari — /api/v1/auth/... ────────────────────────────────────
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

# ─── Fayl yuklash — /api/v1/upload/... ───────────────────────────────────────
# thumbnail va avatar yuklash
api_router.include_router(
    upload.router,
    prefix="/upload",
    tags=["Upload"],
    dependencies=[Depends(get_current_user)],
)

# ─── Admin endpointlari (faqat adminlar) ─────────────────────────────────────

# Foydalanuvchilar — /api/v1/admin/users/...
api_router.include_router(
    admin_users.router,
    prefix="/admin/users",
    tags=["Admin — Foydalanuvchilar"],
)

# Kurslar — /api/v1/admin/courses/...
api_router.include_router(
    admin_courses.router,
    prefix="/admin/courses",
    tags=["Admin — Kurslar"],
)

# Modullar — /api/v1/admin/courses/{course_id}/modules/...
api_router.include_router(
    admin_modules.router,
    prefix="/admin/courses",
    tags=["Admin — Modullar"],
)

# Darslar — /api/v1/admin/courses/{course_id}/lessons/...
api_router.include_router(
    admin_lessons.router,
    prefix="/admin/courses",
    tags=["Admin — Darslar"],
)

# Quizlar — /api/v1/admin/quizzes/...
api_router.include_router(
    admin_quizzes.router,
    prefix="/admin/quizzes",
    tags=["Admin — Quizlar"],
)

# ─── Student endpointlari (login bo'lgan har qanday foydalanuvchi) ────────────
# dependencies=[Depends(get_current_user)] — barcha student routerlarga token talab

# Kurslar ro'yxati va detail — /api/v1/student/courses/...
api_router.include_router(
    student_courses.router,
    prefix="/student/courses",
    tags=["Student — Kurslar"],
    dependencies=[Depends(get_current_user)],
)

# Dars ko'rish — /api/v1/student/courses/{course_id}/lessons/...
api_router.include_router(
    student_lessons.router,
    prefix="/student/courses",
    tags=["Student — Darslar"],
    dependencies=[Depends(get_current_user)],
)

# Progress tracking — /api/v1/student/progress/...
api_router.include_router(
    student_progress.router,
    prefix="/student/progress",
    tags=["Student — Progress"],
    dependencies=[Depends(get_current_user)],
)

# Quiz — /api/v1/student/quizzes/...
api_router.include_router(
    student_quizzes.router,
    prefix="/student/quizzes",
    tags=["Student — Quizlar"],
    dependencies=[Depends(get_current_user)],
)

# Sertifikatlar — /api/v1/student/certificates/...
api_router.include_router(
    student_certificates.router,
    prefix="/student/certificates",
    tags=["Student — Sertifikatlar"],
    dependencies=[Depends(get_current_user)],
)
