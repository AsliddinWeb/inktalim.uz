# Admin — Darslar CRUD
# Kurs ichidagi darslarni yaratish, tahrirlash, nashr qilish va tartib o'zgartirish
# URL prefiksi: /admin/courses/{course_id}/lessons/...

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.user import User
from app.schemas.lesson import (
    LessonCreate,
    LessonListResponse,
    LessonResponse,
    LessonUpdate,
)

router = APIRouter()


# ─── Yordamchi schemalar ─────────────────────────────────────────────────────

class ReorderItem(BaseModel):
    """Dars tartibi o'zgartirish uchun — dars ID va yangi tartib raqami."""
    id: uuid.UUID
    order: int = Field(..., ge=0)


class ReorderRequest(BaseModel):
    """Darslar tartibini o'zgartirish uchun so'rov."""
    items: list[ReorderItem] = Field(..., min_length=1)


# ─── Yordamchi funksiyalar ────────────────────────────────────────────────────

async def _get_course_or_404(course_id: uuid.UUID, db: AsyncSession) -> Course:
    """Kursni DB dan olish, topilmasa 404."""
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kurs topilmadi (ID: {course_id}).",
        )
    return course


async def _get_lesson_or_404(
    lesson_id: uuid.UUID,
    course_id: uuid.UUID,
    db: AsyncSession,
) -> Lesson:
    """Darsni DB dan olish, topilmasa 404. Kursga tegishliligini ham tekshiradi."""
    result = await db.execute(
        select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
    )
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dars topilmadi (ID: {lesson_id}, kurs ID: {course_id}).",
        )
    return lesson


# ─── Endpointlar ─────────────────────────────────────────────────────────────

@router.post(
    "/{course_id}/lessons",
    response_model=LessonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Kursga yangi dars qo'shish",
)
async def create_lesson(
    course_id: uuid.UUID,
    body: LessonCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> Lesson:
    """
    Kursga yangi dars qo'shish.

    - Kurs mavjud emas → 404
    - body.course_id URL dagi course_id bilan mos bo'lishi kerak
    """
    # Kurs mavjudligini tekshirish
    await _get_course_or_404(course_id, db)

    # URL dagi course_id va body dagi course_id mos bo'lishi kerak
    if body.course_id != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="So'rovdagi kurs ID URL dagi kurs ID bilan mos emas.",
        )

    # Modul kursga tegishliligini tekshirish
    if body.module_id:
        mod_result = await db.execute(
            select(Module).where(Module.id == body.module_id, Module.course_id == course_id)
        )
        if not mod_result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Modul bu kursga tegishli emas.")

    new_lesson = Lesson(
        course_id=course_id,
        module_id=body.module_id,
        title=body.title,
        content=body.content,
        video_url=body.video_url,
        order=body.order,
        duration_minutes=body.duration_minutes,
        is_published=body.is_published,
    )
    db.add(new_lesson)
    await db.flush()
    await db.refresh(new_lesson)
    return new_lesson


@router.get(
    "/{course_id}/lessons",
    response_model=LessonListResponse,
    summary="Kursning barcha darslari",
)
async def list_lessons(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> LessonListResponse:
    """
    Berilgan kursning barcha darslari (order bo'yicha o'suvchi tartibda).

    Nashr qilinmagan darslar ham ko'rsatiladi (admin uchun).
    """
    # Kurs mavjudligini tekshirish
    await _get_course_or_404(course_id, db)

    result = await db.execute(
        select(Lesson)
        .where(Lesson.course_id == course_id)
        .order_by(Lesson.order.asc())
    )
    lessons = result.scalars().all()

    return LessonListResponse(total=len(lessons), items=list(lessons))


@router.get(
    "/{course_id}/lessons/{lesson_id}",
    response_model=LessonResponse,
    summary="Bitta dars ma'lumotlari",
)
async def get_lesson(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> Lesson:
    """Kurs darslaridan birini to'liq ma'lumotlari bilan olish."""
    return await _get_lesson_or_404(lesson_id, course_id, db)


@router.put(
    "/{course_id}/lessons/{lesson_id}",
    response_model=LessonResponse,
    summary="Darsni tahrirlash",
)
async def update_lesson(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    body: LessonUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> Lesson:
    """
    Dars sarlavhasi, matni, video URL, davomiyligi va boshqa maydonlarni yangilash.
    """
    lesson = await _get_lesson_or_404(lesson_id, course_id, db)

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(lesson, field, value)

    db.add(lesson)
    await db.flush()
    await db.refresh(lesson)
    return lesson


@router.patch(
    "/{course_id}/lessons/{lesson_id}/publish",
    response_model=LessonResponse,
    summary="Darsni nashr qilish / nashrdan chiqarish",
)
async def toggle_publish_lesson(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> Lesson:
    """
    Dars nashr holatini almashtirish (toggle).

    is_published: False → True yoki True → False
    """
    lesson = await _get_lesson_or_404(lesson_id, course_id, db)

    lesson.is_published = not lesson.is_published
    db.add(lesson)
    await db.flush()
    await db.refresh(lesson)
    return lesson


@router.delete(
    "/{course_id}/lessons/{lesson_id}",
    status_code=status.HTTP_200_OK,
    summary="Darsni o'chirish",
)
async def delete_lesson(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> dict:
    """
    Darsni o'chirish.

    Cascade: darsga tegishli barcha progress yozuvlari ham o'chadi.
    """
    lesson = await _get_lesson_or_404(lesson_id, course_id, db)
    title = lesson.title

    await db.delete(lesson)
    await db.flush()

    return {"message": f"'{title}' darsi muvaffaqiyatli o'chirildi."}


@router.put(
    "/{course_id}/lessons/reorder",
    status_code=status.HTTP_200_OK,
    summary="Darslar tartibini o'zgartirish",
)
async def reorder_lessons(
    course_id: uuid.UUID,
    body: ReorderRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> dict:
    """
    Bir necha darsning tartib raqamini (order) bir vaqtda yangilash.

    So'rov: [{"id": "uuid", "order": 0}, {"id": "uuid2", "order": 1}, ...]
    Barcha darslar berilgan kursga tegishli bo'lishi kerak.
    """
    # Kurs mavjudligini tekshirish
    await _get_course_or_404(course_id, db)

    for item in body.items:
        result = await db.execute(
            select(Lesson).where(
                Lesson.id == item.id,
                Lesson.course_id == course_id,
            )
        )
        lesson = result.scalar_one_or_none()

        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Dars topilmadi yoki bu kursga tegishli emas (ID: {item.id})."
                ),
            )

        lesson.order = item.order
        db.add(lesson)

    await db.flush()
    return {
        "message": f"{len(body.items)} ta dars tartibi muvaffaqiyatli yangilandi."
    }
