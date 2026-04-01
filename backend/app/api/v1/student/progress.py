# Student — Progress tracking API
# Darsni tugatilgan/tugatilmagan qilib belgilash
# Foydalanuvchi barcha kurslardagi yoki bitta kurs progressini ko'rish

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.user import User

router = APIRouter()


# ─── Javob schemalari ─────────────────────────────────────────────────────────

class CompleteResponse(BaseModel):
    """Dars tugatilganda qaytariladigan javob."""
    message: str
    lesson_id: uuid.UUID
    is_completed: bool
    course_progress_percent: float = Field(..., description="Kurs bo'yicha umumiy foiz")


class LessonProgressItem(BaseModel):
    """Kurs progressi detail sahifasida har bir dars uchun."""
    id: uuid.UUID
    title: str
    order: int
    is_completed: bool
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class CourseProgressSummary(BaseModel):
    """Kurslar ro'yxatidagi progress uchun qisqa ma'lumot."""
    course_id: uuid.UUID
    course_title: str
    course_thumbnail: str | None
    lessons_count: int
    completed_lessons: int
    progress_percent: float


class CourseProgressDetail(BaseModel):
    """Bitta kurs progressi batafsil."""
    course_id: uuid.UUID
    course_title: str
    course_thumbnail: str | None
    lessons_count: int
    completed_lessons: int
    progress_percent: float
    lessons: list[LessonProgressItem]


# ─── Yordamchi funksiyalar ────────────────────────────────────────────────────

def _calc_percent(completed: int, total: int) -> float:
    """Foizni hisoblash. Total=0 bo'lsa 0.0 qaytaradi."""
    if total == 0:
        return 0.0
    return round(completed / total * 100, 1)


async def _get_course_progress_percent(
    course_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession,
) -> float:
    """Berilgan kurs bo'yicha foydalanuvchi progress foizini hisoblash."""
    # Nashr qilingan darslar soni
    total_result = await db.execute(
        select(func.count()).where(
            Lesson.course_id == course_id,
            Lesson.is_published == True,  # noqa: E712
        )
    )
    total = total_result.scalar_one()

    # Tugatilgan darslar soni
    completed_result = await db.execute(
        select(func.count()).where(
            Progress.course_id == course_id,
            Progress.user_id == user_id,
            Progress.is_completed == True,  # noqa: E712
        )
    )
    completed = completed_result.scalar_one()

    return _calc_percent(completed, total)


async def _get_or_create_progress(
    user_id: uuid.UUID,
    lesson_id: uuid.UUID,
    course_id: uuid.UUID,
    db: AsyncSession,
) -> Progress:
    """Progress yozuvini olish yoki yangi yaratish."""
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user_id,
            Progress.lesson_id == lesson_id,
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = Progress(
            user_id=user_id,
            lesson_id=lesson_id,
            course_id=course_id,
            is_completed=False,
            completed_at=None,
        )
        db.add(progress)
        await db.flush()

    return progress


# ─── Endpointlar ─────────────────────────────────────────────────────────────

@router.post(
    "/lessons/{lesson_id}/complete",
    response_model=CompleteResponse,
    summary="Darsni tugatilgan deb belgilash",
)
async def complete_lesson(
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CompleteResponse:
    """
    Darsni tugatilgan (is_completed=True) deb belgilash.

    - Dars mavjud emas → 404
    - Dars nashr qilinmagan → 404
    - Allaqachon tugatilgan bo'lsa — idempotent (qayta belgilash mumkin)
    - Javobda kurs bo'yicha yangilangan progress foizi qaytariladi
    """
    # Dars mavjudligi va nashr holatini tekshirish
    lesson_result = await db.execute(
        select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.is_published == True,  # noqa: E712
        )
    )
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dars topilmadi yoki hali nashr qilinmagan.",
        )

    # Progress yozuvini olish yoki yaratish
    progress = await _get_or_create_progress(
        user_id=current_user.id,
        lesson_id=lesson_id,
        course_id=lesson.course_id,
        db=db,
    )

    # Tugatilgan deb belgilash
    progress.is_completed = True
    progress.completed_at = datetime.now(timezone.utc)
    db.add(progress)
    await db.flush()

    # Yangilangan kurs foizini hisoblash
    course_percent = await _get_course_progress_percent(
        lesson.course_id, current_user.id, db
    )

    return CompleteResponse(
        message="Dars muvaffaqiyatli tugatildi.",
        lesson_id=lesson_id,
        is_completed=True,
        course_progress_percent=course_percent,
    )


