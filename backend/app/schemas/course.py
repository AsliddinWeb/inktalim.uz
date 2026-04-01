# Kurs Pydantic schemalari — yaratish, yangilash va ko'rsatish uchun

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    """Kurs uchun umumiy maydonlar."""
    title: str = Field(..., min_length=3, max_length=500, description="Kurs nomi")
    description: str = Field('', description="Kurs tavsifi")
    thumbnail_url: str | None = Field(None, max_length=500, description="Muqova rasmi URL")
    is_published: bool = Field(False, description="Nashr holati")
    order: int = Field(0, ge=0, description="Tartibi (0 dan boshlanadi)")


class CourseCreate(CourseBase):
    """Yangi kurs yaratish uchun schema."""
    pass


class CourseUpdate(BaseModel):
    """Kurs ma'lumotlarini yangilash (ixtiyoriy maydonlar)."""
    title: str | None = Field(None, min_length=3, max_length=500)
    description: str | None = Field(None, min_length=10)
    thumbnail_url: str | None = Field(None, max_length=500)
    is_published: bool | None = None
    order: int | None = Field(None, ge=0)


class CourseResponse(BaseModel):
    """API javobida qaytariladigan kurs ma'lumotlari."""
    id: uuid.UUID
    title: str
    description: str
    thumbnail_url: str | None
    is_published: bool
    order: int
    created_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
    # Darslar soni (hisoblab qo'shiladi)
    lessons_count: int = 0

    model_config = {"from_attributes": True}


class CourseListResponse(BaseModel):
    """Kurslar ro'yxati uchun wrapper."""
    total: int
    items: list[CourseResponse]
