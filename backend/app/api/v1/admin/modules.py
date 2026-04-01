# Admin — Modullar CRUD
# Kurs ichidagi modullarni yaratish, tahrirlash, o'chirish
# URL prefiksi: /admin/courses/{course_id}/modules/...

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.user import User
from app.schemas.lesson import LessonResponse
from app.schemas.module import ModuleCreate, ModuleResponse, ModuleUpdate, ModuleWithLessons

router = APIRouter()


class ReorderItem(BaseModel):
    id: uuid.UUID
    order: int = Field(..., ge=0)


class ReorderRequest(BaseModel):
    items: list[ReorderItem] = Field(..., min_length=1)


# ─── Yordamchilar ─────────────────────────────────────────────────────────────

async def _get_course_or_404(course_id: uuid.UUID, db: AsyncSession) -> Course:
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail=f"Kurs topilmadi (ID: {course_id}).")
    return course


async def _get_module_or_404(module_id: uuid.UUID, course_id: uuid.UUID, db: AsyncSession) -> Module:
    result = await db.execute(
        select(Module).where(Module.id == module_id, Module.course_id == course_id)
    )
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail=f"Modul topilmadi (ID: {module_id}).")
    return module


async def _build_module_with_lessons(module: Module, db: AsyncSession) -> ModuleWithLessons:
    result = await db.execute(
        select(Lesson)
        .where(Lesson.module_id == module.id)
        .order_by(Lesson.order.asc())
    )
    lessons = result.scalars().all()
    lesson_responses = [LessonResponse.model_validate(l) for l in lessons]
    return ModuleWithLessons(
        id=module.id,
        course_id=module.course_id,
        title=module.title,
        description=module.description,
        order=module.order,
        is_published=module.is_published,
        created_at=module.created_at,
        updated_at=module.updated_at,
        lessons_count=len(lessons),
        lessons=lesson_responses,
    )


# ─── Endpointlar ─────────────────────────────────────────────────────────────

@router.post(
    "/{course_id}/modules",
    response_model=ModuleWithLessons,
    status_code=status.HTTP_201_CREATED,
    summary="Kursga yangi modul qo'shish",
)
async def create_module(
    course_id: uuid.UUID,
    body: ModuleCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> ModuleWithLessons:
    await _get_course_or_404(course_id, db)
    module = Module(
        course_id=course_id,
        title=body.title,
        description=body.description,
        order=body.order,
        is_published=body.is_published,
    )
    db.add(module)
    await db.flush()
    await db.refresh(module)
    return await _build_module_with_lessons(module, db)


@router.get(
    "/{course_id}/modules",
    response_model=list[ModuleWithLessons],
    summary="Kursning barcha modullari (darslar bilan)",
)
async def list_modules(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> list[ModuleWithLessons]:
    await _get_course_or_404(course_id, db)
    result = await db.execute(
        select(Module)
        .where(Module.course_id == course_id)
        .order_by(Module.order.asc())
    )
    modules = result.scalars().all()
    return [await _build_module_with_lessons(m, db) for m in modules]


@router.put(
    "/{course_id}/modules/{module_id}",
    response_model=ModuleResponse,
    summary="Modulni tahrirlash",
)
async def update_module(
    course_id: uuid.UUID,
    module_id: uuid.UUID,
    body: ModuleUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> Module:
    module = await _get_module_or_404(module_id, course_id, db)
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(module, field, value)
    db.add(module)
    await db.flush()
    await db.refresh(module)
    return module


@router.patch(
    "/{course_id}/modules/{module_id}/publish",
    response_model=ModuleResponse,
    summary="Modulni nashr qilish / nashrdan chiqarish",
)
async def toggle_publish_module(
    course_id: uuid.UUID,
    module_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> Module:
    module = await _get_module_or_404(module_id, course_id, db)
    module.is_published = not module.is_published
    db.add(module)
    await db.flush()
    await db.refresh(module)
    return module


@router.delete(
    "/{course_id}/modules/{module_id}",
    status_code=status.HTTP_200_OK,
    summary="Modulni o'chirish",
)
async def delete_module(
    course_id: uuid.UUID,
    module_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> dict:
    module = await _get_module_or_404(module_id, course_id, db)
    title = module.title
    await db.delete(module)
    await db.flush()
    return {"message": f"'{title}' moduli muvaffaqiyatli o'chirildi."}


@router.put(
    "/{course_id}/modules/reorder",
    status_code=status.HTTP_200_OK,
    summary="Modullar tartibini o'zgartirish",
)
async def reorder_modules(
    course_id: uuid.UUID,
    body: ReorderRequest,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
) -> dict:
    await _get_course_or_404(course_id, db)
    for item in body.items:
        result = await db.execute(
            select(Module).where(Module.id == item.id, Module.course_id == course_id)
        )
        module = result.scalar_one_or_none()
        if not module:
            raise HTTPException(status_code=404, detail=f"Modul topilmadi (ID: {item.id}).")
        module.order = item.order
        db.add(module)
    await db.flush()
    return {"message": f"{len(body.items)} ta modul tartibi yangilandi."}