@router.delete(
    "/lessons/{lesson_id}/complete",
    response_model=CompleteResponse,
    summary="Darsni tugatilmagan qilib qaytarish",
)
async def uncomplete_lesson(
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CompleteResponse:
    """
    Darsni tugatilmagan (is_completed=False) qilib qaytarish.

    - Dars mavjud emas → 404
    - Progress yozuvi yo'q bo'lsa → 404 (dars hech ochilmagan)
    - Javobda yangilangan kurs foizi qaytariladi
    """
    # Dars mavjudligini tekshirish
    lesson_result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dars topilmadi.",
        )

    # Progress yozuvini olish
    progress_result = await db.execute(
        select(Progress).where(
            Progress.user_id == current_user.id,
            Progress.lesson_id == lesson_id,
        )
    )
    progress = progress_result.scalar_one_or_none()

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bu dars uchun progress yozuvi topilmadi. Avval darsni oching.",
        )

    # Tugatilmagan qilib belgilash
    progress.is_completed = False
    progress.completed_at = None
    db.add(progress)
    await db.flush()

    # Yangilangan kurs foizini hisoblash
    course_percent = await _get_course_progress_percent(
        lesson.course_id, current_user.id, db
    )

    return CompleteResponse(
        message="Dars tugatilmagan qilib belgilandi.",
        lesson_id=lesson_id,
        is_completed=False,
        course_progress_percent=course_percent,
    )


@router.get(
    "",
    response_model=list[CourseProgressSummary],
    summary="Foydalanuvchi barcha kurslardagi progressi",
)
async def get_all_progress(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CourseProgressSummary]:
    """
    Foydalanuvchi boshlagan barcha kurslar bo'yicha progress ro'yxati.

    Faqat user birorta darsini ochgan (progress yozuvi mavjud) kurslar ko'rinadi.
    Natija: kurs nomi, umumiy darslar, tugatilgan darslar, foiz.
    """
    # Foydalanuvchi progress yozuvlari mavjud kurslar ID lari
    enrolled_result = await db.execute(
        select(Progress.course_id)
        .where(Progress.user_id == current_user.id)
        .distinct()
    )
    enrolled_course_ids = enrolled_result.scalars().all()

    if not enrolled_course_ids:
        return []

    # Bu kurslarni olish (nashr qilingan bo'lsin)
    courses_result = await db.execute(
        select(Course).where(
            Course.id.in_(enrolled_course_ids),
            Course.is_published == True,  # noqa: E712
        ).order_by(Course.order.asc())
    )
    courses = courses_result.scalars().all()

    summaries = []
    for course in courses:
        # Nashr qilingan darslar soni
        total_result = await db.execute(
            select(func.count()).where(
                Lesson.course_id == course.id,
                Lesson.is_published == True,  # noqa: E712
            )
        )
        total = total_result.scalar_one()

        # Tugatilgan darslar soni
        completed_result = await db.execute(
            select(func.count()).where(
                Progress.course_id == course.id,
                Progress.user_id == current_user.id,
                Progress.is_completed == True,  # noqa: E712
            )
        )
        completed = completed_result.scalar_one()

        summaries.append(
            CourseProgressSummary(
                course_id=course.id,
                course_title=course.title,
                course_thumbnail=course.thumbnail_url,
                lessons_count=total,
                completed_lessons=completed,
                progress_percent=_calc_percent(completed, total),
            )
        )

    return summaries


@router.get(
    "/{course_id}",
    response_model=CourseProgressDetail,
    summary="Bitta kurs progressi batafsil",
)
async def get_course_progress(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CourseProgressDetail:
    """
    Bitta kurs bo'yicha batafsil progress.

    Javobda:
    - Kurs asosiy ma'lumotlari
    - Har bir nashr qilingan dars: title, order, is_completed, completed_at
    - Umumiy foiz

    Kurs topilmasa yoki nashr qilinmagan → 404
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

    # Nashr qilingan darslar (tartib bo'yicha)
    lessons_result = await db.execute(
        select(Lesson)
        .where(
            Lesson.course_id == course_id,
            Lesson.is_published == True,  # noqa: E712
        )
        .order_by(Lesson.order.asc())
    )
    lessons = lessons_result.scalars().all()

    # Foydalanuvchi progressini bir so'rovda olish
    if lessons:
        lesson_ids = [l.id for l in lessons]
        progress_result = await db.execute(
            select(Progress).where(
                Progress.user_id == current_user.id,
                Progress.lesson_id.in_(lesson_ids),
            )
        )
        progress_map: dict[uuid.UUID, Progress] = {
            p.lesson_id: p for p in progress_result.scalars().all()
        }
    else:
        progress_map = {}

    # Dars progress elementlarini shakllantirish
    lesson_items = []
    completed_count = 0

    for lesson in lessons:
        prog = progress_map.get(lesson.id)
        is_completed = prog.is_completed if prog else False
        completed_at = prog.completed_at if prog else None

        if is_completed:
            completed_count += 1

        lesson_items.append(
            LessonProgressItem(
                id=lesson.id,
                title=lesson.title,
                order=lesson.order,
                is_completed=is_completed,
                completed_at=completed_at,
            )
        )

    total = len(lessons)

    return CourseProgressDetail(
        course_id=course.id,
        course_title=course.title,
        course_thumbnail=course.thumbnail_url,
        lessons_count=total,
        completed_lessons=completed_count,
        progress_percent=_calc_percent(completed_count, total),
        lessons=lesson_items,
    )
