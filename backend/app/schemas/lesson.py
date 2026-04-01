# Dars Pydantic schemalari — yaratish, yangilash va ko'rsatish uchun

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class LessonBase(BaseModel):
    """Dars uchun umumiy maydonlar."""
    title: str = Field(..., min_length=3, max_length=500, description="Dars sarlavhasi")
    content: str = Field("", description="Dars matni (HTML yoki Markdown)")
    video_url: str | None = Field(None, max_length=500, description="Video havola")
    order: int = Field(0, ge=0, description="Tartib raqami")
    duration_minutes: int | None = Field(None, gt=0, description="Davomiylik (daqiqa)")
    is_published: bool = Field(False, description="Nashr holati")


class LessonCreate(LessonBase):
    """Yangi dars yaratish uchun schema."""
    course_id: uuid.UUID = Field(..., description="Tegishli kurs ID si")
    module_id: uuid.UUID | None = Field(None, description="Tegishli modul ID si")


class LessonUpdate(BaseModel):
    """Dars ma'lumotlarini yangilash (ixtiyoriy maydonlar)."""
    title: str | None = Field(None, min_length=3, max_length=500)
    content: str | None = None
    video_url: str | None = Field(None, max_length=500)
    order: int | None = Field(None, ge=0)
    duration_minutes: int | None = Field(None, gt=0)
    is_published: bool | None = None
    module_id: uuid.UUID | None = None


class LessonResponse(BaseModel):
    """API javobida qaytariladigan dars ma'lumotlari."""
    id: uuid.UUID
    course_id: uuid.UUID
    module_id: uuid.UUID | None = None
    title: str
    content: str
    video_url: str | None
    order: int
    duration_minutes: int | None
    is_published: bool
    created_at: datetime
    updated_at: datetime
    # Joriy foydalanuvchi bu darsni tugatganmi? (hisoblab qo'shiladi)
    is_completed: bool = False

    model_config = {"from_attributes": True}


class LessonListResponse(BaseModel):
    """Darslar ro'yxati uchun wrapper."""
    total: int
    items: list[LessonResponse]
