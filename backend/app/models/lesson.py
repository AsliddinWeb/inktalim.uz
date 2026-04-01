# Dars modeli — har bir kurs bir necha darsdan iborat
# Matn (HTML/Markdown) yoki video URL bo'lishi mumkin

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Lesson(Base):
    """Dars jadvali — kurs darslari."""

    __tablename__ = "lessons"

    # Birlamchi kalit — UUID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Qaysi kursga tegishli (FK → courses) — denormalizatsiya
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Qaysi modulga tegishli (FK → modules) — nullable: eski darslar uchun
    module_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Dars sarlavhasi
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # Dars matni — HTML yoki Markdown formatida
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    # Video havola (YouTube, Vimeo yoki to'g'ridan-to'g'ri URL)
    video_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Kurs ichidagi tartib raqami
    order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        index=True,
    )

    # Dars davomiyligi (daqiqalarda), nullable
    duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Nashr holati — False bo'lsa studentlarga ko'rinmaydi
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Yaratilgan vaqt
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Yangilangan vaqt
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Tegishli kurs
    course: Mapped["Course"] = relationship(  # type: ignore
        "Course",
        back_populates="lessons",
    )

    # Tegishli modul
    module: Mapped["Module"] = relationship(  # type: ignore
        "Module",
        back_populates="lessons",
    )

    # Bu dars bo'yicha progress yozuvlari
    progress_records: Mapped[list["Progress"]] = relationship(  # type: ignore
        "Progress",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Lesson id={self.id} title={self.title!r} order={self.order}>"
