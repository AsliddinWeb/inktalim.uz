# Student — Dars ko'rish API
# Dars ochilganda avtomatik progress yozuvi yaratiladi (is_completed=False)
# Oldingi va keyingi dars ma'lumotlari ham qaytariladi

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.user import User

router = APIRouter()


# ─── Javob schemalari ─────────────────────────────────────────────────────────

class AdjacentLesson(BaseModel):
    """Oldingi yoki keyingi dars uchun qisqa ma'lumot."""
    id: uuid.UUID
    title: str
    order: int


class LessonDetailResponse(BaseModel):
    """Dars detail sahifasi uchun to'liq javob."""
    id: uuid.UUID
    course_id: uuid.UUID
    title: str
    content: str
    video_url: str | None
    order: int
    duration_minutes: int | None
    is_completed: bool = False
    # Navigatsiya uchun qo'shni darslar
    prev_lesson: AdjacentLesson | None = None
    next_lesson: AdjacentLesson | None = None

    model_config = {"from_attributes": True}


# ─── Yordamchi funksiyalar ────────────────────────────────────────────────────

async def _ensure_progress_started(
    user_id: uuid.UUID,
    lesson: Lesson,
    db: AsyncSession,
) -> Progress:
    """
    Dars ochilganda progress yozuvini yaratish (agar mavjud bo'lmasa).

    is_completed=False — "darsni boshladi, lekin tugatmadi" holati.
    Agar yozuv allaqachon mavjud bo'lsa — o'zgartirilmaydi.
    """
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user_id,
            Progress.lesson_id == lesson.id,
        )
    )
    existing = result.scalar_one_or_none()

    if not existing:
        # Yangi progress yozuvi yaratish
        new_progress = Progress(
            user_id=user_id,
            lesson_id=lesson.id,
            course_id=lesson.course_id,
            is_completed=False,
            completed_at=None,
        )
        db.add(new_progress)
        await db.flush()
        return new_progress

    return existing


# ─── Endpointlar ─────────────────────────────────────────────────────────────

@router.get(
    "/{course_id}/lessons/{lesson_id}",
    response_model=LessonDetailResponse,
    summary="Dars ko'rish (to'liq content)",
)
async def get_lesson_detail(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LessonDetailResponse:
    """
    Dars to'liq ma'lumotlarini ko'rish.

    Shartlar:
    - Kurs nashr qilingan bo'lishi kerak → aks holda 404
    - Dars nashr qilingan bo'lishi kerak → aks holda 404
    - Dars berilgan kursga tegishli bo'lishi kerak → aks holda 404

    Side effect:
    - Dars birinchi marta ochilganda Progress yozuvi yaratiladi (is_completed=False)
    - Keyingi ochilishlarda Progress o'zgartirilmaydi

    Javobda:
    - Dars to'liq ma'lumotlari (title, content, video_url, duration_minutes)
    - is_completed — bu foydalanuvchi uchun
    - prev_lesson / next_lesson — navigatsiya uchun
    """
    # Kurs mavjudligi va nashr holatini tekshirish
    course_result = await db.execute(
        select(Course).where(
            Course.id == course_id,
            Course.is_published == True,  # noqa: E712
        )
    )
    course = course_result.scalar_one_or_none()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kurs topilmadi yoki hali nashr qilinmagan.",
        )

    # Dars mavjudligi, nashr holati va kursga tegishliligini tekshirish
    lesson_result = await db.execute(
        select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
            Lesson.is_published == True,  # noqa: E712
        )
    )
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dars topilmadi yoki hali nashr qilinmagan.",
        )

    # Progress yozuvini yaratish / olish (side effect)
    progress = await _ensure_progress_started(current_user.id, lesson, db)

    # Kursning barcha nashr qilingan darslari tartib bo'yicha
    all_lessons_result = await db.execute(
        select(Lesson)
        .where(
            Lesson.course_id == course_id,
            Lesson.is_published == True,  # noqa: E712
        )
        .order_by(Lesson.order.asc())
    )
    all_lessons = all_lessons_result.scalars().all()

    # Joriy darsning indeksini topish
    current_index = next(
        (i for i, l in enumerate(all_lessons) if l.id == lesson_id),
        None,
    )

    # Oldingi va keyingi darslarni aniqlash
    prev_lesson: AdjacentLesson | None = None
    next_lesson: AdjacentLesson | None = None

    if current_index is not None:
        if current_index > 0:
            prev = all_lessons[current_index - 1]
            prev_lesson = AdjacentLesson(
                id=prev.id,
                title=prev.title,
                order=prev.order,
            )
        if current_index < len(all_lessons) - 1:
            nxt = all_lessons[current_index + 1]
            next_lesson = AdjacentLesson(
                id=nxt.id,
                title=nxt.title,
                order=nxt.order,
            )

    return LessonDetailResponse(
        id=lesson.id,
        course_id=lesson.course_id,
        title=lesson.title,
        content=lesson.content,
        video_url=lesson.video_url,
        order=lesson.order,
        duration_minutes=lesson.duration_minutes,
        is_completed=progress.is_completed,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
    )
