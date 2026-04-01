# Modul Pydantic schemalari

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.lesson import LessonResponse


class ModuleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    order: int = Field(0, ge=0)
    is_published: bool = False


class ModuleUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = None
    order: int | None = Field(None, ge=0)
    is_published: bool | None = None


class ModuleResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    title: str
    description: str | None
    order: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    lessons_count: int = 0

    model_config = {"from_attributes": True}


class ModuleWithLessons(ModuleResponse):
    """Darslar bilan birga modul (admin uchun)."""
    lessons: list[LessonResponse] = []
