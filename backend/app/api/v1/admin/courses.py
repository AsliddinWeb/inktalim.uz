# Admin — Kurslar CRUD
# Kurs yaratish, tahrirlash, nashr qilish, o'chirish va tartib o'zgartirish
# Faqat admin huquqiga ega foydalanuvchilar uchun

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.course import (
    CourseCreate,
    CourseListResponse,
    CourseResponse,
    CourseUpdate,
)

router = APIRouter()


# ─── Yordamchi schemalar ─────────────────────────────────────────────────────

class ReorderItem(BaseModel):
    """Tartib o'zgartirish uchun — kurs ID va yangi tartib raqami."""
    id: uuid.UUID
    order: int = Field(..., ge=0)


class ReorderRequest(BaseModel):
    """Kurslar tartibini o'zgartirish uchun so'rov."""
    items: list[ReorderItem] = Field(..., min_length=1)


# ─── Yordamchi funksiya ───────────────────────────────────────────────────────

async def _get_course_or_404(course_id: uuid.UUID, db: AsyncSession) -> Course:
    """Kursni DB dan olish, topilmasa 404 qaytarish."""
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kurs topilmadi (ID: {course_id}).",
        )
    return course


async def _build_course_response(course: Course, db: AsyncSession) -> CourseResponse:
    """Kurs javobini darslar soni bilan birga yaratish."""
    count_result = await db.execute(
        select(func.count()).where(Lesson.course_id == course.id)
    )
    lessons_count = count_result.scalar_one()

    response = CourseResponse.model_validate(course)
    response.lessons_count = lessons_count
    return response


# ─── Endpointlar ─────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi kurs yaratish",
)
async def create_course(
    body: CourseCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
) -> CourseResponse:
    """
    Yangi kurs yaratish.

    Kurs default holatda nashr qilinmagan (is_published=False).
    """
    new_course = Course(
        title=body.title,
        description=body.description,
        thumbnail_url=body.thumbnail_url,
        is_published=body.is_published,
        order=body.order,
        created_by=admin.id,
    )
    db.add(new_course)
    await db.flush()
    await db.refresh(new_course)
    return await _build_course_response(new_course, db)


@router.get(
    "",
    response_model=CourseListResponse,
    summary="Barcha kurslar ro'yxati (admin)",
)
async def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    published_only: bool = Query(False, description="Faqat nashr qilinganlarni ko'rsatish"),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> CourseListResponse:
    """
    Barcha kurslar ro'yxati (nashr qilingan va draft).

    - published_only=true: faqat nashr qilinganlar
    - Tartib: order maydoni bo'yicha o'suvchi tartibda
    """
    query = select(Course)

    if published_only:
        query = query.where(Course.is_published == True)  # noqa: E712

    # Jami son
    count_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = count_result.scalar_one()

    # Tartib va pagination
    query = query.order_by(Course.order.asc(), Course.created_at.desc())
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    courses = result.scalars().all()

    # Har bir kurs uchun darslar sonini hisoblash
    items = []
    for course in courses:
        items.append(await _build_course_response(course, db))

    return CourseListResponse(total=total, items=items)


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Bitta kurs ma'lumotlari",
)
async def get_course(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> CourseResponse:
    """Kurs ma'lumotlari + darslar soni."""
    course = await _get_course_or_404(course_id, db)
    return await _build_course_response(course, db)


@router.put(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Kursni tahrirlash",
)
async def update_course(
    course_id: uuid.UUID,
    body: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> CourseResponse:
    """Kurs sarlavhasi, tavsifi, muqovasi va boshqa maydonlarini yangilash."""
    course = await _get_course_or_404(course_id, db)

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(course, field, value)

    db.add(course)
    await db.flush()
    await db.refresh(course)
    return await _build_course_response(course, db)


@router.patch(
    "/{course_id}/publish",
    response_model=CourseResponse,
    summary="Kursni nashr qilish / nashrdan chiqarish",
)
async def toggle_publish_course(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> CourseResponse:
    """
    Kurs nashr holatini almashtirish (toggle).

    is_published: False → True yoki True → False
    """
    course = await _get_course_or_404(course_id, db)

    course.is_published = not course.is_published
    db.add(course)
    await db.flush()
    await db.refresh(course)

    state = "nashr qilindi" if course.is_published else "nashrdan chiqarildi"
    # Javobda holat xabari log uchun — response model kurs ma'lumotlari
    return await _build_course_response(course, db)


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Kursni o'chirish",
)
async def delete_course(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> dict:
    """
    Kursni o'chirish.

    Cascade: kursga tegishli barcha darslar ham o'chadi (DB darajasida).
    """
    course = await _get_course_or_404(course_id, db)
    title = course.title

    await db.delete(course)
    await db.flush()

    return {"message": f"'{title}' kursi va unga tegishli barcha darslar o'chirildi."}


@router.put(
    "/reorder",
    status_code=status.HTTP_200_OK,
    summary="Kurslar tartibini o'zgartirish",
)
async def reorder_courses(
    body: ReorderRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> dict:
    """
    Bir necha kursning tartib raqamini (order) bir vaqtda yangilash.

    So'rov: [{"id": "uuid", "order": 0}, {"id": "uuid2", "order": 1}, ...]
    """
    for item in body.items:
        result = await db.execute(select(Course).where(Course.id == item.id))
        course = result.scalar_one_or_none()

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kurs topilmadi (ID: {item.id}).",
            )

        course.order = item.order
        db.add(course)

    await db.flush()
    return {"message": f"{len(body.items)} ta kurs tartibi muvaffaqiyatli yangilandi."}
