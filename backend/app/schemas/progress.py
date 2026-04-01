# Progress Pydantic schemalari — foydalanuvchi dars ko'rish holati

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ProgressCreate(BaseModel):
    """Dars tugatish yozuvi yaratish uchun schema."""
    lesson_id: uuid.UUID = Field(..., description="Tugatilgan dars ID si")
    course_id: uuid.UUID = Field(..., description="Tegishli kurs ID si")


class ProgressUpdate(BaseModel):
    """Progress holati yangilash uchun schema."""
    is_completed: bool = Field(..., description="Dars tugatildimi?")


class ProgressResponse(BaseModel):
    """API javobida qaytariladigan progress ma'lumotlari."""
    id: uuid.UUID
    user_id: uuid.UUID
    lesson_id: uuid.UUID
    course_id: uuid.UUID
    is_completed: bool
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CourseProgressResponse(BaseModel):
    """Kurs bo'yicha umumiy progress (foizda)."""
    course_id: uuid.UUID
    total_lessons: int = Field(..., description="Kursda jami darslar soni")
    completed_lessons: int = Field(..., description="Tugatilgan darslar soni")
    progress_percent: float = Field(
        ...,
        ge=0,
        le=100,
        description="Tugatilganlik foizi (0.0 - 100.0)",
    )
    # Har bir dars uchun alohida holat
    lessons: list[ProgressResponse] = []
